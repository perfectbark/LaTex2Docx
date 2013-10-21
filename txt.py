from common import NSM, NSW, npf, mmf, ntf, getap, rif, setap, ttf, rbf
from lxml import etree
import ct

def xtext(nd):
    if nd.parentNode.nodeName == '#document':
        return
    
    s = nd.textContent
    if not mmf.isset():
        p = getap(nd)
        if len(p) == 0:
            s = s.lstrip()
        elif p[-1].tag == NSW+'pPr':
            s = s.lstrip()
    
    #if nd.previousSibling == None:
        #s = s.lstrip()
    #elif nd.previousSibling.blockType == True:
        #s = s.lstrip()
    #if nd.nextSibling == None:
        #s = s.rstrip()
    #if s == '':
        #return
    #else:
        #r = tr(s)
    if s == '':
        return
    r = tr(s)
    getap(nd).append(r)

def tr(s):
    if mmf.isset():
        r  = etree.Element(NSM+'r')
        if rpr()!=None:
            r.append(rpr())
        if ntf.isset():
            pr = etree.SubElement(r, NSM+'rPr')
            etree.SubElement(pr, NSM+'nor')
            t = etree.SubElement(r,NSM+'t')
            t.text = s
        else:
            t = etree.SubElement(r,NSM+'t')
            t.text = s.replace(" ", "")
            npf.set()
    else:
        r  = etree.Element(NSW+'r')
        if rpr()!=None:
            r.append(rpr())
        t = etree.SubElement(r,NSW+'t')
        t.set('{http://www.w3.org/XML/1998/namespace}space','preserve')
        t.text = s
        if t.text.isspace()==False:
            npf.set()
    return r

def rpr():
    r = None
    if rif.isset():
        if r==None:
            r = etree.Element(NSW+'rPr')
        etree.SubElement(r,NSW+'i')
    if ttf.isset():
        if mmf.isset():
            if r==None:
                r = etree.Element(NSM+'rPr')
            scr = etree.SubElement(r, NSM+'scr')
            scr.set(NSM+'val', 'monospace')
            sty = etree.SubElement(r, NSM+'sty')
            sty.set(NSM+'val', 'p')
        else:
            if r==None:
                r = etree.Element(NSW+'rPr')
            f = etree.SubElement(r, NSW+'rFonts')
            f.set(NSW+'ascii', 'Courier New')
    if rbf.isset():
        if r==None:
            r = etree.Element(NSW+'rPr')
        etree.SubElement(r,NSW+'b')
    return r
    
def xit(nd):
    rif.set()
    setap(nd, getap(nd))
    ct.cnl(nd)
    rif.clear()

def xem(nd):
    rif.set()
    setap(nd, getap(nd))
    ct.cnl(nd)
    rif.clear()
    
def xtexttt(nd):
    ttf.set()
    setap(nd, getap(nd))
    ct.cnl(nd)
    ttf.clear()
    
def xbf(nd):
    rbf.set()
    setap(nd, getap(nd))
    ct.cnl(nd)
    rbf.clear()
    
def xbgroup(nd):
    rif.push()
    rif.clear()
    rbf.push()
    rbf.clear()
    setap(nd, getap(nd))
    ct.cnl(nd)
    rbf.pop()
    rif.pop()
    
def pmtr(s):
    r = etree.Element(NSM+'r')
    pr = etree.SubElement(r, NSM+'rPr')
    scr = etree.SubElement(pr, NSM+'scr')
    scr.set(NSM+'val', 'roman')
    sty = etree.SubElement(pr, NSM+'sty')
    sty.set(NSM+'val', 'p')
    t = etree.SubElement(r, NSM+'t')
    t.text = s
    return r

def xverbatim(nd):
    ls = nd.textContent.splitlines()
    if ls[0] == '':
        ls = ls[1:]
    p = getap(nd)
    ttf.push()
    ttf.set()
    for l in ls:
        p.append(tr(l))
        p.append(etree.Element(NSW+'br'))
    p.remove(p[-1])
    ttf.pop()
