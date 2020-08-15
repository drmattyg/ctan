{% macro profile(c) -%}
{{ c.firstname }} {{ c.lastname }}

m_token: {{c.token}}

[ {{c.linkedin }} ]

*Interests*:

{{ c.interestedin }}

*Expertise*

{{ c.expertise }}

*Time in Industy*

{{ c.howlong }}

*Why*

{{ c.why }}

*Notes*

{{ c.notes }}
{%- endmacro %}

{{ profile(me) }}