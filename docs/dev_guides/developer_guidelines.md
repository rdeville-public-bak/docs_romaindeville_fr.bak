# Developers Guidelines

This document will describe main guidelines for developers who want to
contribute to this repo. It rely on other documentation in this repo for which
link will be provided when needed.

The aim of this document is to describe how to help development of this project,
how to properly contribute and provide a link the style code used in this repo.

Most of this guidelines are not mandatory, its mainly to make code and
documentation more homogenous and help people to understand what is done in the
code.

## Workflow

The repo use git flow branching model, for more information see:

  * [A successful git branching model][git_branching_model].

To help you following this branching model, you can use `git flow` command. To
install this command, see:

  * [git flow][git_flow] to install package
  * [git flow cheatsheet][git_flow_cheatsheet]

Branches should start with prefix `feature-`, `bugfix-`, `release-` and
`hotfix-`.

Except for the main developers `master`, `develop` and `release-` branches are
protected. You will not be able to push directly on these branches.

For now, main developpers are:

  * [ rdeville]({{ git_platform.url }}{{ git_platform.username }})

## Tutorials

Let us do a little tutorial to apply this workflow.

This tutorial will follow the following workflow steps:

  1. Fork this repo (Optional),
  2. Setup your working environment,
  3. Create your working branch,
  4. Work on this branch,
  5. Ensure your modification are documented and pass the tests,
  6. Once finished and tested, your can merge this branch to your branch,
  7. Prepare your merge request,
  8. Propose a merge request on the main repo.

### 1. Fork this repo (Optional)

This step is optional, as you can work directly on the main repo by creating
branch corresponding on what you are working on like `feature-*` or `bugfix-*`.
But it is the prefered method if you want to keep your configuration and be free
to name the branch whatever you want.

### 2. Setup your working environment

Depending of the type of repos, you might need to install different working
environment. This setup will mainly depend on the base langage of repository,
i.e. python based, ruby based, etc.

Do not hesitate to take a look to the script `.direnv/bin/activate_direnv` which
I use with by `direnv` to automate the setup of my working environments. The
location of the folder `.direnv` depends on the repos type:

* Usually at the root of "standard" git repo.
* Usually in `.config/<repo_name>` for vcsh repo.


??? hint "Hint: Usage of <code>direnv</code> is strongly recommended"

    [`direnv`][direnv] is not a required dependency but it is strongly
    recommended to use it.

    As many tools used by repos required environment variables, we strongly
    recommend using [direnv][direnv] to automate loading of these environment
    variables.

    [`direnv`][direnv] is an extension for your shell. It augments existing
    shells with a new feature that can load and unload environment variables
    depending on the current directory.

    In other terms, if a script `.envrc` is present in a folder and allowed for
    `direnv`, it will automatically be executed when entering the folder. When
    leaving the folder any exported variables will be automatically unloaded.

    This will allow you to not really care about the setup of working
    environment as scripts run by [`direnv`][direnv] will setup it for you.

    If you want to use it, please refer to this short tutorial [Usage of
    Direnv][direnv_tutorial].

??? info "Python based repository "

    First, install the following external software which are required:

      - bash >= 5.0
      - python3 >= 3.8
      - pip3 (using python >= 3.8)
      - python3-venv (using python >= 3.8, or directly `python3.8-venv` for debian
        based distros)

    Then, you will need to clone the repo:
    ```bash
    # Clone with HTTPS
    git clone https://git.platform.tld/namespace/repo.git
    # Clone with SSH
    git clone git@git.platform.tld:namespace/repo.git
    ```

    Finally, you will need to install python required dependencies to be able to
    use scripts in the repo:

    ```bash
    # Assuming you are in the root of the repo or in ~/.config/<repo_name>
    # Create python virtual environment
    python3 -m venv .virtualenv
    # Activate the virtual environment
    source .virtualenv/bin/activate
    # Install python production required dependencies in the virtualenvironment
    pip3 install -r requirements.txt
    # Install python development required dependencies in the virtualenvironment
    pip3 install -r requirements.dev.txt
    ```

