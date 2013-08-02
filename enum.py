from lxml import etree
from common import NSM, setx, mmf, NSW, getap, ntf, setap, Body
from copy import deepcopy
import ct, txt, docx

def xenumerate(nd):
    nr = docx.Numbering
    num = etree.Element(NSW+'num')
    num.set(NSW+'numId', nd.id[1:])
    nr.append(num)
    an = etree.SubElement(num, NSW+'abstractNumId')
    an.set(NSW+'val', '0')
    lo = lvloveride()
    num.append(lo)
    setx(nd, num, getap(nd))
    ct.cnl(nd)
    
def xitem(nd):
    setap(nd, getap(nd))
    ct.cnl(nd)
    
def itempar(nd):
    p = etree.Element(NSW+'p')
    pr = etree.SubElement(p, NSW+'pPr')
    l = lvl(nd)
    if nd.previousSibling!=None:
        ind = etree.SubElement(pr, NSW+'ind')
        li = str((l+1)*420)
        ind.set(NSW+'left', li) #Left Indentation
    else:
        np = etree.SubElement(pr, NSW+'numPr')
        ilv = etree.SubElement(np, NSW+'ilvl')
        ilv.set(NSW+'val', str(l))
        nid = etree.SubElement(np, NSW+'numId')
        nid.set(NSW+'val', nd.parentNode.parentNode.id[1:])
        fl = etree.SubElement(pr, NSW+'ind')
        fl.set(NSW+'firstLineChars', '0')
        li = str((l+1)*420)
        fl.set(NSW+'left', li) #Left Indentation
        fl.set(NSW+'hanging', '420')

    getap(nd).append(p)
    setx(nd, p, p)
    ct.cnl(nd)

def lvl(nd):
    l = -1
    np = nd.parentNode
    while np.nodeName != 'document':
        if np.nodeName == 'enumerate' or np.nodeName == 'itemize':
            l = l+1
        np = np.parentNode
        
    return l

def lvloveride():
    lo = etree.Element(NSW+'lvlOverride')
    lo.set(NSW+'ilvl', '0')
    so = etree.SubElement(lo, NSW+'startOverride')
    so.set(NSW+'val', '1')
    return lo

def xitemize(nd):
    nr = docx.Numbering
    num = etree.Element(NSW+'num')
    num.set(NSW+'numId', nd.id[1:])
    nr.append(num)
    an = etree.SubElement(num, NSW+'abstractNumId')
    an.set(NSW+'val', '0')
    lo = itemizeLvlOveride(str(lvl(nd)+1))
    num.append(lo)
    setx(nd, num, getap(nd))
    ct.cnl(nd)

def itemizeLvlOveride(lv):
    lo = etree.Element(NSW+'lvlOverride')
    lo.set(NSW+'ilvl', lv)
    il = etree.SubElement(lo, NSW+'lvl')
    il.set(NSW+'ilvl', lv)
    fmt = etree.SubElement(il, NSW+'numFmt')
    fmt.set(NSW+'val', 'bullet')
    lt = etree.SubElement(il, NSW+'lvlText')
    lt.set(NSW+'val', u"\u2022")
    return lo
    