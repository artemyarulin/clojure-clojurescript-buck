
# ClojureScript-Buck

## Why?

With help of projects like [ktoa](https://github.com/artemyarulin/ktoa) and [om-next-crossplatform-template](https://github.com/artemyarulin/om-next-cross-platform-template) development of cross platform application with ClojureScript is reality of our days. Unfortunately traditional build systems care about one language support and maintaining multiple different build systems for iOS/Android/browser/node/ClojureScript is a hassle and makes things hard to manage.

Build systems like [Buck](https://buckbuild.com) and [Bazel](http://bazel.io) solve many problems, here the list of important staff for me:

1. Explicit dependency graph between your projects, even if they made using different language, like iOS application depends on CLJS app. For example you can change the module and find all the tests of the projects that depends on this module and run it
2. Unified way of building and testing. When you need to take care about multiple different project knowing that you can build any of them by `buck build project-name` is highly appreciated
3. Reliable cache - maintaining multiple application doesn't mean the build process has to be slow and rebuild all of it

Buck does solve all of those and a bunch of others. Why Buck and not Bazel? Because eventually Buck would support React Native and this is what we use right now

## Background

Buck shines when you have one big monorepo with all your projects. Check this [article](http://danluu.com/monorepo/) to get the idea why it's awesome. When you have one repo you don't think in terms of projects anymore, you begin to think in terms of small reusable modules. 

Don't want to go with monorepo? Consider using [git subtree](https://medium.com/@v/git-subtrees-a-tutorial-6ff568381844#.veprli3me) for this purpose. That's what I'm using currently in order to keep private and public repos together

## Features

- `cljs_lib(name,src,ns='',deps=[]` ClojureScript library: All source files from 'src' and output of 'deps' would be copied to the output. For each folder in src the content would be copied, without the root folder, so it makes easier to use like `cljs_lib('ktoa',src=['src'])` with existing libs

- `cljs_om_component(name,deps=['//ktoa:ktoa']` Wrapper around `cljs_lib` for easier om component creation. Allows you to build components with
just `cljs_om_component('page-header')` assuming that you have `page-header.cljs` file in the same folder

- `cljs_project(cljs_lib_name,project_deps=[]` Creates rule `:gen-project` which would generate lein project for the `cljs_lib_name` library you passed. Optionally you can pass a dependencies which would be included in the lein file

- `cljs_om_project(cljs_lib_name)` Wrapper around `cljs_project` which would include om dependency by default

## Example

See [example](example) folder. In short we define custom reusable Om-Next component, which, with help of `ktoa`, can be used on mobile and inside the browsers. And with help of `clojurescript-buck` we can test it independently. It's just two files!

`cat components/page-header/BUCK`:

``` python
include_defs('//clojurescript-buck/lib')

cljs_om_component('page-header')
cljs_om_project('page-header')
```

`cat components/page-hader/page-header.cljs`:

``` clojure
(ns components.page-header (:require [om.next :as om :refer-macros [defui]]
                                     [om.dom :as dom]))
(defui PageHeader
  ;; some code ommited for clarity, see full code in example folder
  Object
  (render [this] (dom/div nil "HelloWorld"))
  ```

`buck build page-header` would generate such output tree:
``` bash
$ tree page-header
page-header
└── cljs
    ├── component
    │   └── page-header.cljs
    ├── deps.cljs
    ├── ktoa
    │   ├── components.cljc
    │   ├── core.cljs
    │   ├── om.cljs
    │   ├── repl.cljc
    │   └── state.cljc
    ├── libs
    └── react
        ├── react.ext.js
        └── react.native.ext.js
```  

`buck build page-header:gen-project` would generate such output tree:

```
$ tree project.page-header
├── project.clj
└── src
    ├── component
    │   └── page-header.cljs
    ├── deps.cljs
    ├── ktoa
    │   ├── components.cljc
    │   ├── core.cljs
    │   ├── om.cljs
    │   ├── repl.cljc
    │   └── state.cljc
    ├── libs
    └── react
        ├── react.ext.js
        └── react.native.ext.js
```
Where `project.clj` would contain valid ready-made lein project file with all the needed dependencies

## References

[Kapteko frontend](https://github.com/kapteko/frontend) built using this approach

## Status

Proof of concept - still evaluating Buck and looking for the right approach to support ClojureScript. Right way of doing staff would be extending Buck, but for now it's too big task for me
