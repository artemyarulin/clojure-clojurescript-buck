from functools import partial

def ensure_list(i):
    return i if isinstance(i,list) else [i]

def clj_cljs_module(ext,project_file,builder,tester,name,src=None,modules=[],main=None,tests=[],resources=[]):
    src = src or [name.replace('-','_') + '.' + ext]
    modules,tests,resources= map(ensure_list,[modules,tests,resources])

    # Main build rule - used mainly for dependencies
    genrule(name = name,
            srcs = src,
            bash = 'mkdir -p $OUT/resources && ' +
                   ('&&'.join(map(lambda d: 'rsync -r $(location ' + d + ') $OUT/resources',resources)) if len(resources) else 'true') + '&&' +
                   ('&&'.join(map(lambda d: 'rsync -r --prune-empty-dirs $(location ' + d + ')/resources/ $OUT/resources',modules)) if len(modules) else 'true') + '&&' +
                   'echo "{name};{type};{main};$SRCDIR;$OUT;" > $OUT/info && '.format(name=name,type=ext,main=main or "") +
                   ('&&'.join(map(lambda d: 'echo "$(location ' + d + ')" >> $OUT/deps',modules)) if len(modules) else 'true') + '&& ' +
                   '$(location {0}) $OUT/info build'.format(builder),
            out = 'build')

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

    # REPL task
    genrule(name = name + '-repl',
            srcs = [],
            bash = 'echo "cd $(location :{0}) && lein repl :headless :port 55444" > $OUT && chmod +x $OUT'.format('__' + name),
            executable = True,
            out = 'build')

    if tests:
        # Actual test task
        sh_test(name = name + '-test',
                test = tester,
                args = ['$(location :{0})'.format('__' + name)],
                deps = [':__' + name])

def ext_dep(name):
    genrule(name = name.split()[0],
            srcs = [],
            bash = 'mkdir -p $OUT/{{src,resources}} && echo "[{0} \\"{1}\\"]" > $OUT/deps'.format(*name.split()),
            out = 'build',
            visibility = ['PUBLIC'])
