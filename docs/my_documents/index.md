---
hide:
  - toc        # Hide table of contents
---


{%- set i_section = "my_documents" %}
{%- if subrepo[i_section] %}
{%-   set section_name = subrepo[i_section]['nav_entry'] %}
{%-   set section_info = subs(i_section) %}

{%-   if subs(i_section) %}
{%-     set section_logo = section_info.logo | replace("/","../",1) %}
{%-     set section_desc = to_html(section_info.desc) %}
# ![{{ section_name }}]({{ section_logo }}){.logo_section} {{section_name}}

{{ section_desc }}
{%-   else %}
# {{ section_name }}
{%-   endif %}

{%-   if subrepo[i_section]["external"] or subrepo[i_section]["internal"] %}
| Name | Description | Repo |
|-----| ----| ----|
{%-     for i_repo in subrepo[i_section]["external"] %}
{%-       set curr_repo = subs(i_repo.name) %}
{%-       set name = curr_repo.name %}
{%-       set logo = curr_repo.logo | replace('assets','latest/assets') | replace('/','../../',1) %}
{%-       set desc = to_html(curr_repo.desc) %}
{%-       set url = i_repo.online_url | replace('/','../../',1) %}
{%-       set git_platform_info = git_platform.logo ~ " " ~ git_platform.name  %}
{%-       set git_repo_url = git_platform.url ~ curr_repo.git_slug_with_namespace %}
| [![{{name}}]({{logo}}){.logo_repo} {{name}}]({{url}}) | {{desc}} | [{{git_platform_info}}]({{git_repo_url}}) |
{%-     endfor %}
{%-     for i_repo in subrepo[i_section]["internal"] %}
{%-       set curr_repo = subs(i_repo.name) %}
{%-       set name = curr_repo.name %}
{%-       set logo = curr_repo.logo | replace('assets','latest/assets') | replace('/','../../',1) %}
{%-       set desc = to_html(curr_repo.desc) %}
{%-       set url = i_repo.online_url | replace('/','../../',1) %}
{%-       set git_platform_info = git_platform.logo ~ " " ~ git_platform.name  %}
{%-       set git_repo_url = git_platform.url ~ curr_repo.git_slug_with_namespace %}
| [![{{name}}]({{logo}}){.logo_repo} {{name}}]({{url}}) | {{desc}} | [{{git_platform_info}}]({{git_repo_url}}) |
{%-     endfor %}
{%-   endif %}
{%- endif %}
