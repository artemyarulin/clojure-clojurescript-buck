(ns e.e-test
  #?(:clj (:require [e.e-cljc :refer [e]]
                     [clojure.test :refer [is deftest]]))
  #?(:cljs (:require [e.e-cljc :refer [e]]
                     [cljs.test :refer-macros [deftest is testing]])))

(deftest e-test
  (is (= e "e")))
