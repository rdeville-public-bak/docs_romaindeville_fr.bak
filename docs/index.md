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
  <a href="{{ git_platform.url }}{{ curr_repo.git_slug_with_namespace }}">
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

<!-- END MKDOCS TEMPLATE -->


{%- for i_section in subrepo %}
{%-   set section_name = subrepo[i_section]['nav_entry'] %}
{%-   set section_info = subs(i_section) %}

{%-   if subs(i_section) %}
{%-     set section_logo = section_info.logo | replace("/","",1) %}
{%-     set section_desc = to_html(section_info.desc) %}
# [![{{section_name}}]({{section_logo}}){.logo_section} {{section_name}}][{{i_section}}]

{{ section_desc }}
{%-   else %}
# [{{ section_name }}][{{ i_section }}]
{%-   endif %}

{%-   if subrepo[i_section]["external"] or subrepo[i_section]["internal"] %}
| Name | Description | Repo |
|-----| ----| ----|
{%-     for i_repo in subrepo[i_section]["external"] %}
{%-       set curr_repo = subs(i_repo.name) %}
{%-       set name = curr_repo.name %}
{%-       set logo = curr_repo.logo | replace('assets','latest/assets') | replace('/','../',1) %}
{%-       set desc = to_html(curr_repo.desc) %}
{%-       set url = i_repo.online_url | replace('/','../',1) %}
{%-       set git_platform_info = git_platform.logo ~ " " ~ git_platform.name  %}
{%-       set git_repo_url = git_platform.url ~ curr_repo.git_slug_with_namespace %}
| [![{{name}}]({{logo}}){.logo_repo} {{name}}]({{url}}) | {{desc}} | [{{git_platform_info}}]({{git_repo_url}}) |
{%-     endfor %}
{%-     for i_repo in subrepo[i_section]["internal"] %}
{%-       set curr_repo = subs(i_repo.name) %}
{%-       set name = curr_repo.name %}
{%-       set logo = curr_repo.logo | replace('assets','latest/assets') | replace('/','../',1) %}
{%-       set desc = to_html(curr_repo.desc) %}
{%-       set url = i_repo.online_url | replace('/','../',1) %}
{%-       set git_platform_info = git_platform.logo ~ " " ~ git_platform.name  %}
{%-       set git_repo_url = git_platform.url ~ curr_repo.git_slug_with_namespace %}
| [![{{name}}]({{logo}}){.logo_repo} {{name}}]({{url}}) | {{desc}} | [{{git_platform_info}}]({{git_repo_url}}) |
{%-     endfor %}
{%-   endif %}

[{{ i_section }}]: {{ i_section }}/
{%- endfor %}

*[GRidOG]: Get Rid Of Google
