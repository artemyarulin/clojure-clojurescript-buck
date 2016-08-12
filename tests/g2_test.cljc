(ns g.g2-test
  (:require [g.core.g-cljc :refer [g]]
            [clojure.test :refer [is deftest]]))

(deftest g-g2-test
  (is (= g "abacd1d2e")))
