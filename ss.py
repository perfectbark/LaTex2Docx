from copy import deepcopy
from lxml import etree
from common import NSM, setx, mmf, NSW, getap, ntf, setap
import ct, txt

def xsub(nd):
    #if nd.previousSibling.nodeName == 'lim':
        #setap(nd, nd.previousSibling.getUserData('ap'))
        #ct.cnl(nd)
        #return
    ss = setbase(nd)
    if ss is None:
        return
    s = etree.Element(NSM+'sub')
    setx(nd, s, s)
    ct.cnl(nd)
    ss.append(s)

def xsup(nd):
    ss = setbase(nd)
    if ss is None:
        return
    s = etree.Element(NSM+'sup')
    setx(nd, s, s)
    ct.cnl(nd)
    ss.append(s)

def setbase(nd):
    p = getap(nd)
    if len(p)==0:
        x = txt.tr(u'\u200B')
        p.append(x)
    else:
        x = p[-1]
    
        n = nd.previousSibling.nodeName
        if n=='active::_' or n=='active::^':
            return x
        if n=='#text':
            t = x.find(NSM+'t')
            tt = t.text
            if len(tt)>1:
                tt1 = tt[-1]
                x1 = deepcopy(x)
                t1 = x1.find(NSM+'t')
                t1.text = tt1
                t.text = tt[:-1]
                x = x1
            else:
                p.remove(x)
        else:
            p.remove(x)
    
    if nd.nodeName == 'active::_':
        if nd.nextSibling == None:
            s = etree.Element(NSM+'sSub')
            e = etree.SubElement(s, NSM+'e')
            e.append(x)
            p.append(s)
        elif nd.nextSibling.nodeName != 'active::^':
            s = etree.Element(NSM+'sSub')
            e = etree.SubElement(s, NSM+'e')
            e.append(x)
            p.append(s)
        else:
            s = etree.Element(NSM+'sSubSup')
            e = etree.SubElement(s, NSM+'e')
            e.append(x)
            p.append(s)
    elif nd.nodeName == 'active::^':
        if nd.nextSibling==None:
            s = etree.Element(NSM+'sSup')
            e = etree.SubElement(s, NSM+'e')
            e.append(x)
            p.append(s)
        elif nd.nextSibling.nodeName != 'active::_':
            s = etree.Element(NSM+'sSup')
            e = etree.SubElement(s, NSM+'e')
            e.append(x)
            p.append(s)
        else:
            s = etree.Element(NSM+'sSubSup')
            e = etree.SubElement(s, NSM+'e')
            e.append(x)
            p.append(s)
    return s    