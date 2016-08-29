# Here goes example wrappers that you are free to modify depending on
# your needs. It's not meant to be updated with new releases of
# clj-cljs-buck: Use it as an example, change it and store in your
# repo

include_defs('//lib.py')

# Set of helpers
def ext(name):
    return '//tests:' + name
def executer(name):
    return '//:' + name
def resource(name):
    return '//clj-cljs-config:' + name
def ensure_list(i):
    return i if isinstance(i,list) else [i]
cljs_deps = [ext('org.clojure/clojure'),
             ext('org.clojure/clojurescript'),
             ext('figwheel-sidecar'),
             ext('com.cemerick/piggieback')]
builder = executer('builder-planck')

def module(ext,project_file,name,src,main,resources,modules,tests,test_resources,test_modules,tester,tester_args=[]):
    """Module creator helper. ensure_list that ensures that item is a list
    or wraps item with it. Most often you want to use one source file,
    one test, one module dependency so you can use
    clj_module(src='a.clj',tests='test.clj',modules=':b') without
    wrapping each with []. Also allows specifiying module without
    source files. name + ext will be used instead
    """
    src = [name.replace('-','_') + '.' + ext] if src == None else ensure_list(src)

    clj_cljs_module(ext = ext,
                    project_file = resource(project_file),
                    builder = builder,
                    name = name,
                    resources = ensure_list(resources),
                    src = src,
                    modules = ensure_list(modules),
                    main = main)
    if tests:
        clj_cljs_module(ext = ext,
                        project_file = resource(project_file),
                        builder = builder,
                        name = name,
                        resources = ensure_list(test_resources),
                        src = ensure_list(tests),
                        modules = ensure_list(test_modules) + [':' + name],
                        main = main,
                        tester = tester,
                        tester_args = tester_args)

def clj_module(name,src=None,modules=[],main=None,tests=[],test_modules=[],resources=[],test_resources=[]):
    """First is CLJ wrapper - nothing fancy, we just predefine what
    project file to use, setup tester (which is an only options for
    CLJ for now) and add Clojure as dependency that is added always.
    """
    module('clj',
           'project-clj',
           name,
           src,
           main,
           resources,
           ensure_list(modules) + [ext('org.clojure/clojure')],
           tests,
           test_resources,
           test_modules,
           executer('tester-lein-clj'))

def cljs_module(name,src=None,modules=[],main=None,tests=[],test_modules=[],resources=[],test_resources=[],itests=[]):
    """Here goes CLJS wrapper with example of custom logic - if tests
    supplied than planck test executer is used (because it's 10 times
    faster!), otherwise classic doo. Another custom logic is release
    task - if main is specified then new target is added which creates
    release bundle
    """
    module('cljs',
           'project-cljs',
           name,
           src,
           main,
           resources,
           ensure_list(modules) + cljs_deps,
           ensure_list(tests) + ensure_list(itests),
           test_resources,
           test_modules,
           executer('tester-lein-cljs-doo') if itests else executer('tester-lein-cljs-planck'))

    if (main):
        genrule(name + '-release',
                srcs = [],
                bash = 'mkdir $OUT && cd $(location :{0}) && lein cljsbuild once release && cp release/{0}.js $OUT && cp -r resources $OUT'.format(name),
                out = 'build')

def cljc_module(name,src=None,modules=[],main=None,tests=[],test_modules=[],resources=[],test_resources=[],itests=[]):
    module('cljc',
           'project-cljs',
           name,
           src,
           main,
           resources,
           ensure_list(modules) + cljs_deps,
           ensure_list(tests) + ensure_list(itests),
           test_resources,
           test_modules,
           executer('tester-lein-cljs-doo') if itests else executer('tester-lein-cljs-planck'))

