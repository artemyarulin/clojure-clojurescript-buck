from functools import partial

def_rules = {"build":"//RULES/clj-cljs:build",
             "repl":"//RULES/clj-cljs:build",
             "test":"//RULES/clj-cljs:build"}

def ensure_list(i):
    return i if isinstance(i,list) else [i]

def module(ext,name,src = None,rules = {},tests = []):
    src = src or [name.replace('-','_') + '.' + ext]
    tests = ensure_list(tests)

    # User may want to override default rules, so let's add it only in case it's not there
    if ("" not in rules):
        rules[""] = def_rules

    for suffix in rules:
        build = rules[suffix]['build']
        repl = rules[suffix]['repl']
        test = rules[suffix]['test']
        full_name = name + suffix

        # Main build rule - used mainly for dependencies
        genrule(name = full_name,
                srcs = src,
                bash = '$(exe {0}) {1} {2} $SRCDIR $OUT'.format(build,ext,"build"),
                out = 'build')

        # Intermediate task - gathers all source and test files together
        genrule(name = '__' + full_name,
                srcs = tests,
                bash = 'mkdir -p $OUT/test && ' +
                       'rsync -r $(location :{0})/ $OUT && '.format(full_name) +
                       'cp -r $SRCDIR/* $OUT/test',
                out = 'build')

        # REPL task
        genrule(name = full_name + '-repl',
                srcs = [],
                bash = 'echo "cd $(location :{0}) && lein repl :headless :port 55444" > $OUT && chmod +x $OUT'.format('__' + full_name),
                executable = True,
                out = 'build')

        # Actual test task
        sh_test(name = full_name + '-test',
                test = test,
                args = [ext,'test','$(location :{0}'.format('__' + full_name)],
                deps = [':__' + full_name])

clj_module  = partial(module,'clj')
cljs_module = partial(module,'cljs')
cljc_module = partial(module,'cljc')
