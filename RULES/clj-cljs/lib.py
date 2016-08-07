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

    # Intermediate task - gathers all source and test files together
    if tests:
        genrule(name = '__' + name,
                srcs = tests,
                bash = 'mkdir -p $OUT && ' +
                       'echo "{name};{type};{main};$SRCDIR;$OUT;" > $OUT/info && '.format(name=name,type=ext,main=main or "") +
                       'cp -r $(location :{0})/src $OUT && '.format(name) +
                       'cp -r $(location :{0})/deps $OUT && '.format(name) +
                       'cp $(location {0}) $OUT && '.format(project_file) +
                       '$(location {0}) $OUT/info test'.format(builder),
                out = 'build')

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
