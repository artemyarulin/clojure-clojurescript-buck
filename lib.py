def clj_cljs_module(ext,                  # One of [clj cljs cljc]
                    project_file,         # Buck query that points to project file associated with extension
                    builder,              # Buck query to builder which would be run for building a module
                    name,                 # Name of generated target. Following targets will be created ['target' '__target' 'target-test']
                    src = None,           # List of source files that module uses
                    modules = [],         # List of submodules that current module depends on. It will be copied to module folder before building
                    resources = [],       # List of resources that current module depends on. It will be copied to resource module folder before building
                    main = None,          # Main entry point of a module if exists. Used for releases
                    tester = None,        # If current module is a test then it should be a Buck query to tester which would be run for testing a module
                    tester_args = []):    # List of additional test arguments which would be supplied to tester during test run

    # Prepares required resources and modules sub-dependencies. Create
    # info file with module settings and calls builder
    genrule(name = '__' + name if tester else name,
            srcs = src,
            bash = 'mkdir -p $OUT/resources && ' +
                   ('&&'.join(map(lambda d: 'rsync -r $(location ' + d + ') $OUT/resources',resources)) if len(resources) else 'true') + '&&' +
                   ('&&'.join(map(lambda d: 'rsync -r --prune-empty-dirs $(location ' + d + ')/resources/ $OUT/resources',modules)) if len(modules) else 'true') + '&&' +
                   'echo "{name};{type};{main};$SRCDIR;$OUT;" > $OUT/info && '.format(name=name,type=ext,main=main or "") +
                   ('&&'.join(map(lambda d: 'echo "$(location ' + d + ')" >> $OUT/deps',modules)) if len(modules) else 'true') + '&& ' +
                   'cp $(location {0}) $OUT/project.clj && '.format(project_file) +
                   '$(location {0}) $OUT/info {1}'.format(builder,'test' if tester else 'build'),
            out = 'build',
            visibility = ['PUBLIC'])

    if tester: # Actual test task - simply run tester in the right folder
        sh_test(name = name + '-test',
                test = tester,
                args = ['$(location :{0})'.format('__' + name)] + tester_args,
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

def clj_cljs_repl(name,builder,project_file,resource,output_folder):
    genrule(name = name,
            srcs = [],
            bash = 'echo "$(location {0}) repl-init $(location {0}) $(location {1}) $(location {2}) {3} \$@" > $OUT && chmod +x $OUT'.format(builder,project_file,resource,output_folder),
            out = 'repl.sh',
            visibility = ['PUBLIC'],
            executable = True)
