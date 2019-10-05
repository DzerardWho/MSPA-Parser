from arpeggio import ParserPython
# from arpeggio.export import PTDOTExporter
from mspaParser import mspaText


text = r'''tekst przed tagiem<jade2, 134, jhon: to jest<rose: wewnętrzny tag><\
vriska:kolejny tag
zaraz po poprzednim> te\<\>/</>stowy tekst
z polskimi znakami ąćęłńóśtżź>
<dave: kolejny tag>'''

text2 = r'''testtesttse
<jade: test>
test <jade, style<color: #c4118e; font-size: 30px;>, id<Jade: >: test
<url<http://www.google.pl>, style<color: #11c47f>:Google>
<url<http://www.google.pl>:>
<img<width="200" height="100">:madrala.png>
<url<https://homestuckproject.pl>:<img:trollcool.gif>>>
<def<john>: to jeszcze w żaden sposób nie oddziałowuje na resztę>
<html:<h1>TEST</h1>//>/>
<dave: <john, id<>: f\<<rose: y u play baby game y yu no shcut>\>de

ts>>
<scratch: testtestets>'''

text3 = '<url<https://homestuckproject.pl>:<img:trollcool.gif>>'

parser = ParserPython(mspaText, debug=False, reduce_tree=True, skipws=False,
                      ws="\t ", memoization=True)

parse_tree = parser.parse(text3)
# print(parse_tree)
