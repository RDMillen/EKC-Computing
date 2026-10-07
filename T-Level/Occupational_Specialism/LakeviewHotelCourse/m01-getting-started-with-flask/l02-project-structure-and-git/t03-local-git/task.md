# Version control without GitHub

Git works completely on your own computer. GitHub and GitLab are just places to keep a shared copy.
You can use all of the following with no account and no internet connection.

## The basic cycle
```
git init                         # start tracking this folder
git status                       # what has changed?
git add app.py views.py          # stage files for the next snapshot
git commit -m "Add home route"   # save the snapshot with a message
git log --oneline                # list your snapshots
git diff                         # see what changed since the last commit
```
In PyCharm you can do the same from Git | Create Git Repository and the Commit tool window.

## Good habits
- Commit small, working steps: one commit per idea.
- Write messages that say what changed: `Add collision check for edits`, not `stuff`.
- Add a `.gitignore` so you do not commit your virtual environment, caches or database.

## Branches
Newer versions of Git call the first branch `main`; older versions call it `master`. Run `git branch` to see which
yours uses, and use that name wherever you see `main` below.
```
git switch -c collision-check    # new branch for a feature
...work and commit...
git switch main
git merge collision-check
```

## Optional: practise "pushing" without GitHub
A folder can act as the shared remote:
```
git init --bare ../hotel-remote.git
git remote add origin ../hotel-remote.git
git push -u origin main
```

## Task
Do this in your own hotel project (the separate PyCharm project described in task 1.1.1), not in this course:
1. Create a repository and a `.gitignore`.
2. Make at least three commits with meaningful messages.
3. Paste the output of `git log --oneline` into `GIT_NOTES.md`.
