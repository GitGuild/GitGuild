#!/bin/sh
ORIG_USER=$( git config user.name )
ORIG_EMAIL=$( git config user.email )
ORIG_SIGNINGKEY=$( git config user.signingkey )
export USE_GITOLITE=false
export USE_GITHUB=false

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
  if [ ! -d "$HOME"/repositories/"$ORIG_USER".git ]; then
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

teardown() {
  # move any ssh keys back to original locations
  if [ -f "$HOME/.ssh/$ORIG_USER.pub.bak" ]; then
    mv "$HOME/.ssh/$ORIG_USER.bak" "$HOME/.ssh/$ORIG_USER"
    mv "$HOME/.ssh/$ORIG_USER.pub.bak" "$HOME/.ssh/$ORIG_USER.pub"
  fi
  #if [ -f "$HOME/.ssh/id_rsa.pub.bak" ]; then
  #  mv "$HOME/.ssh/id_rsa.bak" "$HOME/.ssh/id_rsa"
  #  mv "$HOME/.ssh/id_rsa.pub.bak" "$HOME/.ssh/id_rsa.pub"
  #fi
  git config --global --add user.name $ORIG_USER
  git config --global --add user.email $ORIG_EMAIL
  git config --global --add user.signingkey $ORIG_SIGNINGKEY
}

setup() {
  # unset user to simulate unconfigured git
  git config --global --unset-all user.name
  git config --global --unset-all user.email
  git config --global --unset-all user.signingkey
  # clean up any existing installation
  make -s uninstall
  # back up ssh keys and move out of proper place
  if [ -f "$HOME/.ssh/$ORIG_USER.pub" ]; then
    mv "$HOME/.ssh/$ORIG_USER" "$HOME/.ssh/$ORIG_USER.bak"
    mv "$HOME/.ssh/$ORIG_USER.pub" "$HOME/.ssh/$ORIG_USER.pub.bak"
  fi
  #if [ -f "$HOME/.ssh/id_rsa.pub" ]; then
  #  mv "$HOME/.ssh/id_rsa" "$HOME/.ssh/id_rsa.bak"
  #  mv "$HOME/.ssh/id_rsa.pub" "$HOME/.ssh/id_rsa.pub.bak"
  #fi
}

__main() {
  # back to base dir
  if [ ! -f "./configure" ]; then
    cd ../
  fi
  # basic configure, no options, only good gpg key
  setup
  git config --global --add user.signingkey $ORIG_SIGNINGKEY
  #echo "if you get to the gpg --gen-key prompt, type ctrl+d"
  mess=$( echo "$ORIG_USER""_bad\n""$ORIG_EMAIL""_bad\n" | ./configure )
  if [ "$( echo "$mess" | grep 'WARNING: Git user.name not configured.' )" = "" ]; then
    fail "git user configuration prompt not triggered"
  elif [ "$( echo "$mess" | grep 'WARNING: Git user.email not configured.' )" = "" ]; then
    fail "git user configuration prompt not triggered"
#  elif [ "$( echo "$mess" | grep 'guessing' )" != "" ]; then
#    fail "git user configuration guessing unexpectedly triggered"
  elif [ "$( echo $mess | grep ".*Operating as user.*$ORIG_USER_bad.*$ORIG_EMAIL_bad.*$ORIG_SIGNINGKEY" )" = "" ]; then
    fail "git user configuration not successful"
  fi
  teardown
  echo "basic configuration, no options, only good gpg key passed."

  # basic configure, no options, in AUTHORS, only known username
  setup
  mess=$( echo "$ORIG_USER\n" | ./configure )
  if [ "$( echo "$mess" | grep 'WARNING: Git user.name not configured.' )" = "" ]; then
    fail "git user configuration prompt not triggered"
  elif [ "$( echo "$mess" | grep 'WARNING: Git user.email not configured.' )" = "" ]; then
    fail "git user configuration prompt not triggered"
  elif [ "$( echo "$mess" | grep 'guessing' )" = "" ]; then
    fail "git user configuration guessing not triggered"
  elif [ "$( echo "$mess" |  grep ".*Operating as user.*"$ORIG_USER".*"$ORIG_EMAIL".*"$ORIG_SIGNINGKEY"" )" = "" ]; then
    fail "git user configuration guessing not successful"
  fi
  teardown
  echo "basic configuration known username in AUTHORS passed."

  # basic install, use gitolite
  USE_GITOLITE=true
  setup
  git config --global --add user.name "$ORIG_USER"
  $( ./configure )
  make -s "install"
  basics_exist
  gitolite_installed
  oksh_installed
  personal_guild_initialized
  teardown
  echo "basic install, use gitolite passed"

  # basic install, use gitolite and github
  USE_GITHUB=true
  setup
  git config --global --add user.name "$ORIG_USER"
  _=$( ./configure )
  make -s "install"
  basics_exist
  gitolite_installed
  oksh_installed
  personal_guild_initialized
  teardown
  echo "basic install, use gitolite and github passed"
}

__main "$@"

