# Here goes example wrappers that you are free to modify depending on
# your needs. It's not meant to be updated with new releases of
# clj-cljs-buck: Use it as an example, change it and store in your
# repo

# Import clj-cljs macroses
include_defs('//lib.py')

def ext(name):
    return '//tests:' + name

cljs_deps = [ext('org.clojure/clojure'),
             ext('org.clojure/clojurescript'),
             ext('figwheel-sidecar'),
             ext('com.cemerick/piggieback')]

builder = '//:builder-planck'

def clj_module(name,src=None,modules=[],main=None,tests=[]):
    clj_cljs_module(ext = 'clj',
                    project_file = '//clj-cljs-config:project-clj',
                    builder = builder,
                    tester = '//:tester-lein-clj',
                    name = name,
                    src = src,
                    modules = ensure_list(modules) + [ext('org.clojure/clojure')],
                    main = main,
                    tests = tests)

def cljs_module(name,src=None,modules=[],main=None,tests=[]):
    clj_cljs_module(ext = 'cljs',
                    project_file = '//clj-cljs-config:project-cljs',
                    builder = builder,
                    resources = '//clj-cljs-config:figwheel-index',
                    tester = '//:tester-lein-cljs-planck',
                    name = name,
                    src = src,
                    modules = ensure_list(modules) + cljs_deps,
                    main = main,
                    tests = tests)

def cljc_module(name,src=None,modules=[],main=None,tests=[]):
    clj_cljs_module(ext = 'cljc',
                    project_file = '//clj-cljs-config:project-cljs',
                    builder = builder,
                    resources = '//clj-cljs-config:figwheel-index',
                    tester = '//:tester-lein-cljc-planck',
                    name = name,
                    src = src,
                    modules = ensure_list(modules) + cljs_deps,
                    main = main,
                    tests = tests)
