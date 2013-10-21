import re, copy

    
class Font(object):
    def __init__(self):
        self.unit = 1
        self.name = ''
        
class GraphicsState(object):
    def __init__(self):
        self.font = None
        self.colorSpace = 'DeviceGray'
        self.linewidth = 0
        self.path = []
        self.color = [0, 0, 0, 0]
        self.cx = None
        self.cy = None
        
class Ent(object):
    UNKNOWN = -1
    OPERATOR = 0
    NAME = 1
    NUMBER = 2
    ARRAY = 3
    STRING = 4
    FONT = 5
    SAVE = 6
    
    def __init__(self):
        self.value = None
        self.entType = Ent.UNKNOWN

class Eps(object):
    def __init__(self, name=''):
        self.operandStack = []
        self.actions = []
        self.ents = []
        self.opDict = dict()
        self.gs = GraphicsState()
        self.gsStack = []
        self.ondraw = self.nothing
        if name:
            self.load(name)
            
    def nothing(self, gs, cmd):
        return
            
    def load(self, fn):
        num = re.compile(r"^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$")
        with open(fn, 'r') as f:
            el = self.ents
            es = [el]
            ts = ''
            tf = False
            for s in self.genToken(f):
                #print s
                if tf:
                    if s[0] == ')':
                        e = Ent()
                        e.entType = Ent.STRING
                        e.value = ts
                        el.append(e)
                        tf = False
                    ts = ts + s
                elif s[0] == '(':
                    ts = ''
                    tf = True
                elif s[0] == '/':
                    e = Ent()
                    e.entType = Ent.NAME
                    e.value = s[1:]
                    el.append(e)
                elif s[0] == '{':
                    e = Ent()
                    e.entType = Ent.ARRAY
                    e.value = []
                    el.append(e)
                    el = e.value
                    es.append(el)
                elif s[0] == '}':
                    es.pop()
                    el = es[-1]
                elif num.match(s):
                    e = Ent()
                    e.entType = Ent.NUMBER
                    e.value = s
                    el.append(e)
                else:
                    e = Ent()
                    e.entType = Ent.OPERATOR
                    e.value = s
                    el.append(e)
            #print '=========================='
            #for e in el:
                #if e.entType == Ent.OPERATOR:
                    #print e.value
            
            self.runps(self.ents)
                
                    
            
    def genToken(self, lf):
        lstr = ''
        instr = False
        while 1:
            try:
                l = lf.readline()
            except StopIteration:
                l = ''
                
            if not l:
                break

            s, p, m = 0, 0, len(l)
            while p<m:
                if instr:
                    if l[p] == ')':
                        if lstr:
                            yield lstr
                            lstr = ''
                        else:
                            yield l[s:p]
                        yield ')'
                        s = p + 1
                        p = s
                        instr = False
                    elif l[p] in '\r\n':
                        lstr = lstr + l[s:p]
                        break
                    else:
                        p = p + 1
                    continue
                
                if l[p] in '%\r\n':
                    if s < p:
                        yield l[s:p]
                    break
                if l[p] == ' ':
                    if s==p:
                        s = s+1
                        p = p+1
                    else:
                        yield(l[s:p])
                        s = p+1
                        p = s
                elif l[p] in '{}[]':
                    if s == p:
                        yield l[p]
                        s = p + 1
                        p = p + 1
                    else:
                        yield l[s:p]
                        yield l[p]
                        s = p + 1
                        p = s
                elif l[p] == '(':
                    instr = True
                    yield '('
                    s = p + 1
                    p = s
                else:
                    p = p+1
            else:
                if s < p:
                    yield l[s:p]
                        

    def runps(self, array):
        for o in array:
            if o.entType == Ent.OPERATOR:
                n = 'op'+o.value
                try:
                    getattr(self, n)()
                except AttributeError:
                    if o.value in self.opDict:
                        self.runps(self.opDict[o.value])
                    else:
                        print 'unknown opcode:', o.value
            else:
                self.operandStack.append(o)


    def opdef(self):
        v = self.operandStack.pop()
        k = self.operandStack.pop()
        self.opDict[k.value] = v.value
        
    def opfindfont(self):
        e = Ent()
        p = self.operandStack.pop()
        f = Font()
        f.name = p.value
        e.value = f
        e.entType = Ent.FONT
        self.operandStack.append(e)
        
    def opmul(self):
        e = Ent()
        p2 = self.operandStack.pop()
        p1 = self.operandStack.pop()
        e.value = float(p2.value)*float(p1.value)
        e.entType = Ent.NUMBER
        self.operandStack.append(e)
        
    def opscalefont(self):
        s = int(self.operandStack.pop().value)
        self.operandStack[-1].value.unit = s
        
    def opsetfont(self):
        f = self.operandStack.pop().value
        self.gs.font = f    
        
    def opsetrgbcolor(self):
        self.gs.colorSpace = 'DeviceRGB'
        self.gs.color[2] = float(self.operandStack.pop().value)
        self.gs.color[1] = float(self.operandStack.pop().value)
        self.gs.color[0] = float(self.operandStack.pop().value)
        
    def opsave(self):
        e = Ent()
        e.entType = Ent.SAVE
        e.value = None
        self.gsStack.append(copy.copy(self.gs))
        self.operandStack.append(e)
        
    def opmoveto(self):
        y = self.operandStack.pop().value
        x = self.operandStack.pop().value
        self.gs.path.append([x, y, 'moveto'])
        self.gs.cx = float(x)
        self.gs.cy = float(y)
        
    def opnewpath(self):
        self.gs.path = []
        
    def oplineto(self):
        y = self.operandStack.pop().value
        x = self.operandStack.pop().value
        self.gs.path.append([x, y, 'lineto'])
        self.gs.cx = float(x)
        self.gs.cy = float(y)
        
    def opstroke(self):
        self.ondraw(self.gs, ['stroke'])

    def oparc(self):
        a2 = self.operandStack.pop().value
        a1 = self.operandStack.pop().value
        r = self.operandStack.pop().value
        y = self.operandStack.pop().value
        x = self.operandStack.pop().value
        self.gs.path.append([x, y, r, a1, a2, 'arc'])
        
    def opclosepath(self):
        self.gs.path.append(['closepath'])
        
    def opshow(self):
        s = self.operandStack.pop().value
        self.ondraw(self.gs, [s, 'show'])
        
    def oprestore(self):
        s = self.operandStack.pop().value
        self.gs = self.gsStack.pop()
        
    def opshowpage(self):
        self.ondraw(self.gs, ['showpage'])
        

if __name__ == "__main__":
    e = Eps('a.eps')