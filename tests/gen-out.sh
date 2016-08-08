# Run from the root of the repo, like:
# ./RULES/clojure-clojurescript-buck/tests/gen-out.sh `buck targets RULES/clojure-clojurescript-buck/tests:`

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
out=$DIR/output
doc=$out/tests.md

rm -rf $out/*
echo "# Test output" > $doc

for target in "$@"
do
    name=`echo $target | sed -e "s/.*://"`
    echo "## $name" >> $doc
    buck query "deps('$target')" --dot | sed -e "s/\/\/RULES\/clojure-clojurescript-buck\/tests//g; s/\/\/RULES\/clojure-clojurescript-buck//g" | dot -Tpng > $out/$name.png
    echo '!'"[$name]($name.png)" >> $doc
    build=`echo $target | sed -e "s/\//buck-out\/gen/; s/:/\//"`
    echo '```' >> $doc
    tree $build >> $doc
    echo '```' >> $doc

    if [ $(find $build -name "project.clj" | wc -l) -gt 0 ]; then
	echo '`cat project.clj`:' >> $doc
	echo '``` clojure' >> $doc
	find $build -name "project.clj" -exec cat {} \; >> $doc
	echo '```' >> $doc
    fi
done
