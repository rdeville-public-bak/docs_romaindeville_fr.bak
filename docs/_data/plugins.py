#!/usr/bin/env python3
"""
Set of method for mkdocs-macros which also update nav entry to dynamically
support subrepo with mkdocs monorepo plugin.
"""

# pylint: disable=R0801

# JSON encoder and decoder
# https://docs.python.org/3/library/json.html
import json

# Logging facility
# https://docs.python.org/3/library/logging.html
import logging

# Miscellaneous operating system interfaces
# https://docs.python.org/3/library/os.html
import os

# Regular expression operations
# https://docs.python.org/3/library/re.html
import re

# High-level file operations
# https://docs.python.org/3/library/shutil.html
import shutil

# System-specific parameters and functions
# https://docs.python.org/3/library/sys.html
import sys

# Time access and conversions
# https://docs.python.org/3/library/time.html
import time

# Python Git Library
# https://pypi.org/project/GitPython/
import git

# YAML parser and emitter for Python
# https://pypi.org/project/PyYAML/
import yaml

# Python lib/cli for JSON/YAML schema validation
# https://pypi.org/project/pykwalify/
from pykwalify.core import Core as yamlschema

# pylint: disable=W0105
# - W0105: String statement has no effect
LOG = logging.getLogger(__name__)
"""The logger facilty"""
ERR_CLR = "\033[31m"
"""String coloring error output in red"""
INFO_CLR = "\033[32m"
"""String coloring error output in green"""
RESET_CLR = "\033[0m"
"""String reseting coloring output"""


def add_internal_to_nav(
    env: dict,
    nav: dict,
    repo_dict: dict,
    repo_parent: list,
    nav_parent: list = None,
) -> None:
    """
    @rdeville TODO
    """
    if nav_parent:
        for i_nav in nav:
            if nav_parent[0] in i_nav:
                for i_key in i_nav:
                    add_internal_to_nav(
                        env,
                        i_nav[i_key],
                        repo_dict,
                        repo_parent,
                        nav_parent[1:],
                    )
    else:
        mkdocs_path = env.project_dir
        for i_parent in repo_parent:
            mkdocs_path = os.path.join(mkdocs_path, i_parent)
        mkdocs_path = os.path.join(mkdocs_path, repo_dict["name"])
        if "subpath" in repo_dict:
            mkdocs_path = os.path.join(mkdocs_path, repo_dict["subpath"])
        mkdocs_path = os.path.join(mkdocs_path, "mkdocs.yml")
        nav.append({repo_dict["nav_entry"]: f"!include {mkdocs_path}"})


def add_external_to_nav(
    env: dict, nav: dict, repo_dict: dict, repo_parent: list, nav_parent: list
) -> None:
    """
    @rdeville TODO
    """
    if nav_parent:
        for i_nav in nav:
            if nav_parent[0] in i_nav:
                for i_key in i_nav:
                    add_external_to_nav(
                        env,
                        i_nav[i_key],
                        repo_dict,
                        repo_parent,
                        nav_parent[1:],
                    )
    else:
        nav.append({repo_dict["nav_entry"]: repo_dict["online_url"]})


def add_nav_entry(nav: list, nav_parent: list = None) -> None:
    """
    @rdeville TODO
    """
    entry = dict()

    for i_nav in nav:
        if nav_parent[0] in i_nav:
            entry = i_nav

    if not entry:
        entry = {nav_parent[0]: []}
        nav.append(entry)

    if len(nav_parent[1:]) == 0:
        return
    add_nav_entry(entry[nav_parent[0]], nav_parent[1:])


def update_nav(
    env: dict,
    repo_dict: dict,
    repo_parent: list = None,
    nav_parent: list = None,
    first_iteration=False,
) -> None:
    """
    @rdeville TODO
    """
    for i_key in repo_dict:
        if not nav_parent or first_iteration:
            nav_parent = list()

        if not repo_parent or first_iteration:
            repo_parent = list()

        if i_key == "nav_entry":
            nav_parent.append(repo_dict["nav_entry"])
        elif i_key == "internal":
            for i_repo in repo_dict["internal"]:
                add_nav_entry(env.conf["nav"], nav_parent)
                add_internal_to_nav(
                    env, env.conf["nav"], i_repo, repo_parent, nav_parent
                )
        elif i_key == "external":
            for i_repo in repo_dict["external"]:
                add_nav_entry(env.conf["nav"], nav_parent)
                add_external_to_nav(
                    env, env.conf["nav"], i_repo, repo_parent, nav_parent
                )
        else:
            repo_parent.append(i_key)
            update_nav(env, repo_dict[i_key], repo_parent, nav_parent)


