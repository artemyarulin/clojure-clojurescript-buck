(ns g.core.g-cljc
  (:require [a.a-cljc :refer [a]]
            [b.b-cljc :refer [b]]
            [c.c-cljc :refer [c]]
            [d.d1 :refer [d1]]
            [d.d2 :refer [d2]]
            [e.e-cljc :refer [e]])
  #?(:clj (:require [clojure.test :refer [deftest is run-tests]]
                    [aleph.http :as http]))
  #?(:clj (:gen-class)))

(def g (str a b c d1 d2 e))
