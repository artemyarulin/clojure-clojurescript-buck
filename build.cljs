(ns build.core
  (:require [planck.core :as core]
            [planck.io :as io]
            [planck.shell :as shell]
            [cljs.tools.reader :as reader]
            [clojure.string :as string]))

;; Helpers
(def make-dirs (partial shell/sh "mkdir" "-p"))
(def pwd (-> "pwd" shell/sh :out string/trim))
(defn copy [from to] (shell/sh "cp" "-r" from to))
(defn symlink [from to] (shell/sh "ln" from to))
(defn path-join [& args] (string/join "/" args))
(defn delete-last-path-component [p] (-> p (string/split "/") butlast (#(string/join "/" %))))
(defn delete-path [path] (shell/sh "rm" "-rf" path))
(defn pad-left [s len char] (if (< (count s) len) (recur (str char s) len char) s))

(defn path-from-content-namespace
  "Given basepath and file content will parse content and return new
  path based on file namespace"
  [base-path file-content]
  (letfn [(is-ns? [form] (and (list? form) (= (first form) 'ns) (< 1 (count form))))
          (parse-ns [form] (cond (is-ns? form) (-> form second str)
                                 (list? form) (some parse-ns form)))]
    (->> file-content
         (#(str "(\n" % "\n)")) ;; Workaround if content has more than one top level s-exp, otherwise read-string will return only first one
         (reader/read-string {:read-cond :allow :features #{:clj :cljs}})
         parse-ns
         (#(string/split % "."))
         butlast
         (#(apply path-join base-path %)))))

(defn organize-sources
  "Given source files and destination will go though all source files
  and exec copy-cmd for each file with original and new path which
  will be created based on a file namespace"
  [base-path files to copy-cmd]
  (letfn [(copy-source [source-file path-to]
            (let [source-path (.-path source-file)
                  source-name (-> source-path (string/split "/") last)]
              (make-dirs path-to)
              (copy-cmd source-path (path-join path-to source-name))))
          (find-out-path [file]
            (if (->> file :path (re-find #"clj$|cljs$|cljc$"))
              (->> file core/slurp (path-from-content-namespace to))
              (-> file :path (string/replace base-path "") (string/split "/") rest butlast
                  ((fn[path-parts]
                     ;; HACK: If we would use clj_module(src=glob(['src/**/*'])) then Buck would copy
                     ;; everything under src folder, but root folder would be still src, same for tests.
                     ;; So here we just flatten folders together in order to avoid paths like module/src/src/file
                     (if (= (first path-parts) (last (string/split to "/")))
                       (rest path-parts)
                       path-parts)))
                  (#(apply path-join to %)))))]
    (->> files
         (filter #(not (io/directory? %)))
         (mapv #(->> % find-out-path (copy-source %))))))

(defn organize-deps
  "Read deps file looking for sub-dependencies and merge all of them
  back into deps file"
  [deps-file]
  (letfn [(read-subdeps [path]
            (let [subdep-file (path-join path "deps")]
              (if (io/file-attributes subdep-file)
                (-> subdep-file core/slurp string/split-lines)
                [])))]
    (->> (core/slurp deps-file)
         string/split-lines
         (map read-subdeps)
         (apply concat)
         distinct
         (string/join "\n")
         (core/spit deps-file))))

(defn merge-deps-src
  "Merge deps source into current module src folder"
  [deps-file to]
  (->> (core/slurp deps-file)
       string/split-lines
       (mapv #(copy (path-join % "src") to))))

(defn update-project-file
  "Updates project file and replace tokens there with supplied data"
  [name main path]
  (let [project-file (path-join path "project.clj")]
    (-> (core/slurp project-file)
        (string/replace "{{name}}" name)
        (string/replace "{{main}}" main)
        (string/replace "{{deps}}" (core/slurp (path-join path "deps")))
        (#(core/spit project-file %)))))

(defn ensure-main-exists
  "Creates entry point file which requires all the existing module
  namespaces (including tests) which simplifies REPL and testing. Used
  as main if no main was supplied"
  [main path type]
  (let [def-main "module.core"
        find-all-namespaces (fn[path]
                              (->> (shell/sh "find" path "-type" "f" "-name" "*.cljc" "-o" "-name" (str "*." type))
                                   :out
                                   string/split-lines
                                   (map #(-> %
                                             (string/replace path "")
                                             (string/replace "/" ".")
                                             (string/replace "_" "-")
                                             (string/split ".")
                                             butlast
                                             rest))
                                   (map #(string/join "." %))))
        main-file (fn[namespaces]
                    (str "(ns " def-main " (:require "
                         (string/join "\n" (map #(str "[" % "]") namespaces))
                         "))"))
        main-path (path-join path "src" "module")]
    (make-dirs main-path)
    (->> (concat (find-all-namespaces (path-join path "src"))
                 (find-all-namespaces (path-join path "test")))
         (filter (complement string/blank?))
         (filter (partial not= "deps"))
         main-file
         (core/spit (path-join main-path (str "core." type))))
    (if (string/blank? main)
      def-main
      main)))

(defn get-all-project-deps []
  (shell/sh "buck" "build" "//ext:") ;; Ensure that all exts got built first
  (->> (shell/sh "buck" "targets" "//ext:" "--show-output" "--verbose" "0")
       :out
       string/split-lines
       (map #(string/split % " "))
       (map second)
       (map #(path-join pwd % "deps"))
       (map core/slurp)
       string/join))

(defn run-repl [args]
  (let [[_ project-file resource output-folder query] args
        targets (->> query (shell/sh "buck" "query") :out string/split-lines)
        source-dest-path (path-join pwd output-folder "src")
        resource-dest-path (path-join pwd output-folder "resources")]
    (delete-path source-dest-path)
    (delete-path resource-dest-path)
    (loop [targets' targets counter 1]
      (when-let [target (first targets')]
        (println (str "[" (-> counter str (pad-left (-> targets count str count) " ")) "/" (count targets) "] Linking " target))
        (let [buildfile-path (->> (shell/sh "buck" "query" (str "buildfile('" target "')")) :out (path-join pwd) delete-last-path-component)
              target-files (->> (shell/sh "buck" "query" (str "labels(srcs,deps('" target "'))")) :out string/split-lines (map #(path-join pwd %)))]
          (organize-sources buildfile-path
                            (map io/file target-files)
                            source-dest-path
                            symlink)
          (organize-sources buildfile-path
                            (->> target-files
                                 (filter #(not (re-find #"clj$|cljs$|cljc$" %)))
                                 (map io/file))
                            resource-dest-path
                            symlink))
        (recur (rest targets') (inc counter))))
    (organize-sources (delete-last-path-component resource) [(io/file resource)] (path-join resource-dest-path "public") symlink)
    (ensure-main-exists nil output-folder "cljs")
    (-> (core/slurp project-file)
        (string/replace "{{deps}}" (get-all-project-deps))
        (#(core/spit (path-join output-folder "project.clj") %)))))

(let [args core/*command-line-args*]
  (case (first args)
    "repl" (run-repl args)
    ;; We cannot run Buck commands while we are inside a command which is running by Buck again
    ;; As a workaround we print the actual command to execute, so we can still use it like
    ;; $(buck run repl -- "//...")
    "repl-init" (print (string/join " " (apply vector (nth args 1) "repl" (subvec (vec args) 2))))
    (let [parse-args #(let [info-file (-> % first core/slurp string/trim)]
                        (zipmap [:name :type :main :src :out :task]
                                (conj (string/split info-file ";") (second %))))
          {:keys [src out type task name main]} (parse-args args)
          build? (= task "build")]
      (organize-sources src (core/file-seq src) (path-join out (if build? "src" "test")) symlink)
      (merge-deps-src (path-join out "deps") out)
      (organize-deps (path-join out "deps"))
      (update-project-file name (if build? name (ensure-main-exists main out type)) out))))