def get_repo_slug(env, git_repo):
    """Compute the slug of the current repo and ensure repo dict is defined

    Compute the slug of the current repo based on the origin remote. If no remo,
    then will use the folder name.
    Then ensure the repo dictionary is defined in `docs/_data/`. If not, print
    an error and exit.

    Arguments:
        env: Mkdocs macro plugin environment dictionary.
        git_repo: Git python object of the current repo.
    """
    if git_repo.remotes:
        repo_slug = (
            git_repo.remotes.origin.url.rsplit("/")[-1]
            .split(".git")[0]
            .replace(".", "_")
        )
    else:
        repo_slug = os.path.basename(env.project_dir)

    if repo_slug not in env.variables:
        LOG.error(
            "%s[macros] - Dictionnary %s is not defined.%s",
            ERR_CLR,
            repo_slug,
            RESET_CLR,
        )
        LOG.error(
            "%s[macros] - Ensure you copy docs/_data/templates/repo.tpl.yaml "
            "to docs/_data/%s.yaml.%s",
            ERR_CLR,
            repo_slug,
            RESET_CLR,
        )
        LOG.error(
            "%s[macros] - And you setup dictionary %s in docs/_data/%s.yaml.%s",
            ERR_CLR,
            repo_slug,
            repo_slug,
            RESET_CLR,
        )
        sys.exit(1)

    env.variables["git"]["repo_slug"] = repo_slug
    return repo_slug


def set_site_name(env, repo_slug):
    """Update content of the `site_name` key in mkdocs.yml

    If `site_name` key is not defined in `mkdocs.yml` then look to
    `docs/_data/vars.yml`, if defined, else look to the the current repo
    dictionary to set value of `site_name`.

    Arguments:
        env: Mkdocs macro plugin environment dictionary.
        repo_slug: Repo slug or name of the repo folder.
    """
    if "site_name" not in env.conf or not env.conf["site_name"]:
        if "site_name" in env.variables:
            env.conf["site_name"] = env.variables["site_name"]
        else:
            env.conf["site_name"] = env.variables[repo_slug]["name"]


def set_site_desc(env, repo_slug):
    """Update content of the `site_desc` key in mkdocs.yml

    If `site_desc` key is not defined in `mkdocs.yml` then look to
    `docs/_data/vars.yml`, if defined, else look to the the current repo
    dictionary to set value of `site_desc`.

    Arguments:
        env: Mkdocs macro plugin environment dictionary.
        repo_slug: Repo slug or name of the repo folder.
    """
    if "site_desc" not in env.conf:
        if "site_desc" in env.variables:
            env.conf["site_desc"] = env.variables["site_desc"]
        else:
            env.conf["site_desc"] = env.variables[repo_slug]["desc"]


def set_site_url(env, repo_slug):
    """Update content of the `site_url` key in mkdocs.yml

    If `site_url` key is not defined in `mkdocs.yml` then look to
    `docs/_data/vars.yml`, if defined, else build value from `site_base_url` and
    the current repo dictionary.

    Arguments:
        env: Mkdocs macro plugin environment dictionary.
        repo_slug: Repo slug or name of the repo folder.
    """
    if "site_url" not in env.conf:
        if "site_url" in env.variables:
            env.conf["site_url"] = env.variables["site_url"]
        elif "site_base_url" in env.variables:
            site_url = (
                env.variables["site_base_url"]
                + env.variables[repo_slug]["url_slug_with_namespace"]
            )
            env.conf["site_url"] = site_url


def set_copyright(env, git_repo):
    """Update content of the `copyright` key in mkdocs.yml

    If `copyright` key is not defined in `mkdocs.yml` but is defined in
    `docs/_data/vars.yml`, this override the content of the default `copyright`
    key in `mkdocs.yml` with date based on the first commit of the repo.

    Arguments:
        env: Mkdocs macro plugin environment dictionary.
        git_repo: Git python object of the current repo.
    """
    if (
        "copyright" not in env.conf or not env.conf["copyright"]
    ) and "copyright" in env.variables:
        if git_repo.branches and git_repo.branches.master:
            first_date = git_repo.commit(
                git_repo.branches.master.log()[0].newhexsha
            ).committed_date
            first_year = time.strftime("%Y", time.gmtime(first_date))
        else:
            first_year = time.strftime("%Y", time.localtime())
        curr_year = time.strftime("%Y", time.localtime())

        env.conf["copyright"] = "Copyright &copy; {} - {} {}".format(
            first_year, curr_year, env.variables["copyright"]
        )


