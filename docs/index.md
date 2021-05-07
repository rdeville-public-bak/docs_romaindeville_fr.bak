---
hide:
  - navigation # Hide navigation pane
  - toc        # Hide table of contents
---

{% set curr_repo=subs("docs_romaindeville_fr") %}

<!-- BEGIN MKDOCS TEMPLATE -->
<!--
WARNING, DO NOT UPDATE CONTENT BETWEEN MKDOCS TEMPLATE TAG !
Modified content will be overwritten when updating
-->

<div align="center">

  <!-- Project Title -->
  <a href="{{ git_platform.url }}{{ curr_repo.repo_path_with_namespace }}">
    <img src="{{ curr_repo.logo }}" width="200px">
    <h1>{{ curr_repo.name }}</h1>
  </a>

<hr>

{{ to_html(curr_repo.desc) }}

<hr>

  <b>
IMPORTANT !<br>

Main repo is on
<a href="{{ git_platform.url }}{{ curr_repo.git_slug_with_namespace }}">
  {{ git_platform.name }} - {{ curr_repo.git_name_with_namespace }}</a>.<br>
On other online git platforms, they are just mirrors of the main repo.<br>
Any issues, pull/merge requests, etc., might not be considered on those other
platforms.
  </b>

</div>

--------------------------------------------------------------------------------

<!-- END MKDOCS TEMPLATE -->

{% for i_section in subrepo %}
# {{ subrepo[i_section]["nav_entry"] }}

| Name | Description | Repo |
|-----| ----| ----|
{%- for i_repo in subrepo[i_section]["external"] %}
{%-  set curr_repo = subs(i_repo.name) %}
{%-  set name = curr_repo.name %}
{%-  set logo = curr_repo.logo | replace('assets','latest/assets') %}
{%-  set desc = curr_repo.desc %}
{%-  set url = i_repo.online_url %}
{%-  set git_platform_info = git_platform.logo ~ " " ~ git_platform.name  %}
| [![{{ name }}]({{ logo | replace('assets','latest/assets')}}){.logo_repo} {{ name }}]({{ url }}) | {{ to_html(desc) }} | [{{ git_platform_info }}]({{ online_url }}) |
{%- endfor %}
{% endfor %}


