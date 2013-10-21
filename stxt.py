from lxml import etree
from common import NSM, NSW, getap
import txt

_tum = {
        'Alpha'     : u'\u0391', 
        'Beta'      : u'\u0392', 
        'Gamma'     : u'\u0393', 
        'Delta'     : u'\u0394', 
        'Epsilon'   : u'\u0395', 
        'Zeta'      : u'\u0396', 
        'Eta'       : u'\u0397', 
        'Theta'     : u'\u0398', 
        'Iota'      : u'\u0399', 
        'Kappa'     : u'\u039A', 
        'Lambda'     : u'\u039B', 
        'Mu'        : u'\u039C', 
        'Nu'        : u'\u039D', 
        'Xi'        : u'\u039E', 
        'Omicron'   : u'\u039F', 
        'Pi'        : u'\u03A0', 
        'Rho'       : u'\u03A1', 
        'Sigma'     : u'\u03A3', 
        'Tau'       : u'\u03A4', 
        'Upsilon'   : u'\u03A5', 
        'Phi'       : u'\u03A6', 
        'Chi'       : u'\u03A7', 
        'Psi'       : u'\u03A8', 
        'Omega'     : u'\u03A9', 
        'alpha'     : u'\u03B1', 
        'beta'      : u'\u03B2', 
        'gamma'     : u'\u03B3', 
        'delta'     : u'\u03B4', 
        'epsilon'   : u'\u03F5', 
        'zeta'      : u'\u03B6', 
        'eta'       : u'\u03B7', 
        'theta'     : u'\u03B8', 
        'iota'      : u'\u03B9', 
        'kappa'     : u'\u03BA', 
        'lambda'     : u'\u03BB', 
        'mu'        : u'\u03BC', 
        'nu'        : u'\u03BD', 
        'xi'        : u'\u03BE', 
        'omicron'   : u'\u03BF', 
        'pi'        : u'\u03C0', 
        'rho'       : u'\u03C1', 
        'sigma'     : u'\u03C3', 
        'tau'       : u'\u03C4', 
        'upsilon'   : u'\u03C5', 
        'phi'       : u'\u03D5', 
        'chi'       : u'\u03C7', 
        'psi'       : u'\u03C8', 
        'omega'     : u'\u03C9', 
        'backslash' : '\\',
        '{'         : '{',
        '}'         : '}',
        '$'         : '$',
        '_'         : '_',
        '^'         : '^',
        'partial'   : u'\u2202',
        'LaTeX'     : 'LaTeX',
        'infty'     : u'\u221E',
        'in'        : u'\u2208',
        'le'        : u'\u2264',
        'cdots'     : u'\u22EF',
        'vdots'     : u'\u22EE',
        'ddots'     : u'\u22F1',
        'ldots'     : u'\u2026',
        'rightarrow': u'\u2192',
        'Re'        : u'\u211C',
        'times'     : u'\u00D7',
        'varepsilon': u'\u03B5',
        'ge'        : u'\u2265',
        '|'         : u'\u2016',
        ' '         : u'\u2008',
        'equiv'     : u'\u2261',
        'Box'       : u'\u25A1',
        'varphi'    : u'\u03C6',
        '\r'        : u'\u2008',
        'neq'       : u'\u2260',
        ';'         : u'\u2004',
        'cdot'      : u'\u2219',
        'leq'       : u'\u2264',
        'prime'     : u'\u2032',
        'approx'    : u'\u2248',
        '&'         : '&',
        'quad'      : u'\u2003',
        ','         : u'\u2006',
        'forall'    : u'\u2200',
        'exists'    : u'\u2203',
        'leftrightarrow' : u'\u2194',
        'pm'        : u'\u00B1',
}

def xstxt(nd):
    k = nd.nodeName
    v = _tum[k]
    getap(nd).append(txt.tr(v))
    

def updatect(ct):
    ctc = dict([(x, xstxt) for x in _tum.keys()])
    ct.update(ctc)
    
def xacchar(nd):
    getap(nd).append(txt.tr(nd.chars[nd.textContent]))
    
    
    
    
if __name__ == "__main__":
    k = _tum.keys()
    ctc = dict([(x, xtchar) for x in _tum.keys()])
    print len(ctc)
    
