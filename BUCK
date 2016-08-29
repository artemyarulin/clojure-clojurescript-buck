export_file(name = 'build.cljs',
            visibility = ['PUBLIC'])

genrule(name = 'builder-planck',
        srcs = [],
        # HACK: If we change `build.cljs` file then `build` target would be updated, but because
        # it will generate exactly the same output (planck script invocation is the same) then
        # no rebuild will occur for dependent targets. Here we force it by including md5 checksum
        # into the script file as a comment
        # Note: --auto-cache --cache=$SRCDIR --static-fns optimisations doesn't bring anything
        bash = 'echo "planck $(location :build.cljs) \$@" > $OUT && ' +
               'echo "#`cat $(location :build.cljs) | md5`" >> $OUT && ' +
               'chmod +x $OUT',
        out = 'build.sh',
        executable = True,
        visibility = ['PUBLIC'])

for name in ['tester-lein-clj.sh',
             'tester-lein-cljs-doo.sh',
             'tester-lein-cljs-planck.sh',
             'tester-lein-cljc-doo.sh',
             'tester-lein-cljc-planck.sh']:
    export_file(name = name.split('.')[0],
                src = name,
                out = name,
                visibility = ['PUBLIC'])
