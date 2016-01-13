out=$1
source=$2
deps="${@:3}"
echo $deps > /tmp/files
read -r -d '' project << EOM
(defproject app "0.0.1"
  :dependencies [$deps]
  :plugins [[lein-cljsbuild "1.1.2"]]
  :source-paths ["src"]
  :cljsbuild {:builds {:debug {:source-paths ["src" ]
                               :compiler {:output-dir "debug"}}
                       :release {:source-paths ["src"]
                                 :compiler {:optimizations :advanced
                                            :output-to "release/main.js"}}}})
EOM

mkdir -p $out/src
rsync -r $source/ $out/src
echo $project > $out/project.clj
#(cd $out; lein cljsbuild once;)
