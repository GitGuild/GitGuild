#!/bin/sh
. "./helpers.sh"

teardown() {
  rm -fR "$HOME/gitguild/tmp"
}

setup() {
  rm -fR "$HOME/gitguild/tmp"
  cp -fR "$HOME/gitguild/$USER_NAME" "$HOME/gitguild/tmp"
  cd "$HOME/gitguild/tmp"
  if [ "$(pwd)" = "$HOME/gitguild/tmp" ]; then
    git reset --hard HEAD || exit 1
  else
    fail "Could not create test env at $HOME/gitguild/tmp"
    exit 1
  fi
}

__main() {
  setup
  # the last transaction should be valid. check to make sure...
  gitguild tx check
  if [ "$?" != 0 ]; then
    fail "Last transaction was not valid. Cannot run tx tests."
    teardown
    exit 1
  fi
  echo "OK, ready for tests"
}

__main "$@"

