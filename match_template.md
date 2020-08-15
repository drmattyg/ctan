*Mentee*
{{me.firstname}} {{me.lastname}}

*Mentors*
{% for mr in mentors %} 
- {{ mr.firstname }} {{ mr.lastname }}
{% endfor %}