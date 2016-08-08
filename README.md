# Clojure-ClojureScript-Buck

[![Build Status](https://travis-ci.org/artemyarulin/clojure-clojurescript-buck.svg?branch=master)](https://travis-ci.org/artemyarulin/clojure-clojurescript-buck)

Clojure and ClojureScript support for [Buck build system](https://buckbuild.com). If you have Clojure/ClojureScript and monorepo then it's a thing to check

## Features

- Build Clojure/ClojureScript
- Run tests for Clojure and choose what test runner to use with ClojureScript: [doo](https://github.com/bensu/doo) or [Planck](http://planck-repl.org/testing.html)!
- Build and test any Clojure/ClojureScript with always the same command: `buck build [module-name] && buck test [module-name]-test`
- Run REPL into the module without too much thinking about details: `buck run [module-name]-repl`
- All the features from [Buck build system](https://buckbuild.com) - it's a peace of cake!

## What problems does it solve

- It allows you to use Clojure/ClojureScript inside a monorepo where different projects may depends on each other
- With project based approach where you have one Leningen/Boot project per application/library it's sometimes difficult to reuse some part of the code between projects. Buck instead encourages you to create many small independent modules with their own dependencies/source/tests which will improve your code reuse
- Buck allows to abstract build/test steps into functions that can be used later on across your repo

## Installation and requirements

Currently only MacOS is supported. Linux/Windows support is covered in this [issue 18](https://github.com/artemyarulin/clojure-clojurescript-buck/issues/18)

Just copy `RULES` folder into your repo, then configure your `.buckconfig` and include of `clj-cljs-config`:

```
[buildfile]
  includes = //RULES/clj-cljs-config/config.py
```

`RULES` has two subfolders:
- `clj-cljs` - folder with actual macro helpers which builds Clojure and ClojureScript. Not meant to be modified
- `clj-cljs-config` - has all configuration related to build process. Feel free to modify according to your needs

It's recommended to create a separate folder with list of external libs, like it's done in [ext/BUCK](ext/BUCK)

## Configuration

Idea it that `clj_cljs_module` is low level function and it's used always via some wrapper functions like in [RULES/clj-cljs-config/config.py](RULES/clj-cljs-config/config.py) where you can specify custom project files, default dependencies (Clojure/ClojureScript versions), different builders or testers

## How does it work

Under the hood we simply create Leiningen project and put files and parameters in the right place.

Entry point would be your [custom wrapper](RULES/clj-cljs-config/config.py) with supplied project file on top of `clj_cljs_module` function in [lib.py](RULES/clj-cljs/lib.py), which in turn will save all supplied parameters to `info` file which then would be executed by builder. For now only Planck based [builder.cljs](RULES/clj-cljs/build.cljs) is available.

`builder` then:
- Create a normal folder structure (with source files placed in a right sub-folder, etc.)
- Collect all sub-dependencies
- Create entry point file which requires all the existing module namespaces (including tests) which simplifies REPL and testing
- Update project file with actual data

## Status

Foundation is solid and unlikely that API gonna change in near feature. It's a second big rewrite already so most of the edge cases should be covered. Although it still missing some important things like [Figwheel support](https://github.com/artemyarulin/clojure-clojurescript-buck/issues/19)

## Alternatives

- [lein-monolith](https://github.com/amperity/lein-monolith) from Amperity - is a Leiningen plugin to work with multiple projects inside a monorepo. Doesn't require any additional tools but Leiningen, much easier to start with, although it still uses project approach.

- [Ladder developer mentioned on HN](https://news.ycombinator.com/item?id=11507975) that they have their own solution for CLJ/CLJS + Buck which looks awesome but not yet open sourced and includes some hacks in CLJS compiler.

- [make](https://www.gnu.org/software/make/) - there are no tasks that you cannot do with make. If you like bare metal - then check [version 1.0.0](https://github.com/artemyarulin/clojure-clojurescript-buck/tree/1.0.0), it was implemented with power of shell,sed,grep and regexps.
