
# Clojure-ClojureScript-Buck

Set of macroses that allow building Clojure and ClojureScript using [Buck](https://buckbuild.com) build system

## Features

- `clj_lib|cljs_lib(name,src,ns='',modules=[],deps=[]` Defines Clojure or ClojureScirpt module. Module can have other `modules` as dependencies and can include `deps` as dependency references outside your repo (Clojars in this case)

- `clj_project|cljs_project(module_name)` Creates project with source code of all modules combined. As well generates lein compatible project.clj with all external dependencies specified

- `clj_release|cljs_relase(modulef_name)` Creates release output for the library (uberjar or js file with advanced optimization)

## Installation

Take [lib](lib) file and put in a right place inside your repo. Then in your BUCK files reference it as `include_defs('//path/to/lib')`. Alternatively use [.buckconfig includes](https://buckbuild.com/concept/buckconfig.html#buildfile.includes)

## Example

See [example](example) folder for both Clojure and ClojureScript examples

## References

[Kapteko frontend](https://github.com/kapteko/frontend) built using this approach

## Status

I'm using it everywhere for Clojure and ClojureScript open source and not projects, although it's still an alpha quality - many corner cases are not covered. Right way of doing staff would be extending Buck, but for now it's too big task for me
