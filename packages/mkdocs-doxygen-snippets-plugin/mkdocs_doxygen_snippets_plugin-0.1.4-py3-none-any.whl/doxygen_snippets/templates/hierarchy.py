# TODO not working {{link_prefix}}

TEMPLATE = """
# Class Hierarchy

This inheritance list is sorted roughly, but not completely, alphabetically:

{% for node in classes recursive %}
{% if node.is_resolved -%}
* **{{node.kind.value}}** [**{{node.name_long}}**]({{node.url}}) {{node.brief}}
{%- else -%}
* **{{node.kind.value}}** **{{node.name_long}}**
{%- endif %}
{%- if node.derived_classes %}
  {{- loop(node.derived_classes)|indent(2, true) }}
{%- endif %}
{%- endfor %}
"""