def set_repo_name(env, repo_slug):
    """Update content of the `repo_url` key in mkdocs.yml

    If `repo_url` key is defined in `docs/_data/vars.yml`, this override the
    content of the default `repo_url` key in `mkdocs.yml`. Else, update the
    repo_url based on the value of `git_platform` dictionary and the dictionary
    corresponding of the repo.

    Arguments:
        env: Mkdocs macro plugin environment dictionary.
        repo_slug: Repo slug or name of the repo folder.
    """

    if "repo_name" not in env.conf or not env.conf["repo_name"]:
        if "name" in env.variables[repo_slug]:
            if env.variables[repo_slug]["name"] == "!!git_platform":
                env.conf["repo_name"] = env.variables["git_platform"]["name"]
            else:
                env.conf["repo_name"] = env.variables[repo_slug]["name"]


def set_repo_url(env, repo_slug):
    """Update content of the `repo_url` key in mkdocs.yml

    If `repo_url` key is defined in `docs/_data/vars.yml`, this override the
    content of the default `repo_url` key in `mkdocs.yml`. Else, update the
    repo_url based on the value of `git_platform` dictionary and the dictionary
    corresponding of the repo.

    Arguments:
        env: Mkdocs macro plugin environment dictionary.
        repo_slug: Repo slug or name of the repo folder.
    """
    if "repo_url" not in env.conf or not env.conf["repo_url"]:
        if "repo_url" in env.variables:
            env.conf["repo_url"] = env.variables["repo_url"]
        elif "repo_url" in env.conf:
            env.conf["repo_url"] = "{}{}".format(
                env.variables["git_platform"]["url"],
                env.variables[repo_slug]["git_slug_with_namespace"],
            )


def update_theme(env, repo_slug):
    """Update content of the `theme` key in mkdocs.yml

    If `theme` key is defined in `docs/_data/vars.yml`, this override the
    content of the default `theme` key in `mkdocs.yml`.

    Arguments:
        env: Mkdocs macro plugin environment dictionary.
        repo_slug: Repo slug or name of the repo folder.
    """
    if "theme" in env.variables:
        for i_key in env.variables["theme"]:
            env.conf["theme"][i_key] = env.variables["theme"][i_key]

    if "logo" not in env.conf["theme"] or not env.conf["theme"]["logo"]:
        if "logo" in env.variables[repo_slug]:
            env.conf["theme"]["logo"] = env.variables[repo_slug]["logo"]
        else:
            env.conf["theme"]["logo"] = os.path.join(
                "assets", "img", "meta", f"{repo_slug}_logo.png"
            )

    if not env.conf["theme"]["icon"]:
        env.conf["theme"]["icon"] = {}

    if "icon" not in env.conf["theme"] or not env.conf["theme"]["icon"]:
        env.conf["theme"]["icon"]["repo"] = env.variables["git_platform"][
            "icon"
        ]

    if "favicon" not in env.conf["theme"] or not env.conf["theme"]["favicon"]:
        if "favicon" in env.variables[repo_slug]:
            env.conf["theme"]["favicon"] = env.variables[repo_slug]["favicon"]
        elif "logo" in env.variables[repo_slug]:
            env.conf["theme"]["favicon"] = env.variables[repo_slug]["logo"]
    else:
        env.conf["theme"]["favicon"] = os.path.join(
            "assets", "img", "meta", f"{repo_slug}_logo.png"
        )


def set_config(env: dict) -> None:
    """Dynamically update mkdocs configuration

    Based on the repo slug (or folder name) load variables in
    `docs/_data/vars.yml` and update content of mkdocs.yml accordingly.

    Especially, if `docs/_data/subrepo.yaml` exists and define valid subrepod,
    dynamically add these subrepo to the `nav` key of the mkdocs.yml
    configuration.

    Arguments:
        env: Mkdocs macro plugin environment dictionary.
    """

    git_repo = git.Repo(search_parent_directories=True)
    repo_slug = get_repo_slug(env, git_repo)

    set_site_name(env, repo_slug)
    set_site_desc(env, repo_slug)
    set_site_url(env, repo_slug)
    set_copyright(env, git_repo)
    set_repo_name(env, repo_slug)
    set_repo_url(env, repo_slug)
    update_theme(env, repo_slug)

    if "subrepo" in env.variables:
        if (
            env.variables["internal_subdoc"]
            and "monorepo" in env.conf["plugins"]
        ):
            env.conf["plugins"].pop("monorepo")
        else:
            update_nav(env, env.variables["subrepo"], first_iteration=True)


