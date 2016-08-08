(ns e.e-test
  (:require [e.e-cljs :refer [e]]
            [cljs.test :refer-macros [deftest is testing]]))

(deftest e-test
  (is (= e "e")))
