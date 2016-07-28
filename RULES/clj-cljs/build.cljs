;; planck build file
(ns build.core
  (:require [planck.core :as core]
            [planck.io :as io]
            [planck.shell :as shell]
            [cljs.tools.reader :as reader]))

(defn log [s]
  (core/spit "/tmp/buck-clj.log" (str "[" (.toISOString (js/Date.)) "] " s "\n") :append true))

(def make-dirs (partial shell/sh "mkdir" "-p"))

(defn ns-decl? [form]
  (and (list? form)
       (= 'ns (first form))
       (< 1 (count form))))

(defn parse-ns [form]
  (cond
    (ns-decl? form) (-> form str)
    (list? form) (some parse-ns form)))

(defn parse-args [args]
  {:type (first args)
   :task (second args)
   :src (nth args 2)
   :out (last args)})

(defn build [run-options]
  (let [args (parse-args run-options)
        _ (log (str "Running: " args))]
    (case (:task args)
      "build" (do
                (make-dirs (:out args))
                (core/spit (str (:out args) "/file.out" )
                           (str args)))
      "repl" (do
               (println "NRepl listening on 55444")
               (println (shell/sh "lein" "repl" ":headless" ":port" "55444")))
      "test" (do
               (println "Nope, wrong test")
               (core/exit 99)))
    (log "Done")))

(build core/*command-line-args*)
