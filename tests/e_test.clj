(ns e.e-test
  (:require [e.e-clj :refer [e]]
            [clojure.test :refer [is deftest]]))

(deftest e-test
  (is (= e "e")))