def load_yaml_file(path: str, filename: str) -> None:
    """Ensure a YAML file is valid again a schema and return its content

    Depending on the name of the YAML file, compare its content to a schema to
    validate its content. If content is not valid, an error will be raised.
    Otherwise, its content will be returned.

    Arguments:
        path: Base path where YAML files are.
        filename: Name of the YAML file to load.
    """
    source_file = os.path.join(path, filename)
    schema_file = os.path.join(path, "schema")
    data_type = ""

    if filename in ("subrepo.yaml", "subrepo.yml"):
        schema_file = os.path.join(schema_file, "subrepo.schema.yaml")
    elif filename in ("vars.yaml", "vars.yml"):
        schema_file = os.path.join(schema_file, "vars.schema.yaml")
    else:
        schema_file = os.path.join(schema_file, "repo.schema.yaml")
        data_type = "repo"

    schema = yamlschema(source_file=source_file, schema_files=[schema_file])
    schema.validate(raise_exception=True)
    return schema.source, data_type


def update_subrepo_logo_src(env:dict,curr_repo:dict,repo_name:str,subrepo_dict:dict, path:str,external:bool) -> None:
    logo_subpath = ""
    src_subpath = ""
    if external:
        logo_subpath = os.path.join(subrepo_dict["online_url"])

    src_subpath = os.path.join(path.replace(f"{env.project_dir}/",""),repo_name)

    if "logo" not in curr_repo:
        curr_repo["logo"] = os.path.join(logo_subpath, "assets", "img", "meta",f"{repo_name}_logo.png")
    if "src_path" in curr_repo:
        for i_src in curr_repo["src_path"]:
            i_src = os.path.join(src_subpath, i_src)
            env.conf["plugins"]["mkdocstrings"].config.data["handlers"][
                "python"
            ]["setup_commands"].append(f"sys.path.append('{i_src}')")


def update_subrepo_info(env: dict, subrepo_list: dict, path: str, external:bool = False) -> dict:
    """
    @rdeville TODO
    """
    return_dict = dict()
    for i_repo in subrepo_list:
        subrepo_root = os.path.join(path, i_repo["name"])

        if os.path.isdir(subrepo_root):
            print(
                f"{INFO_CLR}INFO [macros] - Pulling repo {i_repo['name']}{RESET_CLR}"
            )
            git_subrepo = git.Repo(subrepo_root)
            git_subrepo.remotes.origin.pull()
        else:
            print(
                f"{INFO_CLR}INFO [macros] - Cloning repo {i_repo['name']}{RESET_CLR}"
            )
            git.Repo.clone_from(i_repo["git_url"], subrepo_root)

        if "subpath" in i_repo:
            data_dir = os.path.join(
                subrepo_root, i_repo["subpath"], "docs", "_data"
            )
        else:
            data_dir = os.path.join(subrepo_root, "docs", "_data")

        data_file = os.path.join(data_dir, f"{i_repo['name']}.yaml")
        data, _ = load_yaml_file(data_dir, data_file)
        for i_repo_info in data:
            curr_repo = data[i_repo_info]
            update_subrepo_logo_src(env,curr_repo,i_repo_info,i_repo,path,external)
        return_dict.update(data)
    return return_dict


def update_subrepo(env: dict, subrepo_dict: dict, path: str, external:bool) -> dict:
    """
    @rdeville TODO
    """
    return_dict = dict()
    for i_key in subrepo_dict:
        if isinstance(subrepo_dict[i_key], list):
            if i_key == "external":
                external = True
            elif i_key == "internal":
                env.variables["internal_subdoc"] = True
            return_dict.update(
                update_subrepo_info(env, subrepo_dict[i_key], path,external)
            )
        elif i_key not in ["nav_entry"]:
            return_dict.update(
                update_subrepo(
                    env, subrepo_dict[i_key], os.path.join(path, i_key),external
                )
            )
    return return_dict


