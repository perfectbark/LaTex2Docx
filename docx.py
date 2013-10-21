from lxml import etree
from zipfile import ZipFile
from string import lstrip
from common import wSPar, NSM, NSW, Body, Document, wText, setx
import ct

_pd = dict()

def xdoc(nd):
    setx(nd, Document, Document)
    ct.cnl(nd)
    
def xdocument(nd):
    setx(nd, Body, Body)
    ct.cnl(nd)


def save(name):
    zf = ZipFile(name+'.docx', mode="w")
    
    zf.writestr('[Content_Types].xml', etree.tostring(_pd['types']))
    zf.writestr('_rels/.rels', etree.tostring(_pd['rel']))
    zf.writestr('word/_rels/document.xml.rels', etree.tostring(_pd['partrel']))
    zf.writestr('word/styles.xml', etree.tostring(_pd['sty']))
    zf.writestr('word/numbering.xml', etree.tostring(_pd['numbering']))
    zf.writestr('word/footnotes.xml', etree.tostring(_pd['footnotes']))
    zf.writestr('word/settings.xml', etree.tostring(_pd['settings']))
    
    zf.writestr('word/document.xml', etree.tostring(Document,encoding='UTF-8',xml_declaration=True,standalone=True))
    
    zf.close()

def _loadparts():
    ps = etree.XMLParser(remove_blank_text=True)
    _pd['sty'] = etree.parse('styles.xml', ps)
    _pd['rel'] = etree.parse('relations.xml', ps)
    _pd['partrel'] = etree.parse('partrel.xml', ps)
    _pd['types'] = etree.parse('types.xml', ps)
    _pd['numbering'] = etree.parse('numbering.xml', ps)
    _pd['settings'] = etree.parse('settings.xml', ps)
    _pd['footnotes'] = etree.parse('footnotes.xml', ps)
    
_loadparts()
Numbering = _pd['numbering'].getroot()
Footnotes = _pd['footnotes'].getroot()

if __name__ == "__main__":
    p = etree.SubElement(Body, NSW+'p')
    r = etree.SubElement(p, NSW+'r')
    save('sd')