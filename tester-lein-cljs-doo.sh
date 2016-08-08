set -e

cd $1

echo "(ns test.runner (:require [doo.runner :refer-macros [doo-all-tests]] \
                                [module.core])) (doo-all-tests)" > test/runner.cljs
LEIN_ROOT=1 lein doo phantom debug once
