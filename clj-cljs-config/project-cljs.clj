(defproject {{name}} "0.0.1"
  :dependencies [{{deps}}]
  :plugins [[lein-cljsbuild "1.1.3"]
            [lein-figwheel "0.5.4-7"]
            [lein-doo "0.1.6"]]
  :source-paths ["src" "test"]
  :repl-options {:nrepl-middleware [cemerick.piggieback/wrap-cljs-repl]
                 :init (do (use 'figwheel-sidecar.repl-api)(start-figwheel!))}
  :figwheel  {:http-server-root ""}
  :cljsbuild {:builds {:repl {:source-paths ["src" "test"]
                              :figwheel true
                              :compiler {:language-in :ecmascript5
                                         :language-out :ecmascript5
                                         :main {{main}}
                                         :asset-path "public/js"
                                         :output-dir "resources/public/js"
                                         :output-to "resources/public/js/module.js"}}
                       :debug {:source-paths ["src" "test"]
                               :compiler {:optimizations :whitespace
                                          :parallel-build true
                                          :language-in :ecmascript5
                                          :language-out :ecmascript5
                                          :output-dir "target"
                                          :output-to "target/{{name}}.js"}}
                       :release {:source-paths ["src"]
                                 :compiler {:optimizations :advanced
                                            :language-in :ecmascript5
                                            :language-out :ecmascript5
                                            :output-dir "release"
                                            :output-to "release/{{name}}.js"}}}})
