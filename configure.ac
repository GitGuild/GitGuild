define(_CLIENT_VERSION_MAJOR, 0)
define(_CLIENT_VERSION_MINOR, 2)
define(_CLIENT_VERSION_REVISION, 2)
define(_CLIENT_VERSION_BUILD, 0)
define(_CLIENT_VERSION_IS_RELEASE, false)
define(_COPYRIGHT_YEAR, 2016)
define(_COPYRIGHT_HOLDERS,[The %s developers])
define(_COPYRIGHT_HOLDERS_SUBSTITUTION,[[AUTHORS]])
AC_INIT([GitGuild],[_CLIENT_VERSION_MAJOR._CLIENT_VERSION_MINOR._CLIENT_VERSION_REVISION],[https://github.com/gitguild/gitguild-cli/issues],[gitguild],[http://gitguild.com/])
dnl Automake init set-up and checks
AM_INIT_AUTOMAKE

dnl --disable-maintainer-mode can be used to bypass this.
AM_MAINTAINER_MODE([enable])
AC_CONFIG_FILES([Makefile])
AC_CONFIG_FILES([src/Makefile])
AC_CONFIG_FILES([src/check-sigs], [chmod +x src/check-sigs])
AC_CONFIG_FILES([src/archive-tx-ledger], [chmod +x src/archive-tx-ledger])
AC_CONFIG_FILES([src/gitguild], [chmod +x src/gitguild])

AC_PROG_CC
AC_PROG_CXX
AC_PROG_AWK
AC_PROG_GREP
AC_PROG_SED
AC_PROG_INSTALL
AC_CHECK_TOOLS(AR, [gar ar])
AC_CHECK_PROGS(TAR, [gtar tar])
AC_CHECK_PROGS(DIFF, [gnudiff gdiff diff])

dnl 
AC_PATH_TOOL(STRIP, strip)
AC_PATH_PROG(GNUPG, gpg)
AC_PATH_PROG(LEDGER, ledger,AC_MSG_ERROR(ledger missing))
AC_PATH_PROG([GIT], [git],AC_MSG_ERROR(git missing))
AC_PATH_PROG(GITOLITE, gitolite, '')

dnl AC_CHECK_FILES

dnl Enable gitolite-server
AC_ARG_ENABLE([gitolite-server],
    AS_HELP_STRING([--enable-gitolite-server],[enable detachable gitolite server component (default no)]),
    [enable_gitolite_server=$enableval],
[enable_gitolite_server=no])

dnl enable gitolite-server
AC_MSG_CHECKING([if gitolite-server should be enabled])
if test x$enable_gitolite_server != xno; then
  AC_MSG_RESULT(yes)
  AC_DEFINE_UNQUOTED([ENABLE_GITOLITE_SERVER],[1],[Define to 1 to enable gitolite server])

else
  AC_MSG_RESULT(no)
fi


AM_CONDITIONAL([ENABLE_GITOLITE_SERVER],[test x$enable_gitolite_server = xyes])

AC_DEFINE(CLIENT_VERSION_MAJOR, _CLIENT_VERSION_MAJOR, [Major version])
AC_DEFINE(CLIENT_VERSION_MINOR, _CLIENT_VERSION_MINOR, [Minor version])
AC_DEFINE(CLIENT_VERSION_REVISION, _CLIENT_VERSION_REVISION, [Build revision])
AC_DEFINE(CLIENT_VERSION_BUILD, _CLIENT_VERSION_BUILD, [Version Build])
AC_DEFINE(CLIENT_VERSION_IS_RELEASE, _CLIENT_VERSION_IS_RELEASE, [Version is release])
AC_DEFINE(COPYRIGHT_YEAR, _COPYRIGHT_YEAR, [Copyright year])
AC_DEFINE(COPYRIGHT_HOLDERS, "_COPYRIGHT_HOLDERS", [Copyright holder(s) before %s replacement])
AC_DEFINE(COPYRIGHT_HOLDERS_SUBSTITUTION, "_COPYRIGHT_HOLDERS_SUBSTITUTION", [Replacement for %s in copyright holders string])
define(_COPYRIGHT_HOLDERS_FINAL, [patsubst(_COPYRIGHT_HOLDERS, [%s], [_COPYRIGHT_HOLDERS_SUBSTITUTION])])
AC_DEFINE(COPYRIGHT_HOLDERS_FINAL, "_COPYRIGHT_HOLDERS_FINAL", [Copyright holder(s)])
AC_SUBST(CLIENT_VERSION_MAJOR, _CLIENT_VERSION_MAJOR)
AC_SUBST(CLIENT_VERSION_MINOR, _CLIENT_VERSION_MINOR)
AC_SUBST(CLIENT_VERSION_REVISION, _CLIENT_VERSION_REVISION)
AC_SUBST(CLIENT_VERSION_BUILD, _CLIENT_VERSION_BUILD)
AC_SUBST(CLIENT_VERSION_IS_RELEASE, _CLIENT_VERSION_IS_RELEASE)
AC_SUBST(COPYRIGHT_YEAR, _COPYRIGHT_YEAR)
AC_SUBST(COPYRIGHT_HOLDERS, "_COPYRIGHT_HOLDERS")
AC_SUBST(COPYRIGHT_HOLDERS_SUBSTITUTION, "_COPYRIGHT_HOLDERS_SUBSTITUTION")
AC_SUBST(COPYRIGHT_HOLDERS_FINAL, "_COPYRIGHT_HOLDERS_FINAL")

AC_OUTPUT

echo 
echo "Options used to compile and link:"
echo "  with gitolite server  = $enable_gitolite_server"
echo 

