
import markdown2

head = """
{% extends "val3dity/layout.html" %}
{% block body %}
<title>val3dity: geometric validation of solids according to ISO19107</title>  
"""

foot = """
{% endblock %}
"""

f = open('contact.md')
html = head + markdown2.markdown(f.read(), extras=["smarty-pants"]) + foot
fout = open('../templates/val3dity/contact.html', 'w')
fout.write(html)

f = open('faq.md')
html = markdown2.markdown(f.read(), extras=['toc', 'smarty-pants'])
htmltoc = html.toc_html
s = htmltoc.rfind('<ul>')
e = htmltoc.find('</ul>')
html = str(html)  
html = head + html.replace('<!--TOC-->', htmltoc[s:e+5]) + foot
fout = open('../templates/val3dity/faq.html', 'w')
fout.write(html)

f = open('about.md')
html = head + markdown2.markdown(f.read(), extras=["smarty-pants"]) + foot
fout = open('../templates/val3dity/about.html', 'w')
fout.write(html)

