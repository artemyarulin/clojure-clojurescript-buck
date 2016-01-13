(ns components.page-header
  (:require [ktoa.components :refer [view text]]
            [ktoa.core :as ktoa]
            [om.next :as om :refer-macros [defui]]
            [om.dom :as dom]))

(defn render [mobile? menu-items]
  (if mobile?
    (view nil
          (map #(text nil "PageHeader:" (:page-header/title %)) menu-items))
    (dom/div nil
           (map #(dom/div nil "PageHeader:" (:page-header/title %)) menu-items))))

(defui PageHeader
  static om/IQuery (query [this] [:page-header/img
                                  {:page-header/menu
                                   [:page-header/title
                                    :page-header/link
                                    :page-header/selected?
                                    :page-header/highlighted?
                                    :page-header/mode-clicked?]}])
  static om/Ident (ident [this {:keys [img]}] [:page-header/by-img img])
  Object
  (render [this] (render ktoa/react-native [{:page-header/title "one"}
                                            {:page-header/title "two"}])))
