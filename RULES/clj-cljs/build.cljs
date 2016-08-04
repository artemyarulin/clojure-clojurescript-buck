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
                  source-name (->> source-path (string/split "/") last)]
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

(defn merge-deps-src [deps-file to]
  (->> (core/slurp deps-file)
       string/split-lines
       (mapv #(copy (path-join % "src") to))))

(let [{:keys [src out task]} (parse-args core/*command-line-args*)]
  (case task
    "build" (do
              (organize-sources src (path-join out "src"))
              (merge-deps-src (path-join out "deps") out)
              (organize-deps (path-join out "deps")))))
