set -e

cd $1

tests=`(cd test && find . -type f ! -name runner.cljs | sed -e "s/.cljs//; s/.\///; s/\//./g; s/_/-/g; s/$/]/; s/^/[/")`

echo "(ns test.runner (:require [doo.runner :refer-macros [doo-all-tests]] \
                                 $tests)) (doo-all-tests)" > test/runner.cljs
lein doo phantom debug once
lein doo phantom integration once
