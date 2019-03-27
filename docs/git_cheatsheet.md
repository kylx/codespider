# Git Cheatsheet

## Info commands
Walay magchange sa files, commits, history, etc. pag gamit ani na commands. So use them alot.

|||
| --- | --- |
| `git status` | show files added/not added for next commit |
| `git status -s` | show status in compact form |
| `git log` | show commit history for current branch (add `--all` for all branches) |
| `git log --oneline --graph --decorate` | pretty print commit history  (add `--all` for all branches) |


## Local Repo
These commands only changes your local repo(files sa imong computer). Dili ma propagate ang changes sa github.

|||
| --- | --- |
| `git add -a` | add *all* file changes to next commit |
