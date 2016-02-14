(ns g.core.g-cljs
  (:require [a.a-cljs :refer [a]]
            [b.b-cljs :refer [b]]
            [c.c-cljs :refer [c]]
            [d.d1 :refer [d1]]
            [d.d2 :refer [d2]]
            [e.e-cljc :refer [e]]))

(def g (str a b c d1 d2 e))
