(ns build.core
  (:require [planck.core :as core]
            [planck.io :as io]
            [planck.shell :as shell]
            [cljs.tools.reader :as reader]
            [clojure.string :as string]))

;; Helpers
(def make-dirs (partial shell/sh "mkdir" "-p"))
(defn copy [from to] (shell/sh "cp" "-r" from to) (println "Copy:" "cp" "-r" from to))
(defn path-join [& args] (string/join "/" args))
(defn time-now [] (str "[" (.toISOString (js/Date.)) "] "))
(defn log [s] (core/spit "/tmp/buck-clj.log" (str (time-now) s "\n") :append true) (println s))


"a" "a-clj"

(defn organize-sources [from to]
  (letfn [(is-ns? [form] (and (list? form) (= (first form) 'ns) (< 1 (count form))))
          (parse-ns [form] (cond (is-ns? form) (-> form second str)
                                 (list? form) (some parse-ns form)))
          (path-for-ns [ns] (-> ns (string/split ".") butlast (#(apply path-join to %))))
          (copy-source [source-file path-to]
            (let [source-path (.-path source-file)
                  source-name (-> source-path (string/split "/") last)]
              (make-dirs path-to)
              (copy source-path (path-join path-to source-name))))]
    (->> (core/file-seq from)
         (filter #(not (io/directory? %)))
         (mapv #(->> %
                     core/slurp
                     (reader/read-string {:read-cond :allow :features #{:clj :cljs}})
                     parse-ns
                     path-for-ns
                     (copy-source %))))))

(defn parse-args [args]
  (let [info-file (-> args first core/slurp string/trim)]
    (zipmap [:name :type :main :src :out :task]
            (conj (string/split info-file ";") (second args)))))

(defn organize-deps [deps-file]
  (letfn [(format-dep [dep]
            (let [[name ver] (string/split dep " ")]
              (str "[" name " \"" ver "\"]")))
          (read-subdeps [path]
            (let [subdep-file (path-join path "deps")]
              (if (io/file-attributes subdep-file)
                (-> subdep-file core/slurp string/split-lines)
                [])))
          ]
    (->> (core/slurp deps-file)
         string/split-lines
         (map read-subdeps)
         (apply concat)
         (map format-dep)
         distinct
         (string/join "\n")
         (core/spit deps-file))))

(defn merge-deps-src [deps-file to]
  (->> (core/slurp deps-file)
       string/split-lines
       (mapv #(copy (path-join % "src") to))))

(defn update-project-file [name main path]
  (let [project-file (path-join path "project.clj")]
    (-> (core/slurp project-file)
        (string/replace "{{name}}" name)
        (string/replace "{{main}}" main)
        (string/replace "{{deps}}" (core/slurp (path-join path "deps")))
        (#(core/spit project-file %)))))

(defn ensure-main-exists [main path type]
  (if (string/blank? main)
    (let [def-main "module.core"
          find-all-namespaces (fn[path]
                                (->> (shell/sh "find" path "-type" "f" "-name" "*.clj*")
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
           main-file
           (core/spit (path-join main-path (str "core." type))))
      def-main)
    main))

(let [{:keys [src out type task name main]} (parse-args core/*command-line-args*)]
  (case task
    "build" (do
              (organize-sources src (path-join out "src"))
              (merge-deps-src (path-join out "deps") out)
              (organize-deps (path-join out "deps")))
    "test" (do
             (organize-sources src (path-join out "test"))
             (update-project-file name
                                  (ensure-main-exists main out type)
                                  out))))
