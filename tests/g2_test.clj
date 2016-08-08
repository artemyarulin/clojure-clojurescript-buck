(ns g.g2-test
  (:require [g.core.g-clj :refer [g]]
            [clojure.test :refer [is deftest]]))

(deftest g-2-test
  (is (= g "abacd1d2e")))
