(ns g.g1-test
  (:require [g.core.g-cljs :refer [g]]
            [cljs.test :refer-macros [deftest is testing]]))

(deftest g-g1-test
  (is (= g "abacd1d2e")))
