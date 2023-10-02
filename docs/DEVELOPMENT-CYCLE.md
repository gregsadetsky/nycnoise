## development cycle i.e. how to contribute code

- we'll use the established model described [here](https://nvie.com/posts/a-successful-git-branching-model/)
  - TLDR: everyone works in feature branches, those branches get merged to `dev`, and then we merge from there to `main` when we're ready to release

### step by step

- create a new branch based on `dev` for your feature or fix (e.g. make sure you're on `dev` and have git pulled, then `git checkout -b my-fix`)
- keep branch up to date with dev (e.g. `git pull origin dev`)
- push code / branch to repo (e.g. `git push origin my-fix`)
- open PR on github
- go through a code review
- code gets merged to `dev`
- delete branch
- repeat
