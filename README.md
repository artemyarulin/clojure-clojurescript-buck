# Clojure-ClojureScript-Buck

[![Build Status](https://travis-ci.org/artemyarulin/clojure-clojurescript-buck.svg?branch=master)](https://travis-ci.org/artemyarulin/clojure-clojurescript-buck)

Set of macroses that allow building and testing Clojure and ClojureScript using [Buck](https://buckbuild.com) build system

## Features

- You can build both Clojure and ClojureScript
- Clojure test and support of testing using ClojureScript with [doo library](https://github.com/bensu/doo)
- Release task which will create uberjar for Clojure and advanced optimized JS for ClojureScript
- Dependencies on other modules within the same repo or use external dependencies with help of Clojars

# API

``` python
clj_module|cljs_module(name,                 # Name of the module
                       src = None,           # List of source file which belongs to the module
                       modules = [],         # List of depended modules
                       deps = [],            # List of external dependencies e.g. clojars links
                       tests = [],           # List of test files
                       main = None):         # Main entry point if module is meant to be used as an app
```
New target equal to `name` will be created. It will gather all the sources and test files of a current module and depended modules, generates `project.clj` file using specified external dependencies and will build the project.
If `tests` specified - new target `test` would be created which will run the tests when called.
If `main` specified - new target `release` would be created which will generate release artifact when called.

# Example

Check our [tests](tests/BUCK.tests) and corresponding generated [output](tests/output/tests.md) from them

## Installation

Take all the source files from the repo and put it to `public/clojure-clojurescript-buck/lib` folder inside your repo. Then in your BUCK files reference it as `include_defs('//public/clojure-clojurescript-buck/lib)`. Alternatively use [.buckconfig includes](https://buckbuild.com/concept/buckconfig.html#buildfile.includes)

If you want to put it in a different place - make sure that you've changed test files locations inside `module` function definition

## Status

I'm using it everywhere for Clojure and ClojureScript open source and not projects. Although it's just passed stage `Make it happen` and now I'm concentrated on a `Make it better`. Library has a lot of regular expressions, workaround, doesn't have error handling and most probably doesn't handle all the corner cases
