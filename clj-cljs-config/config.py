# Here goes example wrappers that you are free to modify depending on
# your needs. It's not meant to be updated with new releases of
# clj-cljs-buck: Use it as an example, change it and store in your
# repo

# Import clj-cljs macroses
include_defs('//lib.py')

# Helpers for easier referencing different things
def ext(name):
    return '//tests:' + name
def executer(name):
    return '//:' + name
def resource(name):
    return '//clj-cljs-config:' + name
cljs_deps = [ext('org.clojure/clojure'),
             ext('org.clojure/clojurescript'),
             ext('figwheel-sidecar'),
             ext('com.cemerick/piggieback')]
builder = executer('builder-planck')

# First is CLJ wrapper - nothing fancy, we just predefine what project
# file to use, setup tester (which is an only options for CLJ for now)
# and add Clojure as dependency that is added always.

# Only interesting part is ensure_list that ensures that item is a
# list or wraps item with it. Most often you want to use one source
# file, one test, one module dependency so you can use
# clj_module(src='a.clj',tests='a_test.clj',modules=':b') without
# wrapping each with []
def clj_module(name,src=None,modules=[],main=None,tests=[],resources=[]):
    clj_cljs_module(ext = 'clj',
                    project_file = resource('project-clj'),
                    builder = builder,
                    resources = ensure_list(resources),
                    tester = executer('tester-lein-clj'),
                    name = name,
                    src = src,
                    modules = ensure_list(modules) + [ext('org.clojure/clojure')],
                    main = main,
                    tests = tests)

# Here goes CLJS wrapper with example of custom logic - if tests
# supplied than planck test executer is used (because it's 10 times
# faster!), otherwise classic doo.

# Another custom logic is release task - if main is specified then new
# target is added which creates release bundle
def cljs_module(name,src=None,modules=[],main=None,tests=[],resources=[],itests=[]):
    clj_cljs_module(ext = 'cljs',
                    project_file = resource('project-cljs'),
                    builder = builder,
                    resources = ensure_list(resources) + [resource('figwheel-index')],
                    tester = executer('tester-lein-cljs-doo') if itests else executer('tester-lein-cljs-planck'),
                    name = name,
                    src = src,
                    modules = ensure_list(modules) + cljs_deps,
                    main = main,
                    tests = tests)

    if (main):
        genrule(name + '-release',
                srcs = [],
                bash = 'mkdir $OUT && cd $(location :__{0}) && lein cljsbuild once release && cp release/{0}.js $OUT && cp -r resources $OUT'.format(name),
                out = 'build')

# Nothing interesting here - same as for CLJS, but wihtout release task
def cljc_module(name,src=None,modules=[],main=None,tests=[],resources=[],itests=[]):
    clj_cljs_module(ext = 'cljc',
                    project_file = resource('project-cljs'),
                    builder = builder,
                    resources = ensure_list(resources) + [resource('figwheel-index')],
                    tester = executer('tester-lein-cljs-doo') if itests else executer('tester-lein-cljs-planck'),
                    name = name,
                    src = src,
                    modules = ensure_list(modules) + cljs_deps,
                    main = main,
                    tests = tests)
