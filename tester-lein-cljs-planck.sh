set -e

cd $1

planck --classpath="test:src" \
       --eval="(ns test.test (:require [module.core] [cljs.test] [planck.core]))" \
       --eval="(defmethod cljs.test/report [:cljs.test/default :end-run-tests] [m] (when-not (cljs.test/successful? m) (planck.core/exit 1)))" \
       --eval="(cljs.test/run-all-tests)"
