(ns g.g1-test
  (:require [g.core.g-clj :refer [g]]
            [clojure.test :refer [is deftest]]))

(deftest g-g1-test
  (is (= g "abacd1d2e")))
