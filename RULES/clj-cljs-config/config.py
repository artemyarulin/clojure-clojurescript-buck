include_defs('//RULES/clj-cljs/lib.py')

def target(name):
    return '//ext:' + name

# Define module wrappers with preferred options
def clj_module(name,src=None,modules=[],main=None,tests=[]):
    clj_cljs_module(ext = 'clj',
                    project_file = '//RULES/clj-cljs-config:project-clj',
                    builder = '//RULES/clj-cljs:builder',
                    name = name,
                    src = src,
                    modules = ensure_list(modules) + [target('org.clojure/clojure')],
                    main = main,
                    tests = tests)

def cljs_module(name,src=None,modules=[],main=None,tests=[]):
    clj_cljs_module(ext = 'cljs',
                    project_file = '//RULES/clj-cljs-config:project-cljs',
                    builder = '//RULES/clj-cljs:builder',
                    resources = '//RULES/clj-cljs-config:figwheel-index',
                    name = name,
                    src = src,
                    modules = ensure_list(modules) + [target('org.clojure/clojure'),
                                                      target('org.clojure/clojurescript'),
                                                      target('figwheel-sidecar'),
                                                      target('com.cemerick/piggieback')],
                    main = main,
                    tests = tests)

def cljc_module(name,src=None,modules=[],main=None,tests=[]):
    clj_cljs_module(ext = 'cljc',
                    project_file = '//RULES/clj-cljs-config:project-cljs',
                    builder = '//RULES/clj-cljs:builder',
                    name = name,
                    src = src,
                    modules = ensure_list(modules) + [target('org.clojure/clojure'),
                                                      target('org.clojure/clojurescript')],
                    main = main,
                    tests = tests)
