# Contributing

Feedback and contributions are very welcome!

## General information


### Open Source License (MIT)

All (new) contributed material must be released under the [MIT license](./LICENSE).
All new contributed material that is not executable, including all text when not executed, is also released under the [Creative Commons Attribution 3.0 International (CC BY 3.0) license](https://creativecommons.org/licenses/by/3.0/) or later.

## Vulnerability reporting (security issues)

If you find a significant vulnerability, or evidence of one,
please send an email to the security contacts that you have such
information, and we'll tell you the next steps.
For now, the security contacts are:
isysd <ira@gitguild.com>,
cindy-zimmerman <cindy@tigoctm.com>,
and d3brouille <robinson@gitguild.com>
(remove the -NOSPAM markers).  

Please use the PGP keys provided in the AUTHORS file to encrypt your message!

## Documentation changes

Most of the documentation is in "markdown" format.
All markdown files use the .md filename extension.

Where reasonable, limit yourself to Markdown
that will be accepted by different markdown processors
(e.g., what is specified by CommonMark or the original Markdown)
In practice we use
the version of Markdown implemented by GitHub when it renders .md files,
and you can use its extensions
(in particular, mark code snippets with the programming language used).
This version of markdown is sometimes called
[GitHub-flavored markdown](https://help.github.com/articles/github-flavored-markdown/).
In particular, blank lines separate paragraphs; newlines inside a paragraph
do *not* force a line break.
Beware - this is *not*
the same markdown algorithm used by GitHub when it renders
issue or pull comments; in those cases
[newlines in paragraph-like content are considered as real line breaks](https://help.github.com/articles/writing-on-github/);
unfortunately this other algorithm is *also* called
GitHub rendered markdown.
(Yes, it'd be better if there were standard different names
for different things.)

The style is basically that enforced by the "markdownlint" tool.
Don't use tab characters, avoid "bare" URLs (in a hypertext link, the
link text and URL should be on the same line), and try to limit
lines to 80 characters (but ignore the 80-character limit if that would
create bare URLs).
Using the "rake markdownlint" or "rake" command
(described below) implemented in the development
environment can detect some problems in the markdown.
That said, if you don't know how to install the development environment,
don't worry - we'd rather have your proposals, even if you don't know how to
check them that way.

Do not use trailing two spaces for line breaks, since these cannot be
seen and may be silently removed by some tools.
Instead, use <tt>&lt;br&nbsp;/&gt;</tt> (an HTML break).

## Code changes

##### Copyright

This file adapted from the Linux Foundation's Core Infrastructure Initiative's [CONTRIBUTING.md](https://github.com/linuxfoundation/cii-best-practices-badge/blob/master/CONTRIBUTING.md).
