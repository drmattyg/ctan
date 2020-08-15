{% macro mentee_profile(c) -%}
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


{% macro mentor_profile(c) -%}
{{ c.firstname }} {{ c.lastname }}

m_token: {{c.token}}

[ {{c.linkedin }} ]

*Works In*:

{{ c.workin }}

*Expertise*

{{ c.expertise }}

*Time in Industy*

{{ c.howlong }}

*Why*

{{ c.why }}

*Notes*

{{ c.notes }}
{%- endmacro %}
