from lxml import etree
from common import NSM, setx, mmf, NSW, getap, ntf, setap, Body
from copy import deepcopy
import ct, txt

def xmath(nd):
    mmf.push()
    mmf.set()
    if ntf.isset():
        ntf.push()
        ntf.clear()
        setap(nd, getap(nd))
        ct.cnl(nd)
        ntf.pop()
    else:
        e = etree.Element(NSM+'oMath')
        setx(nd, e, e)
        ct.cnl(nd)
        getap(nd).append(e)
    mmf.pop()

def xdisplaymath(nd):
    ap = getap(nd)
    if nd.previousSibling != None:
        ap.append(etree.Element(NSW+'br'))
    mmf.push()
    mmf.set()
    p = etree.Element(NSM+'oMathPara')
    m = etree.SubElement(p, NSM+'oMath')
    setx(nd, p, m)
    ct.cnl(nd)
    ap.append(p)
    mmf.pop()
    if nd.previousSibling != None:
        ap.append(etree.Element(NSW+'br'))

def xtext(nd):
    ntf.push()
    ntf.set()
    setap(nd, getap(nd))
    ct.cnl(nd)
    ntf.pop()

def _table():
    s = """    
        <w:tbl xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
          <w:tblPr>
            <w:tblStyle w:val="a3" />
            <w:tblW w:w="5036" w:type="pct" />
            <w:tblBorders>
              <w:top w:val="none" w:sz="0" w:space="0"
              w:color="auto" />
              <w:left w:val="none" w:sz="0" w:space="0"
              w:color="auto" />
              <w:bottom w:val="none" w:sz="0" w:space="0"
              w:color="auto" />
              <w:right w:val="none" w:sz="0" w:space="0"
              w:color="auto" />
              <w:insideH w:val="none" w:sz="0" w:space="0"
              w:color="auto" />
              <w:insideV w:val="none" w:sz="0" w:space="0"
              w:color="auto" />
            </w:tblBorders>
            <w:tblLayout w:type="fixed" />
            <w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0"
            w:firstColumn="1" w:lastColumn="0" w:noHBand="0"
            w:noVBand="1" />
          </w:tblPr>
          <w:tblGrid>
            <w:gridCol w:w="859" />
            <w:gridCol w:w="6866" />
            <w:gridCol w:w="858" />
          </w:tblGrid>
          <w:tr>
            <w:tc>
              <w:tcPr>
                <w:tcW w:w="500" w:type="pct" />
                <w:vAlign w:val="center" />
              </w:tcPr>
              <w:p>
                <w:pPr>
                  <w:jc w:val="left" />
                </w:pPr>
              </w:p>
            </w:tc>
            <w:tc>
              <w:tcPr>
                <w:tcW w:w="4000" w:type="pct" />
                <w:vAlign w:val="center" />
              </w:tcPr>
              <w:p>
                <w:pPr>
                  <w:jc w:val="center" />
                </w:pPr>
              </w:p>
            </w:tc>
            <w:tc>
              <w:tcPr>
                <w:tcW w:w="500" w:type="pct" />
                <w:vAlign w:val="center" />
              </w:tcPr>
              <w:p>
                <w:pPr>
                  <w:jc w:val="right" />
                </w:pPr>
              </w:p>
            </w:tc>
          </w:tr>
        </w:tbl>
    """
    ps = etree.XMLParser(remove_blank_text=True)
    t = etree.fromstring(s, ps)
    return t
    
def xequation(nd):
    t = deepcopy(_tbe)
    it = t.iter(NSW+'p')
    lp = it.next()
    mp = it.next()
    rp = it.next()
    p = etree.SubElement(mp,NSM+'oMathPara')
    m = etree.SubElement(p, NSM+'oMath')
    
    ref = '('+nd.ref.textContent+')'
    rp.append(txt.tr(ref))
    
    Body.append(t)
    setx(nd, p, m)
    mmf.push()
    mmf.set()
    ct.cnl(nd)
    mmf.pop()

def xfrac(nd):
    f = etree.Element(NSM+'f')
    fpr = etree.SubElement(f,NSM+'fPr')
    tp = etree.SubElement(fpr,NSM+'type')
    tp.set(NSM+'val','bar')
    getap(nd).append(f)
    num = etree.SubElement(f, NSM+'num')
    setx(nd.attributes['numer'], num, num)
    ct.cnl(nd.attributes['numer'])
    den = etree.SubElement(f, NSM+'den')
    setx(nd.attributes['denom'], den, den)
    ct.cnl(nd.attributes['denom'])
    

