from common import NSW, NSM, npf, getap, setx, Body, mmf, setap
import ct, par

def xnewtheorem(nd):
    name = nd.attributes['name']
    ct.ct[name] = par.xtheorem