## development cycle i.e. how to contribute code

### step by step

- please first fork this repo
- git clone your fork to your computer
- specify a new remote upstream repository:

```bash
git remote add upstream https://github.com/gregsadetsky/nycnoise.git
```

- you can check if it was succesful with: `git remote -v`
- then fetch && merge to update your project: `git pull upstream/dev`

- create a new branch based on `dev` for your feature or fix (e.g. make sure you're on `dev` and have git pulled from upstream, then `git checkout -b my-fix`)
- keep branch up to date with the upstream dev
- push code / branch to your repo (e.g. `git push origin my-fix`)
- open a PR on github
- go through the code review
- code gets merged to the upstream `dev`
- delete the branch
- repeat

---

- some instructions from https://stackoverflow.com/a/39822102 thanks!
- also see https://nvie.com/posts/a-successful-git-branching-model/
