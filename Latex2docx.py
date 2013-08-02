from plasTeX.TeX import TeX
from lxml import etree
import ct, docx
from common import Document
import sys, os

try:
    tf = sys.argv[1]
except:
    print 'useage: Latex2docx texfile'
    sys.exit(0)

try:
    df = os.path.splitext(tf)[0]
    td = TeX(file=tf)
    td = td.parse()
    ct.cnd(td)
    docx.save(df)
except OSError as oe:
    print oe
except IOError as oe:
    print oe
