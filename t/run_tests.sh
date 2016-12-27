tests=$( find ./ -name "test_*.sh" )

execute_all() {
  for t in $tests; do
    $( t )
  done
}

execute_install() {
  echo "----------------This installation test is dangerous!--------------------"
  echo "It will wipe any local gitguild data, and also move around PGP and SSH keys! Are you sure you want to run it?"
  read readyono
  echo
  if [ "$( echo "$readyono" | grep '[yY].*' )" != "" ]; then
    . "./install_unsafe_test.sh"
  fi
}

case "$1" in
  install)
    execute_install
    ;;
  *)
    execute_all
esac
