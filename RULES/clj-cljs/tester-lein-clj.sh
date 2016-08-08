set -e

cd $1 && LEIN_ROOT=1 lein test
