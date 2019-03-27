[< BACK](../README.md)

# Git Cheatsheet
DISCLAIMER: Command descriptions are ***heavily simplified***. 

## Info commands
Walay mag change sa files, commits, history, etc. pag gamit ani na commands. So use them freely and frequently.

|||
| --- | --- |
| `git status` | show files added/not added for next commit |
| `git status -s` | show status in short/compact form |
| `git log` | show commit history for current branch (add `--all` for all branches) |
| `git log --oneline --graph --decorate` | pretty print commit history  (add `--all` for all branches) |


## Local Repo
These commands only changes your local repo(files sa imong computer). Dili ma propagate ang changes sa github.

|||
| --- | --- |
| `git add -A` | add *all* file changes to next commit |
| `git commit -m "enter message here"` | commit all *added* changes with message |
| `git reset --HARD` | reset all changes |
| `git stash` | save local changes temporarily (files will revert back to original state) |
| `git stash pop` | re-apply stashed changes |

## Uploading/Downloading changes to/from github
Use your judgment for when to upload local changes. You don't have to upload changes every commit. 

|||
| --- | --- |
| `git fetch` | check for new updates from github without changing files |
| `git pull` | check for new updates from github *and* update files as well |
| `git push` | upload all local changes to github |


## Branch

|||
| --- | --- |
| `git branch` | list branches on your local repo |
| `git branch -a` | list *all* branches including sa github |
| `git checkout <branch_name>` | switch working branch |
| `git checkout -b <new_branch_name>` | create new branch (by branching from ***current*** working branch) |
| `git merge <branch_name>` | merge changes from `<branch_name>` to  ***current*** working branch |

## Others
Useful and commands pero medyo complicated. Kamo na search ani.

1. `git diff` - show differences between files line-by-line, branches, commits, etc.
   
   Akong natry: show differences between current branch and develop
   ```
   $ git diff develop --stat
    README.md                           | 43 +++++------------------------------
    _config.yml                         |  1 +
    docs/cloning.md                     | 37 ++++++++++++++++++++++++++++++
    docs/git_cheatsheet.md              | 45 +++++++++++++++++++++++++++++++++++++
    learn/README.md => docs/learning.md |  2 ++
    5 files changed, 91 insertions(+), 37 deletions(-)
    ```
