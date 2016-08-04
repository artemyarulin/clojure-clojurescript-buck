(ns g.core.g-clj
  (:require [a.a-clj :refer [a]]
            [b.b-clj :refer [b]]
            [c.c-clj :refer [c]]
            [d.d1 :refer [d1]]
            [d.d2 :refer [d2]]
            [e.e-cljc :refer [e]]
            [aleph.http :as http]
            [clojure.data.json :as json])
  (:gen-class))

(def g (str a b c d1 d2 e))
