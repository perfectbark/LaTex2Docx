from plasTeX.TeX import TeX
#from Common import NSW, NSM, Document, Body, npf
#from lxml import etree
#from T2U import t2uct, xtchar, t2uctw
#from Numbering import xenumerate
#import Equation
import docx, txt, par, stxt, mm, ss, space, enum, dfn


ct =  {
      '#document' : docx.xdoc,
      'document' : docx.xdocument,
      '#text' : txt.xtext,
      'par' : par.xpar,
      'emph': txt.xit,
      'equation': mm.xequation,
      'math':mm.xmath,
      'section' : par.xsection,
      'displaymath' : mm.xdisplaymath,
      'title' : par.xtitle,
      'author' : par.xauthor,
      'it' : txt.xit,
      'active::_':ss.xsub,
      'active::^':ss.xsup,
      'frac':mm.xfrac,
      '\\' : par.xbr,
      'maketitle' : par.xmaketitle,
      'date' : par.xdate,
      'text' : mm.xtext,
      'texttt': txt.xtexttt,
      'delim' : mm.xdelim,
      'array' : mm.xarray,
      'ArrayRow' : mm.xArrayRow,
      'ArrayCell' : mm.xArrayCell,
      'mbox' : mm.xtext,
      'eqnarray' : mm.xeqnarray,
      'hspace' : space.xhspace,
      'enumerate' : enum.xenumerate,
      'item' : enum.xitem,
      'bgroup' : txt.xbgroup,
      'quote' : par.xquote,
      'bf' : txt.xbf,
      'itemize' : enum.xitemize,
      'newtheorem' : dfn.xnewtheorem,
      'bar'        : mm.xbar,
      'em'         : txt.xem,
      'ref'        : mm.xref,
      'abstract'   : par.xabstract,
      'lim'        : mm.xlim,
      'eqnarray*'  : mm.xeqnarray,
      'over'       : mm.xfrac,
      'sum'        : mm.xsum,
      'rm'         : mm.xtext,
      'min'        : mm.xmin,
      'int'        : mm.xint,
      'hat'        : mm.xhat,
      'thebibliography' : par.xthebibliography,
      'bibitem'    : par.xbibitem,
      'thanks'     : par.xthanks,
      'footnote'   : par.xthanks,
      'max'        : mm.xmax,
      }

stxt.updatect(ct)


def unknowntag(nd):
    if nd.nodeType == 1:
        if nd.nodeName in {'def', 'label', 'usepackage', 'documentclass'}:
            return
        else:
            print ' id:', nd.id, 'Name:', nd.nodeName
    else:
        print 'Name:', nd.nodeName, 'Value:', nd.nodeValue
    
def cnd(nd):
    if nd.nodeName in ct:
        ct[nd.nodeName](nd)
    else:
        unknowntag(nd)
        
def cnl(nd):
    for ne in nd.childNodes:
        ne.parentNode = nd
    for ne in nd.childNodes:
        cnd(ne)