# Transaction Templates

Usually shortened as "templates," all gitguild transacions must correspond to one or more patch files describing the changes being made. These patterns have been pre-approved by the guild governing the transaction, with set XP voting rules for acceptance.

### Diff & Patch

The core engine of gitguild's template system is GNU's [diffutils](https://www.gnu.org/software/diffutils/). Users of git are no doubt already familiar with `diff`, and maybe even `patch`. Gitguild uses these to create (diff), apply (patch), and check (reverse patch) templates.

Lets look at a simple example: adding a new member to the `AUTHORS` file. This template is in `template/add_member_authors.patch`.

```
diff -cr -N -x .git -x '*.patch' /old//AUTHORS /new//AUTHORS
*** /old//AUTHORS	1969-12-31 19:00:00.000000000 -0500
--- /new//AUTHORS	2016-12-23 11:00:15.859360525 -0500
***************
*** 0 ****
--- 1 ----
+ <<< user_name >>> <<< user_email >>> <<< user_signingkey >>>
```

The patch shows one line being added to the AUTHORS file. It could be run in reverse to show one line being deleted from the AUTHORS file.

### Parameters

To transform a strict patch into a more flexible template, add parameters. Gitguild template parameters are surrounded by triple tri-angle brackets. i.e. `<<< param_name >>>`. As far as the developers can tell, this is a previously unused format, which will avoid collisions with any documents under revision control.

At runtime, these parameters will be replaced by the appropriate values from the context of the transaction. For instance, `<<< user_name >>>` would be the current user's name when creating a transaction using a patch, but would be the committer's name when checking said transaction.

```
$ head -n 1 AUTHORS
isysd ira@gitguild.com 5C3586F6
```

### Creating Templates

To create a template, start with a git repo representing your starting state. Commit this starting state so that there are no uncommitted new or modified files.

Now modify make any file changes you wish to be templated. In generating the example above, the AUTHORS file was manually edited, and the parameterized line was added.

```
$ echo "<<< user_name >>> <<< user_email >>> <<< user_signingkey >>>" >> AUTHORS
```

If you run `git status`, it should now show one or more changes against your starting commit. These can be added or untracked, it doesn't matter. The next step is to run `gitguild template create`.

```
$ gitguild template create
diff -cr -N -x .git -x '*.patch' /old//AUTHORS /new//AUTHORS
*** /old//AUTHORS	1969-12-31 19:00:00.000000000 -0500
--- /new//AUTHORS	2016-12-23 11:00:15.859360525 -0500
***************
*** 0 ****
--- 1 ----
+ <<< user_name >>> <<< user_email >>> <<< user_signingkey >>>
```

The patch was printed to stdout for you to review. If it looks good, route the output into a file, like so.
  
```
$ gitguild template create > ~/gitguild/gitguild/template/add_member_authors.patch
```

Assuming the edits were made in parameterized fashion, and no new parameters were introduced, your template is now ready to run. Congratulations!
