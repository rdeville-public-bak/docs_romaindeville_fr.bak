

{% for i_section in subrepo %}
{% for i_repo in subrepo[i_section]["external"] %}
{% set curr_repo = subs(i_repo.name) %}
![!{{ i_repo.name }}]({{ curr_repo.logo }})

{{ curr_repo.desc }}
{% endfor %}
{% endfor %}

<!-- BEGIN MKDOCS TEMPLATE -->
<!-- END MKDOCS TEMPLATE -->