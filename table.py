from lxml import etree
from common import NSM, setx, mmf, NSW, getap, ntf, setap, Body, dc
from copy import deepcopy
import ct, txt, par, mm

def xtabular(nd):
    t = etree.Element(NSW+'tbl')
    pr = etree.SubElement(t, NSW+'tblPr')
    sty = etree.SubElement(pr, NSW+'tblStyle')
    sty.set(NSW+'val', 'tbl')
    jc = etree.SubElement(pr, NSW+'jc')
    jc.set(NSW+'val', 'center')
    setx(nd, t, t)
    getap(nd).append(t)
    ct.cnl(nd)
    
def xArrayRow(nd):
    if mmf.isset():
        mm.xArrayRow(nd)
        return
    tr(nd)
    
def xArrayCell(nd):
    if mmf.isset():
        mm.xArrayCell(nd)
        return
    tc(nd)
    
def tr(nd):
    r = etree.Element(NSW+'tr')
    getap(nd).append(r)
    setx(nd, r, r)
    ct.cnl(nd)
    
def tc(nd):
    c = etree.Element(NSW+'tc')
    cp = etree.SubElement(c, NSW+'tcPr')
    
    if 'colspan' in nd.attributes:
        gs = etree.SubElement(cp, NSW+'gridSpan')
        gs.set(NSW+'val', str(nd.attributes['colspan']))
        
    bd = etree.SubElement(cp, NSW+'tcBorders')
    
    if 'border-top-style' in nd.style:
        tb = etree.SubElement(bd, NSW+'top')
        if nd.style['border-top-style'] == 'solid':
            tb.set(NSW+'val', 'single')
        
    if 'border-bottom-style' in nd.style:
        bb = etree.SubElement(bd, NSW+'bottom')
        if nd.style['border-bottom-style'] == 'solid':
            bb.set(NSW+'val', 'single')
        
    if 'border-left' in nd.style:
        sb = etree.SubElement(bd, NSW+'start')
        s = nd.style['border-left'].split()
        if s[1] == 'solid':
            sb.set(NSW+'val', 'single')
    
    if 'border-right' in nd.style:    
        eb = etree.SubElement(bd, NSW+'end')
        s = nd.style['border-right'].split()
        if s[1] == 'solid':
            eb.set(NSW+'val', 'single')
            
        
    if nd.style['text-align'] == 'center':
        dc.ac = 'c'
    elif nd.style['text-align'] == 'right':
        dc.ac = 'r'
    elif nd.style['text-align'] == 'left':
        dc.ac = 'l'
        
    getap(nd).append(c)
    if nd.childNodes:    
        setx(nd,c,c)
        ct.cnl(nd)
    
    p = c.find(NSW+'p')
    if p == None:
        p = etree.SubElement(c, NSW+'p')
        par.setAlign(p)
        
    dc.acPop()
        
    
def xtable(nd):
    ct.pn(nd)

