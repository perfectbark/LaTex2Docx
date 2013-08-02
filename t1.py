from plasTeX.TeX import TeX
from lxml import etree
import ct, docx
from common import Document

td = TeX(file='nt.tex')
td = td.parse()

print
print td.toXML()

print
ct.cnd(td)

#print etree.tostring(Document, encoding='utf-8', xml_declaration=True, standalone=True, pretty_print=True)

docx.save('sd')
