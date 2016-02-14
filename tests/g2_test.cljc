(ns g.g2-test
  #?(:clj (:require [g.core.g-cljc :refer [g]]
                    [clojure.test :refer [is deftest]]))
  #?(:cljs (:require [g.core.g-cljc :refer [g]]
                     [cljs.test :refer-macros [deftest is testing]])))

(deftest g-g2-test
  (is (= g "abacd1d2e")))
