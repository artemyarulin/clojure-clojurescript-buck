(ns g.g2-test
  (:require [g.core.g-cljs :refer [g]]
            [cljs.test :refer-macros [deftest is testing]]))

(deftest g-g2-test
  (is (= g "abacd1d2e")))
