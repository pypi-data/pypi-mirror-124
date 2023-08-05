TEMPLATE = """
# {{title}}

{% for letter, items in dictionary.items() %}
## {{letter}}

{% for name, parents in items.items() -%}
* **{{name}}** (
{%- for parent in parents -%}[**{{parent.name_long}}**]({{parent.url}}){{ ', ' if not loop.last else '' }}{% endfor -%} )
{% endfor %}
{% endfor %}
"""
