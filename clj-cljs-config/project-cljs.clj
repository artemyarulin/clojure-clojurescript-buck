(defproject {{name}} "0.0.1"
  :dependencies [{{deps}}]
  :plugins [[lein-cljsbuild "1.1.3"]
            [lein-doo "0.1.6"]]
  :source-paths ["src" "test"]
  :cljsbuild {:builds {:debug {:source-paths ["src" "test"]
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