### 3. Create your working branch

In this exemple we will add a new documentation page, it is kind of a new
feature, so the new branch will be name `feature-doc-content-title`.

```bash
# Create the branch and directly go to it
git checkout -b feature-doc-content-title
```

**NOTE**: If it is a bufix, the branch name may be like
`bugfix-name-of-the-bug`, etc. This naming convention is only if you wish to
work directly on the main repo, you are free to name the branch whatever you
like on your own fork.

### 4. Work on this branch

Then, do the work you need to do on your branch.

  * If you want to write the documentation page and are new using mkdocs, a
    tutorials is provided to help you adding content to the documentation.

    See [Update documentation][update_documentation].

  * If you want to setup/modify the CI to automatically push the website, a
    tutorial is provided to help you learn how to do it.

    See [Update CI][update_ci].

### 5. Ensure your modification are documented and pass the tests

To ensure your modification are valid, i.e. pass the test. This will depend on
the language base of the repo.

??? info "Python based repo"
    For python based repo simply use the following command:

    ```bash
    # Assuming you are in the root of the repo or in .config/<repo_name>
    # and you setup python dev requirements
    tox
    ```

    This will automatically run the testing tools (also used in the CI) and will
    ensure the build of the documentation:

    * [tox][tox]: Setup python testing suite
    * [shellcheck][shellcheck]: Shell script analysis tools

    For more information, you can check following files:

    * pyproject.toml
    * .gitlab-ci.yaml

    This previously described files are usually:

    * In the root of the repo for "standard" git repo
    * In `.config/<repo_name>` for `vcsh` repo

### 6. Merge branch on your fork

This step is optional and only if you make a fork of the repo, otherwise, go
directly to the next section.

Now you have finish your work, you can merge this feature into your `develop` or
`master` branch (you are free of your branch management in your own fork).

```bash
# Go to your develop branch
git checkout develop
# Merge feature into develop
git merge feature-doc-content-title
```

!!! important
    If you did not make a fork of the repo, when merging your branch to `master`
    or `develop`, you will have no issues. But when pushing your modification,
    these modification will be rejected as branch `master` and `develop` are
    protected on the main repo.

### 7. Prepare your merge request

Before proposing your merge request, ensure that :

  - Your your configuration files are not versionned

### 8. Propose a merge request on the main repo

Finally, you can propose a merge request.

#### If you make a fork of the main repo

To do so, if your fork is not on [{{ git_platform.name }}][gitlab], you may need to
push it on this platform.

To do so, create an account on [{{ git_platform.name }}][gitlab] or ask your
colleague how to do so as [{{ git_platform.name }}][gitlab] may not allow open
registration.

Then, create an empty repo on [{{ git_platform.name }}][gitlab] and create the
remote on your local folder and push your repo:

```bash
git remote add upstream-fork {{ git_platform.url }}/<USER>/<REPO_NAME>
# To be sure, push all your branch, or if you know, push only needed branches
git push upstream-fork --all
```

Then propose your merge request on the branch `master` of the main repo. **DO
NOT FORGET TO BE EXPLICIT ON YOU MERGE REQUEST**

#### If you work directly on a branch on the main repo

You can direclty propose your merge request on the branch `master` of the main
repo. **DO NOT FORGET TO BE EXPLICIT ON YOU MERGE REQUEST**

[tox]: https://tox.readthedocs.io/en/latest/
[mkdocs]: https://pypi.org/project/mkdocs/
[shellcheck]: https://github.com/koalaman/shellcheck
[direnv]: https://direnv.net/

[gitlab]: {{ git_platform.url }}

[git_branching_model]: https://nvie.com/posts/a-successful-git-branching-model/
[git_flow]: https://github.com/nvie/gitflow/wiki/Installation
[git_flow_cheatsheet]: https://danielkummer.github.io/git-flow-cheatsheet/

[direnv_tutorial]: tutorials/usage_of_direnv.md
[update_documentation]: tutorials/update_documentation.md
[update_ci]: tutorials/update_ci.md