def update_logo_src_repo(env:dict,curr_repo:dict,repo_name:str,path:str=None) -> None:
    subpath = ""
    if path:
        subpath = os.path.join(path.replace(env.project_dir,""),repo_name)

    if "logo" not in curr_repo:
        curr_repo["logo"] = os.path.join(subpath, "assets", "img", "meta",f"{repo_name}_logo.png")
    if "src_path" in curr_repo:
        for i_src in curr_repo["src_path"]:
            i_src = os.path.join(subpath, i_src)
            env.conf["plugins"]["mkdocstrings"].config.data["handlers"][
                "python"
            ]["setup_commands"].append(f"sys.path.append('{i_src}')")



def load_var_file(env: dict) -> None:
    """Load variables files in docs/_data/ and variable of subrepo

    Load every yaml files in docs/_data/, if one of the file define a `subrepo`
    key, load every variables associated to subrepo.

    Arguments:
        env: Mkdocs macro plugin environment dictionary.
    """
    var_dir = os.path.join(env.project_dir, "docs", "_data")

    for i_file in os.listdir(var_dir):
        if i_file.endswith((".yml", ".yaml")):
            data, data_type = load_yaml_file(var_dir, i_file)
            for i_key in data:
                if data_type == "repo":
                    update_logo_src_repo(env,data[i_key],i_key)
                env.variables[i_key] = data[i_key]


def update_version(env: dict) -> None:
    """Update docs/versions.json if last commit has a tag

    Arguments:
        env: Mkdocs macro plugin environment dictionary.
    """
    if (
        "version" not in env.variables
        or "provider" not in env.variables["version"]
        or env.variables["version"]["provider"] != "mike"
    ):
        return
    git_repo = git.Repo(search_parent_directories=True)
    mike_version = list()
    last_major = 0
    last_minor = 0
    last_patch = 0
    for i_tag in git_repo.tags:
        i_tag = yaml.dump(i_tag.path)
        i_tag = re.sub(".*v", "", i_tag).split(".")
        major = int(i_tag[0])
        minor = int(i_tag[1])
        patch = int(i_tag[2])
        if major > last_major:
            mike_version.append(
                {
                    "version": "{}.{}".format(last_major, last_minor),
                    "title": "{}.{}.{}".format(
                        last_major, last_minor, last_patch
                    ),
                    "aliases": [],
                }
            )
            last_major = major
            last_minor = 0
        if minor > last_minor:
            mike_version.append(
                {
                    "version": "{}.{}".format(last_major, last_minor),
                    "title": "{}.{}.{}".format(
                        last_major, last_minor, last_patch
                    ),
                    "aliases": [],
                }
            )
            last_minor = minor
            last_patch = 0
        if patch > last_patch:
            last_patch = patch
    mike_version.append(
        {
            "version": "{}.{}".format(last_major, last_minor),
            "title": "{}.{}.{}".format(last_major, last_minor, last_patch),
            "aliases": ["latest"],
        }
    )
    mike_version.reverse()
    with open(
        os.path.join(env.project_dir, "docs", "versions.json"), "w"
    ) as version_file:
        json.dump(mike_version, version_file, indent=2)


def define_env(env: dict) -> None:
    # pylint: disable=C0301
    # - C0301: Line to long
    """
    This is the hook for defining variables, macros and filters

    - variables: the dictionary that contains the environment variables
    - macro: a decorator function, to declare a macro.

    See
    [https://mkdocs-macros-plugin.readthedocs.io/en/latest/](https://mkdocs-macros-plugin.readthedocs.io/en/latest/)

    Arguments:
        env: Mkdocs macro plugin environment dictionary.
    """

    load_var_file(env)

    if "subrepo" in env.variables:
        env.variables["internal_subdoc"] = False
        env.variables.update(
            update_subrepo(env, env.variables["subrepo"], env.project_dir, False)
        )

    set_config(env)

    update_version(env)

    @env.macro
    # pylint: disable=W0612
    # -  W0612: Unused variable (unused-variable)
    def subs(var: str) -> dict:
        """Return the content of the dictionary defined by var"""
        return env.variables[var]

    @env.macro
    # pylint: disable=W0612
    # -  W0612: Unused variable (unused-variable)
    def get_repo() -> dict:
        """Return the content of the dictionary of the current repo"""
        git_repo = git.Repo(search_parent_directories=True)
        return env.variables[get_repo_slug(env, git_repo)]


# -----------------------------------------------------------------------------
# VIM MODELINE
# vim: fdm=indent
# -----------------------------------------------------------------------------
