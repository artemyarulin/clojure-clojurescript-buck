from functools import partial

def ensure_list(i):
    return i if isinstance(i,list) else [i]

def clj_cljs_module(ext,project_file,builder,tester,name,src=None,modules=[],main=None,tests=[],resources=[]):
    "Defines CLJ/CLJS/CLJC module. As it defines low level interface you are encouruged to wrap it with your custom function"
    src = [name.replace('-','_') + '.' + ext] if src == None else src
    modules,tests,resources= map(ensure_list,[modules,tests,resources])

    # Prepares required resources and modules sub-dependencies. Create
    # info file with module settings and calls builder
    genrule(name = name,
            srcs = src,
            bash = 'mkdir -p $OUT/resources && ' +
                   ('&&'.join(map(lambda d: 'rsync -r $(location ' + d + ') $OUT/resources',resources)) if len(resources) else 'true') + '&&' +
                   ('&&'.join(map(lambda d: 'rsync -r --prune-empty-dirs $(location ' + d + ')/resources/ $OUT/resources',modules)) if len(modules) else 'true') + '&&' +
                   'echo "{name};{type};{main};$SRCDIR;$OUT;" > $OUT/info && '.format(name=name,type=ext,main=main or "") +
                   ('&&'.join(map(lambda d: 'echo "$(location ' + d + ')" >> $OUT/deps',modules)) if len(modules) else 'true') + '&& ' +
                   '$(location {0}) $OUT/info build'.format(builder),
            out = 'build',
            visibility = ['PUBLIC'])

    # REPL/Test task: For testing we have to have separate target (or
    # include test files into main target, which we don't want). It
    # copies everything from main build target and call builder again
    # but with info file and `test` as arguments for additional
    # processing
    genrule(name = '__' + name,
            srcs = tests,
            bash = 'mkdir -p $OUT && ' +
                   'echo "{name};{type};{main};$SRCDIR;$OUT;" > $OUT/info && '.format(name=name,type=ext,main=main or "") +
                   'cp -r $(location :{0})/src $OUT && '.format(name) +
                   'cp -r $(location :{0})/deps $OUT && '.format(name) +
                   'cp -r $(location :{0})/resources $OUT && '.format(name) +
                   'cp $(location {0}) $OUT/project.clj && '.format(project_file) +
                   '$(location {0}) $OUT/info test'.format(builder),
            out = 'build')

    # Simple REPL task - additional settings may be specified via project.clj :repl-options
    genrule(name = name + '-repl',
            srcs = [],
            bash = 'echo "cd $(location :{0}) && lein repl :headless :port 55444" > $OUT && chmod +x $OUT'.format('__' + name),
            executable = True,
            out = 'build')

    # Actual test task - simply run tester in the right folder
    if tests:
        sh_test(name = name + '-test',
                test = tester,
                args = ['$(location :{0})'.format('__' + name)],
                deps = [':__' + name])

def ext_dep(name):
    """Defines external dependency which then can be references from other
    modules. Name should be in format '[name] [version]' like 'koh
    0.1.1', but it will generate a target with name equal to name
    without version, ex. 'koh'.  Idea is to have only one version of
    external dependency across your monorepo while other modules don't
    know anything about actual version"""
    genrule(name = name.split()[0],
            srcs = [],
            bash = 'mkdir -p $OUT/{{src,resources}} && echo "[{0} \\"{1}\\"]" > $OUT/deps'.format(*name.split()),
            out = 'build',
            visibility = ['PUBLIC'])
