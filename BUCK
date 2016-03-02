export_file(name = 'clj_test.sh',
            out = 'clj_test.sh',
            visibility = ['PUBLIC'])

export_file(name = 'cljs_test.sh',
            out = 'cljs_test.sh',
            visibility = ['PUBLIC'])

module(name = 'clojure',
       ext = '.clj',
       src = [],
       modules = [],
       deps = ['[org.clojure/clojure "1.8.0"]'],
       tests = [],
       main = None,
       template = '(defproject clojure "0.0.1")',
       resources = [])

clj_module(name = 'clojurescript',
           src=[],
           deps = ['[org.clojure/clojurescript "1.7.228"]'])
