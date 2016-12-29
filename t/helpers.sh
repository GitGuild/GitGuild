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
  elif [ ! -d "$HOME/gitguild/$ORIG_USER" ]; then
    fail "$HOME/gitguild/$ORIG_USER"
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
  if [ ! -d "$HOME/repositories/$ORIG_USER.git" ]; then
    fail "$HOME/repositories/$ORIG_USER.git not found"
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
  if [ ! -d "$HOME/gitguild/$ORIG_USER/ledger" ]; then
    fail "$HOME/gitguild/$ORIG_USER/ledger not found"
  elif [ ! -d "$HOME/gitguild/$ORIG_USER/conf" ]; then
    fail "$HOME/gitguild/$ORIG_USER/conf not found"
  elif [ ! -d "$HOME/gitguild/$ORIG_USER/keydir" ]; then
    fail "$HOME/gitguild/$ORIG_USER/keydir not found"
  elif [ ! -f "$HOME/gitguild/$ORIG_USER/keydir/$ORIG_USER.pub" ]; then
    fail "$HOME/gitguild/$ORIG_USER/keydir/$ORIG_USER.pub not found"
  elif [ ! -f "$HOME/gitguild/$ORIG_USER/AUTHORS" ]; then
    fail "$HOME/gitguild/$ORIG_USER/AUTHORS not found"
  elif [ ! -f "$HOME/gitguild/$ORIG_USER/GUILD" ]; then
    fail "$HOME/gitguild/$ORIG_USER/GUILD not found"
  elif [ ! -f "$HOME/gitguild/$ORIG_USER/VERSION" ]; then
    fail "$HOME/gitguild/$ORIG_USER/VERSION not found"
  elif [ ! -f "$HOME/gitguild/$ORIG_USER/CONTRIBUTING.md" ]; then
    fail "$HOME/gitguild/$ORIG_USER/CONTRIBUTING.md not found"
  elif [ ! -f "$HOME/gitguild/$ORIG_USER/CHANGELOG.md" ]; then
    fail "$HOME/gitguild/$ORIG_USER/CHANGELOG.md not found"
  fi
}