def xdelim(nd):
    d = etree.Element(NSM+'d')
    dpr = etree.SubElement(d, NSM+'dPr')
    bc = etree.SubElement(dpr, NSM+'begChr')
    if nd.attributes['bchar'].textContent != '.':
        bc.set(NSM+'val', nd.attributes['bchar'].textContent)
    else:
        bc.set(NSM+'val', '')
    ec = etree.SubElement(dpr, NSM+'endChr')
    if nd.attributes['echar'].textContent != '.':
        ec.set(NSM+'val', nd.attributes['echar'].textContent)
    else:
        ec.set(NSM+'val', '')
    e = etree.SubElement(d, NSM+'e')
    setx(nd, d, e)
    getap(nd).append(d)
    ct.cnl(nd)

def xarray(nd):
    m = etree.Element(NSM+'m')
    getap(nd).append(m)
    setx(nd, m, m)
    ct.cnl(nd)

def xArrayRow(nd):
    mr = etree.Element(NSM+'mr')
    getap(nd).append(mr)
    setx(nd, mr, mr)
    ct.cnl(nd)
    if nd.parentNode.nodeName == 'eqnarray':
        e = etree.Element(NSM+'e')
        mr.append(e)
        if nd.ref != None:
            ntf.push()
            ntf.set()
            e.append(txt.tr('     ('+nd.ref.textContent+')'))
            ntf.pop()
            
    
def xArrayCell(nd):
    e = etree.Element(NSM+'e')
    getap(nd).append(e)
    setx(nd, e, e)
    ct.cnl(nd)

def _mpreqa():
    s = """    
    <m:mPr xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
      <m:cGpRule m:val="3" />
      <m:cGp m:val="72" />
      <m:mcs>
        <m:mc>
          <m:mcPr>
            <m:count m:val="1" />
            <m:mcJc m:val="right" />
          </m:mcPr>
        </m:mc>
        <m:mc>
          <m:mcPr>
            <m:count m:val="1" />
            <m:mcJc m:val="center" />
          </m:mcPr>
        </m:mc>
        <m:mc>
          <m:mcPr>
            <m:count m:val="1" />
            <m:mcJc m:val="left" />
          </m:mcPr>
        </m:mc>
        <m:mc>
          <m:mcPr>
            <m:count m:val="1" />
            <m:mcJc m:val="right" />
          </m:mcPr>
        </m:mc>
      </m:mcs>
    </m:mPr>
    """
    ps = etree.XMLParser(remove_blank_text=True)
    t = etree.fromstring(s, ps)
    return t

def xeqnarray(nd):
    p = etree.Element(NSM+'oMathPara')
    m = etree.SubElement(p, NSM+'oMath')
    m = etree.SubElement(m, NSM+'m')
    m.append(_mpreqa())
    
    getap(nd).append(p)
    setx(nd, p, m)
    mmf.push()
    mmf.set()
    ct.cnl(nd)
    mmf.pop()
    
_tbe = _table()

def xbar(nd):
    a = etree.Element(NSM+'acc')
    pr = etree.SubElement(a, NSM+'accPr')
    ch = etree.SubElement(pr, NSM+'chr')
    ch.set(NSM+'val', u'\u0304')
    e = etree.SubElement(a, NSM+'e')
    getap(nd).append(a)
    setx(nd, a, e)
    ct.cnl(nd)
    
def accent(nd, char):
    a = etree.Element(NSM+'acc')
    pr = etree.SubElement(a, NSM+'accPr')
    ch = etree.SubElement(pr, NSM+'chr')
    ch.set(NSM+'val', char)
    e = etree.SubElement(a, NSM+'e')
    getap(nd).append(a)
    setx(nd, a, e)
    ct.cnl(nd)
    
def xhat(nd):
    accent(nd, u"\u0302")

def xtilde(nd):
    accent(nd, u'\u0303')
    
def xref(nd):
    getap(nd).append(txt.tr(nd.idref['label'].ref.textContent))
    
def xlim(nd):
    limlow(nd, 'lim')
    #ll = etree.Element(NSM+'limLow')
    #e = etree.SubElement(ll, NSM+'e')
    #e.append(txt.pmtr('lim'))
    #l = etree.SubElement(ll, NSM+'lim')
    #setx(nd, ll, l)
    #getap(nd).append(ll)
    #ct.cnl(nd)
    
def xmin(nd):
    ll = etree.Element(NSM+'limLow')
    e = etree.SubElement(ll, NSM+'e')
    e.append(txt.pmtr('min'))
    l = etree.SubElement(ll, NSM+'lim')
    getap(nd).append(ll)
    ns = nd.nextSibling
    if ns.nodeName=='active::_':
        setap(ns, l)
        ct.cnl(ns)
        nd.parentNode.removeChild(ns)
    
