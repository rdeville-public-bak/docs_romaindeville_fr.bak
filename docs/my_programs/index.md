---
hide:
  - toc        # Hide table of contents
---


{%- set i_section = "my_programs" %}
{%- set section_name = subrepo[i_section]['nav_entry'] %}
{%- set section_info = subs(i_section) %}

{%- if subs(i_section) %}
{%-   set section_logo = section_info.logo %}
{%-   set section_desc = section_info.desc %}
# ![{{ section_name }}]({{ section_logo }}){.logo_section} {{ section_name}}

{{ section_desc }}
{%- else %}
# {{ section_name }}
{%- endif %}

| Name | Description | Repo |
|-----| ----| ----|
{%- for i_repo in subrepo[i_section]["external"] %}
{%-   set curr_repo = subs(i_repo.name) %}
{%-   set name = curr_repo.name %}
{%-   set logo = curr_repo.logo | replace('assets','latest/assets') | replace('/','../../',1) %}
{%-   set desc = curr_repo.desc %}
{%-   set url = i_repo.online_url | replace('/','../../',1) %}
{%-   set git_platform_info = git_platform.logo ~ " " ~ git_platform.name  %}
| [![{{ name }}]({{ logo }}){.logo_repo} {{ name }}]({{ url }}) | {{ to_html(desc) }} | [{{ git_platform_info }}]({{ online_url }}) |
{%- endfor %}

