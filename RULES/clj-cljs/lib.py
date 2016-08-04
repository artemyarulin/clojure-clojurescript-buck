from functools import partial

def ensure_list(i):
    return i if isinstance(i,list) else [i]

def clj_cljs_module(ext,project_file,builder,name,src=None,modules=[],main=None,tests=[]):
    src = src or [name.replace('-','_') + '.' + ext]
    modules,tests= map(ensure_list,[modules,tests])

    # Main build rule - used mainly for dependencies
    genrule(name = name,
            srcs = src,
            bash = 'mkdir -p $OUT && ' +
                   'echo "{name};{type};{main};$SRCDIR;$OUT;" > $OUT/info && '.format(name=name,type=ext,main=main or "") +
                   ('&&'.join(map(lambda d: 'echo "$(location ' + d + ')" >> $OUT/deps',modules)) if len(modules) else 'true') + '&& ' +
                   '$(location {0}) $OUT/info build'.format(builder),
            out = 'build')
# # info
# $name;$type;main;$SRCDIR;$OUT
# $modules;
# $resources;

# $tests;
# $int_tests;




        # Intermediate task - gathers all source and test files together
        # genrule(name = '__' + full_name,
        #         srcs = tests + int_tests,
        #         bash = '$(location {0}) {1} {2} $SRCDIR $OUT'.format(build,ext,"build"),
        #         out = 'build')

        # REPL task
        # genrule(name = full_name + '-repl',
        #         srcs = [],
        #         bash = 'echo "cd $(location :{0}) && lein repl :headless :port 55444" > $OUT && chmod +x $OUT'.format('__' + full_name),
        #         executable = True,
        #         out = 'build')

        # # Actual test task
        # sh_test(name = full_name + '-test',
        #         test = test,
        #         args = [ext,'integrations' if int_tests else 'unit','$(location :{0}'.format('__' + full_name)],
        #         deps = [':__' + full_name])

def ext_dep(name):
    genrule(name = name.split()[0],
            srcs = [],
            bash = 'mkdir -p $OUT/src && echo "{0}" > $OUT/deps'.format(name),
            out = 'build',
            visibility = ['PUBLIC'])
