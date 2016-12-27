#!/bin/sh
export USER_NAME=$( git config user.name )
export USER_EMAIL=$( git config user.email )
export USER_SIGNINGKEY=$( git config user.signingkey )

# $1 failure message
fail() {
  echo "FAIL: $1" 1>&2
  teardown
  exit 1
}

basics_exist() {
  if [ ! -d "$HOME/gitguild" ]; then
    fail "$HOME/gitguild does not exist"
  elif [ ! -d "$HOME/gitguild/$USER_NAME" ]; then
    fail "$HOME/gitguild/$USER_NAME"
  elif [ ! -d "$HOME"/gitguild/gitguild ]; then
    fail "$HOME/gitguild/gitguild does not exist"
  fi
  wpath=$( which gitguild )
  if [ "$wpath" = "" ]; then
    fail "gitguild not found in PATH"
  fi
}

gitolite_installed() {
  wpath=$( which gitolite )
  if [ "$wpath" = "" ] && [ "$USE_GITOLITE" = "true" ]; then
    fail "gitolite not found in PATH"
  elif [ "$wpath" != "" ] && [ "$USE_GITOLITE" = "false" ]; then
    fail "gitolite unexpectedly found in PATH"
  fi
  if [ ! -d "$HOME"/repositories ] && [ "$USE_GITOLITE" = "true" ]; then
    fail "$HOME/repositories not found"
  elif [ -d "$HOME"/repositories ] && [ "$USE_GITOLITE" = "false" ]; then
    fail "$HOME/repositories unexpectedly exists"
  fi
  if [ -d "$HOME"/repositories/gitolite-admin.git ]; then
    fail "$HOME/repositories/gitolite-admin.git unexpectedly exists"
  fi
  if [ ! -d "$HOME/repositories/$USER_NAME.git" ]; then
    fail "$HOME/repositories/$USER_NAME.git not found"
  fi
}

oksh_installed() {
  wpath=$( which ok.sh )
  if [ "$wpath" = "" ] && [ "$USE_GITHUB" = "true" ]; then
    fail "ok.sh not found in PATH"
  elif [ "$wpath" != "" ] && [ "$USE_GITHUB" = "false" ]; then
    fail "ok.sh unexpectedly found in PATH"
  fi
  if [ ! -d "$HOME"/gitguild/ok.sh ] && [ "$USE_GITHUB" = "true" ]; then
    fail "$HOME/gitguild/ok.sh not found"
  elif [ -d "$HOME"/gitguild/ok.sh ] && [ "$USE_GITHUB" = "false" ]; then
    fail "$HOME/gitguild/ok.sh unexpectedly exists"
  fi
}

personal_guild_initialized() {
  if [ ! -d "$HOME/gitguild/$USER_NAME/ledger" ]; then
    fail "$HOME/gitguild/$USER_NAME/ledger not found"
  elif [ ! -d "$HOME/gitguild/$USER_NAME/conf" ]; then
    fail "$HOME/gitguild/$USER_NAME/conf not found"
  elif [ ! -d "$HOME/gitguild/$USER_NAME/keydir" ]; then
    fail "$HOME/gitguild/$USER_NAME/keydir not found"
  elif [ ! -f "$HOME/gitguild/$USER_NAME/keydir/$USER_NAME.pub" ]; then
    fail "$HOME/gitguild/$USER_NAME/keydir/$USER_NAME.pub not found"
  elif [ ! -f "$HOME/gitguild/$USER_NAME/AUTHORS" ]; then
    fail "$HOME/gitguild/$USER_NAME/AUTHORS not found"
  elif [ ! -f "$HOME/gitguild/$USER_NAME/GUILD" ]; then
    fail "$HOME/gitguild/$USER_NAME/GUILD not found"
  elif [ ! -f "$HOME/gitguild/$USER_NAME/VERSION" ]; then
    fail "$HOME/gitguild/$USER_NAME/VERSION not found"
  elif [ ! -f "$HOME/gitguild/$USER_NAME/CONTRIBUTING.md" ]; then
    fail "$HOME/gitguild/$USER_NAME/CONTRIBUTING.md not found"
  elif [ ! -f "$HOME/gitguild/$USER_NAME/CHANGELOG.md" ]; then
    fail "$HOME/gitguild/$USER_NAME/CHANGELOG.md not found"
  fi
}