def limlow(nd, s):
    ll = etree.Element(NSM+'limLow')
    e = etree.SubElement(ll, NSM+'e')
    e.append(txt.pmtr(s))
    l = etree.SubElement(ll, NSM+'lim')
    getap(nd).append(ll)
    ns = nd.nextSibling
    if ns.nodeName=='active::_':
        setap(ns, l)
        ct.cnl(ns)
        nd.parentNode.removeChild(ns)

def xmax(nd):
    limlow(nd, 'max')

def xsum(nd):
    n = etree.Element(NSM+'nary')
    getap(nd).append(n)
    
    np = etree.SubElement(n, NSM+'naryPr')
    ch = etree.SubElement(np, NSM+'chr')
    ch.set(NSM+'val', u'\u2211')
    subHide = etree.SubElement(np, NSM+'subHide')
    subHide.set(NSM+'val', '1')
    supHide = etree.SubElement(np, NSM+'supHide')
    supHide.set(NSM+'val', '1')
    
    e = etree.SubElement(n, NSM+'e')
    d = nd.ownerDocument.createDocumentFragment()
    setap(d, e)
    ns = nd.nextSibling
    
    try:
        for x in range(0,2):
            if ns.nodeName == 'active::_':
                s = etree.SubElement(n, NSM+'sub')
                subHide.set(NSM+'val', '0')
                setap(ns, s)
                ct.cnl(ns)
            elif ns.nodeName == 'active::^':
                s = etree.SubElement(n, NSM+'sup')
                supHide.set(NSM+'val', '0')
                setap(ns, s)
                ct.cnl(ns)
            else:
                while ns is not None:
                    d.appendChild(ns)
                    nd.parentNode.removeChild(ns)
                    ns = nd.nextSibling
                ct.cnl(d)
                return
            nd.parentNode.removeChild(ns)
            ns = nd.nextSibling
            if nd.nodeType==3 and ns.isspace():
                nd.parentNode.removeChild(ns)
                ns = nd.nextSibling

        while ns is not None:
            d.appendChild(ns)
            nd.parentNode.removeChild(ns)
            ns = nd.nextSibling
        ct.cnl(d)
        return
    except AttributeError:
        return

def xint(nd):
    narg(nd, u'\u222B')
    
def xprod(nd):
    narg(nd, u'\u220F')

def narg(nd, char):
    n = etree.Element(NSM+'nary')
    getap(nd).append(n)
    
    np = etree.SubElement(n, NSM+'naryPr')
    ch = etree.SubElement(np, NSM+'chr')
    ch.set(NSM+'val', char)
    subHide = etree.SubElement(np, NSM+'subHide')
    subHide.set(NSM+'val', '1')
    supHide = etree.SubElement(np, NSM+'supHide')
    supHide.set(NSM+'val', '1')
    
    e = etree.SubElement(n, NSM+'e')
    d = nd.ownerDocument.createDocumentFragment()
    setap(d, e)
    ns = nd.nextSibling
    
    try:
        for x in range(0,2):
            if ns.nodeName == 'active::_':
                s = etree.SubElement(n, NSM+'sub')
                subHide.set(NSM+'val', '0')
                setap(ns, s)
                ct.cnl(ns)
            elif ns.nodeName == 'active::^':
                s = etree.SubElement(n, NSM+'sup')
                supHide.set(NSM+'val', '0')
                setap(ns, s)
                ct.cnl(ns)
            else:
                while ns is not None:
                    d.appendChild(ns)
                    nd.parentNode.removeChild(ns)
                    ns = nd.nextSibling
                ct.cnl(d)
                return
            nd.parentNode.removeChild(ns)
            ns = nd.nextSibling
            if nd.nodeType==3 and ns.isspace():
                nd.parentNode.removeChild(ns)
                ns = nd.nextSibling

        while ns is not None:
            d.appendChild(ns)
            nd.parentNode.removeChild(ns)
            ns = nd.nextSibling
        ct.cnl(d)
        return
    except AttributeError:
        return
    
def xfunc(nd):
    s = nd.nextSibling.textContent
    n = nd.tagName
    if s:
        if s[0] not in {'(', '[', '{'}:
            getap(nd).append(txt.pmtr(n+u'\u2006'));
        else:
            getap(nd).append(txt.pmtr(n))
    else:
        getap(nd).append(txt.pmtr(n))

