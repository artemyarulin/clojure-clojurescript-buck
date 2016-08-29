(defproject repl "0.0.1"
  :dependencies [{{deps}}]
  :plugins [[lein-cljsbuild "1.1.3"]
            [lein-figwheel "0.5.4-7"]]
  :source-paths ["src"]
  :repl-options {:nrepl-middleware [cemerick.piggieback/wrap-cljs-repl]
                 :init (do (use 'figwheel-sidecar.repl-api)(start-figwheel!))}
  :figwheel  {:hawk-options {:watcher :polling}}
  :cljsbuild {:builds {:repl {:source-paths ["src"]
                              :figwheel true
                              :compiler {:language-in :ecmascript5
                                         :language-out :ecmascript5
                                         :main module.core
                                         :asset-path "js"
                                         :output-dir "resources/public/js"
                                         :output-to "resources/public/js/module.js"}}}})
