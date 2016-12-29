#!/bin/sh
. "./helpers.sh"
export USE_GITOLITE=false
export USE_GITHUB=false

teardown() {
  # move any ssh keys back to original locations
  if [ -f "$HOME/.ssh/$USER_NAME.pub.bak" ]; then
    mv "$HOME/.ssh/$USER_NAME.bak" "$HOME/.ssh/$USER_NAME"
    mv "$HOME/.ssh/$USER_NAME.pub.bak" "$HOME/.ssh/$USER_NAME.pub"
  fi
  #if [ -f "$HOME/.ssh/id_rsa.pub.bak" ]; then
  #  mv "$HOME/.ssh/id_rsa.bak" "$HOME/.ssh/id_rsa"
  #  mv "$HOME/.ssh/id_rsa.pub.bak" "$HOME/.ssh/id_rsa.pub"
  #fi
  git config --global --add user.name "$USER_NAME"
  git config --global --add user.email "$USER_EMAIL"
  git config --global --add user.signingkey "$USER_SIGNINGKEY"
}

setup() {
  # unset user to simulate unconfigured git
  git config --global --unset-all user.name
  git config --global --unset-all user.email
  git config --global --unset-all user.signingkey
  # clean up any existing installation
  make -s uninstall
  # back up ssh keys and move out of proper place
  if [ -f "$HOME/.ssh/$USER_NAME.pub" ]; then
    mv "$HOME/.ssh/$USER_NAME" "$HOME/.ssh/$USER_NAME.bak"
    mv "$HOME/.ssh/$USER_NAME.pub" "$HOME/.ssh/$USER_NAME.pub.bak"
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
  git config --global --add user.signingkey "$USER_SIGNINGKEY"
  #echo "if you get to the gpg --gen-key prompt, type ctrl+d"
  # shellcheck disable=SC2028
  mess=$( echo "$USER_NAME""_bad\n""$USER_EMAIL""_bad\n" | ./configure )
  if [ "$( echo "$mess" | grep 'WARNING: Git user.name not configured.' )" = "" ]; then
    fail "git user configuration prompt not triggered"
  elif [ "$( echo "$mess" | grep 'WARNING: Git user.email not configured.' )" = "" ]; then
    fail "git user configuration prompt not triggered"
#  elif [ "$( echo "$mess" | grep 'guessing' )" != "" ]; then
#    fail "git user configuration guessing unexpectedly triggered"
  elif [ "$( echo "$mess" | grep ".*Operating as user.*$USER_NAME_bad.*$USER_EMAIL_bad.*$USER_SIGNINGKEY" )" = "" ]; then
    fail "git user configuration not successful"
  fi
  teardown
  echo "basic configuration, no options, only good gpg key passed."

  # basic configure, no options, in AUTHORS, only known username
  setup
  mess=$( echo "$USER_NAME" | ./configure )
  if [ "$( echo "$mess" | grep 'WARNING: Git user.name not configured.' )" = "" ]; then
    fail "git user configuration prompt not triggered"
  elif [ "$( echo "$mess" | grep 'WARNING: Git user.email not configured.' )" = "" ]; then
    fail "git user configuration prompt not triggered"
  elif [ "$( echo "$mess" | grep 'guessing' )" = "" ]; then
    fail "git user configuration guessing not triggered"
  elif [ "$( echo "$mess" |  grep ".*Operating as user.*$USER_NAME.*$USER_EMAIL.*$USER_SIGNINGKEY" )" = "" ]; then
    fail "git user configuration guessing not successful"
  fi
  teardown
  echo "basic configuration known username in AUTHORS passed."

  # basic install, use gitolite
  USE_GITOLITE=true
  setup
  git config --global --add user.name "$USER_NAME"
  _=$( ./configure )
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
  git config --global --add user.name "$USER_NAME"
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

