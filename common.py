#coding=gbk
from lxml import etree

NSW = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
NSM = '{http://schemas.openxmlformats.org/officeDocument/2006/math}'

nm = {'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
      'm':'http://schemas.openxmlformats.org/officeDocument/2006/math',
      'r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}

Document = etree.Element(NSW+'document',nsmap=nm)
Body = etree.SubElement(Document, NSW+'body')
Style = {'class':'article'}

class Flag:
    def __init__(self):
        self.f = False
        self.l = []
        
    def set(self):
        self.f = True
        
    def clear(self):
        self.f = False
        
    def push(self):
        self.l.append(self.f)
        
    def pop(self):
        self.f = self.l.pop()
        
    def isset(self):
        return(self.f)

def wSPar(sty):
    p = etree.Element(NSW+'p')
    pr = etree.SubElement(p, NSW+'pPr')
    ps = etree.SubElement(pr, NSW+'pStyle')
    ps.set(NSW+'val', sty)
    return p

def wText(txt, ps=True):
    r = etree.Element(NSW+'r')
    t = etree.SubElement(r,NSW+'t')
    if ps is True:
        t.set('{http://www.w3.org/XML/1998/namespace}space','preserve')
    t.text = txt
    return r

    
def setx(nd, xe, ap):
    nd.setUserData('xe', xe)
    nd.setUserData('ap', ap)
    
def getap(nd):
    return(nd.parentNode.getUserData('ap'))

def setap(nd, ap):
    nd.setUserData('ap', ap)

#非空段落标记
npf = Flag()

#norm text in math mode
ntf = Flag()

#math mode flag
mmf = Flag()

#rpr italic flag
rif = Flag()

ttf = Flag()

rbf = Flag()