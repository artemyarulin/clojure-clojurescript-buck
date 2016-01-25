
# Clojure-ClojureScript-Buck

Set of macroses that allow building and testing Clojure and ClojureScript using [Buck](https://buckbuild.com) build system

## Features

- You can build both Clojure and ClojureScript
- Clojure test and support of testing using ClojureScript with [doo library](https://github.com/bensu/doo)
- Release task which will create uberjar for Clojure and advanced optimized JS for ClojureScript
- Dependencies on other modules within the same repo or use external dependencies

# API

``` python
clj_module|cljs_module(name,                 # Name of the module
                       src = None,           # List of source file which belongs to the module
                       ns = '',              # Namespace of the module
                       modules = [],         # List of depended modules
                       deps = [],            # List of external dependencies e.g. clojars links
                       tests = [],           # List of test files
                       test_modules = [],    # List of depended modules which required for testing
                       main = None):         # Main entry point if module it meant to be used as an app
```
New target equal to `name` will be created. It will gather all the sources and test files of a current module and depended modules, generates `project.clj` file using specified external dependencies and will build the project.
If `tests` specified - new target `test` would be created which will run the tests when called.
If `main` specified - new target `release` would be created which will generate release artifact when called.

# Example

- Shortest one:

`cat BUCK`:
``` python
clj_module('app')
```
`cat app.clj`:
``` clojure
(ns app.app)
(defn hello [m] (println "Hello " m)
```

- Full example:
`cat BUCK`:
``` python
cljs_module(name = 'mars',
	        src = ['mars.cljs','mars_helper.cljs'],
            ns = 'planets',
            modules = ['//planets/pluto',
			           '//planets/earth'],
 		    deps = ['[ktoa "0.1.2-SNAPSHOT"]',
			        '[convey "1.0.2"]'],
			tests = ['mars_test.cljs','mars_helper_test.cljs'],
            test_modules = ['[planet-test-helper "0.0.1"]'],
            main = 'planet.mars')
```
`cat mars.cljs`:
``` clojure
(ns planet.mars
  (:require [planet.pluto :as pluto]
            [planet.earth :as earth]
            [ktoa.core :refer [react-native]]))

(defn -main [& args]
  (println "Earth and Mars support Pluto with React Native:" earth pluto react-native))
```

## Installation

Take all the source files from the repo and put it to `public/clojure-clojurescript-buck` folder inside your repo. Then in your BUCK files reference it as `include_defs('//public/clojure-clojurescript-buck)`. Alternatively use [.buckconfig includes](https://buckbuild.com/concept/buckconfig.html#buildfile.includes)

If you want to put it in a different place - make sure that you've changed test files locations inside `module` function definition

## Status

I'm using it everywhere for Clojure and ClojureScript open source and not projects. Although it's just passed stage `Make it happen` and now I'm concentrated on a `Make it better`. Library has a lot of regular expressions, workaround, doesn't have error handling and most probably doesn't handle all the corner cases
