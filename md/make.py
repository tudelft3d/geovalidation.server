
import markdown2

f = open('contact.md')
html = markdown2.markdown(f.read(), extras=["smarty-pants"])
fout = open('../contact.html', 'w')
fout.write(html)

f = open('faq.md')
html = markdown2.markdown(f.read(), extras=['toc', 'smarty-pants'])
htmltoc = html.toc_html
s = htmltoc.rfind('<ul>')
e = htmltoc.find('</ul>')
html = str(html)  
html = html.replace('<!--TOC-->', htmltoc[s:e+5])
fout = open('../faq.html', 'w')
fout.write(html)

f = open('about.md')
html = markdown2.markdown(f.read(), extras=["smarty-pants"])
fout = open('../about.html', 'w')
fout.write(html)

