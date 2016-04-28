
import markdown2

head = """
{% extends "layout.html" %}
{% block body %}
"""

foot = """
{% endblock %}
"""

f = open('about.md')
html = head + markdown2.markdown(f.read(), extras=["smarty-pants"]) + foot
fout = open('../templates/about.html', 'w')
fout.write(html)

