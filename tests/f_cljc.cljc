(ns f.core.f-cljc
  #?(:clj (:gen-class)))

#?(:clj
   (defn -main [& args]
     (println "f")))

#?(:cljs
   (.log js/console "f"))
