# Clojure-ClojureScript-Buck

Development version, moving everything to planck

For simple case we have:

``` python

# cat tests/BUCK
clj_module('a',tests='a_test.clj')

# which generates following targets
//RULES/clj-cljs/tests:__a     # Intermediate target, not to be meant to run manually
//RULES/clj-cljs/tests:a       # Build target, used as a dependency
//RULES/clj-cljs/tests:a-repl  # Executable to run repl! buck run RULES/clj-cljs/tests:a-repl start listening for nrepl connections
//RULES/clj-cljs/tests:a-test  # Test target - buck test //RULES/clj-cljs/test:a-test will run tests
```

## Status

Proof of concept - we can do it! Let's do it then!
