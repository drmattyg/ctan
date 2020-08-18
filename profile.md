{% macro mentee_profile(c) -%}
{{ c.firstname }} {{ c.lastname }}

*Location*
{{ c.city }}

[ {{c.linkedin }} ]

*Job role*
{{ c.role }}

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

*Location*
{{ c.city }}

[ {{c.linkedin }} ]

*Job role*
{{ c.role }}

*Overlap interests*:

{{ c.overlap }}

*Expertise*

{{ c.expertise }}

*Time in Industy*

{{ c.howlong }}

*Why*

{{ c.why }}

*Notes*

{{ c.notes }}
{%- endmacro %}
