from common import NSW, NSM, npf, getap, setx, Body, mmf, setap, rbf, rif, Style
from lxml import etree
import ct, txt, enum, docx, datetime

_mt = dict()

def xpar(nd):
    if nd.firstChild != None:
        if nd.firstChild.nodeName in {'enumerate', 'itemize', 'equation', 'abstract', 'thebibliography'}:
            setap(nd, getap(nd))
            ct.cnl(nd)
            return
    else:
        return
    
    
    if mmf.isset():
        setap(nd, getap(nd))
        ct.cnl(nd)
        return
    
    if nd.parentNode.nodeName=='item':
        enum.itempar(nd)
        return
        
    p = etree.Element(NSW+'p')
    setx(nd, p, p)
    npf.clear()
    ct.cnl(nd)
    if npf.isset():
        getap(nd).append(p)
    
def xbr(nd):
    r = etree.Element(NSW+'br')
    getap(nd).append(r)

def spar(sty):
    p = etree.Element(NSW+'p')
    pr = etree.SubElement(p, NSW+'pPr')
    ps = etree.SubElement(pr, NSW+'pStyle')
    ps.set(NSW+'val', sty)
    return p
    
def xtitle(nd):
    npf.push()
    p = spar('title')
    _mt['title'] = p
    setx(nd, p, p)
    ct.cnl(nd)
    npf.pop()
    
def xauthor(nd):
    npf.push()
    p = spar('author')
    _mt['author'] = p
    setx(nd, p, p)
    ct.cnl(nd)
    npf.pop()

def xdate(nd):
    npf.push()
    p = spar('author')
    _mt['date'] = p
    setx(nd, p, p)
    ct.cnl(nd)
    npf.pop()

def xmaketitle(nd):
    if 'title' in _mt.keys():
        Body.insert(0,_mt['title'])
    if 'author' in _mt.keys():
        Body.insert(1,_mt['author'])
    if 'date' in _mt.keys():
        Body.insert(2,_mt['date'])
    else:
        npf.push()
        p = spar('author')
        p.append(txt.tr(datetime.date.strftime(datetime.date.today(),'%B %d, %Y')))
        Body.insert(2, p)
        npf.pop()

        

def xsection(nd):
    s = nd.ref.textContent + '. ' + nd.attributes['title'].textContent
    r = txt.tr(s)
    p = spar('section')
    p.append(r)
    getap(nd).append(p)
    setx(nd, p, getap(nd))
    ct.cnl(nd)

def xabstract(nd):
    r = txt.tr('Abstract')
    p = spar('section')
    p.append(r)
    getap(nd).append(p)
    setx(nd, p, getap(nd))
    ct.cnl(nd)

def ipar(nd):
    if nd.firstChild != None:
        if nd.firstChild.nodeName == 'enumerate':
            return True
        else:
            return False
    return False

def xquote(nd):
    p = getap(nd)
    pr = p.find('.//'+NSW+'pPr')
    if pr==None:
        pr = etree.SubElement(p, NSW+'pPr')
        ind = etree.SubElement(pr, NSW+'ind')
        ind.set(NSW+'left','420')
        ind.set(NSW+'right','420')
    else:
        ind = pr.find('.//'+NSW+'ind')
        if ind == None:
            ind = etree.SubElement(pr, NSW+'ind')
            ind.set(NSW+'left','420')
            ind.set(NSW+'right','420')
        else:
            left = ind.get(NSW+'left')
            if left == None:
                left = '420'
            else:
                left = str(int(left)+420)
            ind.set(NSW+'left',left)
            right = ind.get(NSW+'right')
            if right == None:
                right = '420'
            else:
                right = str(int(right)+420)
            ind.set(NSW+'right',right)
    setap(nd, p)
    ct.cnl(nd)
                
def xtheorem(nd):
    cap = nd.caption
    p = etree.Element(NSW+'p')
    setap(cap, p)
    rbf.push()
    rbf.set()
    ct.cnl(cap)
    p.append(txt.tr(' '+nd.ref.textContent))
    rbf.pop()

    rif.push()
    rif.set()
    i = 1
    if nd.childNodes[0].firstChild.nodeName == 'displaymath':
        i = 0
    else:
        setap(nd.childNodes[0], p)
        ct.cnl(nd.childNodes[0])
    np = getap(nd.parentNode)
    setap(nd, np)
    np.append(p)
    for par in nd.childNodes[i:]:
        ct.cnd(par)
    rif.pop()
    npf.clear()
    
def xthebibliography(nd):
    r = txt.tr('References')
    p = spar('section')
    p.append(r)
    getap(nd).append(p)
    setx(nd, p, getap(nd))
    ct.cnl(nd)

def xbibitem(nd):
    p = etree.Element(NSW+'p')
    p.append(txt.tr('['+nd.bibcite.childNodes[0]+'] '))
    setap(nd.firstChild, p)
    ct.cnl(nd.firstChild)
    getap(nd).append(p)
             
def xthanks(nd):
    def fr(sr):
        r = etree.Element(NSW+'r')
        rpr = etree.SubElement(r, NSW+'rPr')
        rs = etree.SubElement(rpr, NSW+'rStyle')
        rs.set(NSW+'val', 'sup')
        fr = etree.SubElement(r, NSW+sr)
        fr.set(NSW+'id', i)
        return r
    i = nd.id[1:]
    f = etree.Element(NSW+'footnote')
    f.set(NSW+'id', i)
    p = etree.SubElement(f, NSW+'p')
    setap(nd, p)
    p.append(fr('footnoteRef'))
    ct.cnl(nd)
    getap(nd).append(fr('footnoteReference'))
    docx.Footnotes.append(f)
    
def setfnf(p, s):
    pr = p.find(NSW+'pPr')
    if pr == None:
        pr = etree.Element(NSW+'pPr')
        p.insert(0, pr)
    sp = pr.find(NSW+'sectPr')
    if sp == None:
        sp = etree.SubElement(pr, NSW+'sectPr')
    t = sp.find(NSW+'type')
    if t == None:
        t = etree.SubElement(sp, NSW+'type')
    t.set(NSW+'val', 'continuous')
    fp = sp.find(NSW+'footnotePr')
    if fp == None:
        fp = etree.SubElement(sp, NSW+'footnotePr')
    fnf = fp.find(NSW+'numFmt')
    if fnf == None:
        fnf = etree.SubElement(fp, NSW+'numFmt')
    fnf.set(NSW+'val', s)
