from lxml import etree
from common import NSM, setx, mmf, NSW, getap, ntf, setap, Body
from copy import deepcopy
import ct, txt

def xhspace(nd):
    s = nd.attributes['len']
    n = int(s.em*6)
    t = txt.tr(u"\u2006"*n)
    getap(nd).append(t)
    
    