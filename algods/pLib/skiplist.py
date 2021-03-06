# skiplist, for explanation refer to skiplistRank.py
import random
import math
import operator

class SkiplistNode:
    def __init__(self, level: int, val):
        self.val = val
        self.levels = [None for _ in range(level)]
    def __repr__(self):
        return str(self.val)

class Skiplist:
    def __init__(self, maxlevel=32, p=0.5, opt=operator.lt):
        self.MAXLEVEL = maxlevel
        self.P = p
        self.header = SkiplistNode(maxlevel, '/')
        self.length = 0
        self.opt_lt = opt

    def _find(self, val, opt):
        update = [self.header] * self.MAXLEVEL
        x = self.header
        for i in range(self.MAXLEVEL - 1, -1, -1):
            while x.levels[i]!=None and opt(x.levels[i].val, val):
                x = x.levels[i]
            update[i] = x
        return update

    def add(self, val):
        update = self._find(val, self.opt_lt)
        level = min(1-int(math.log(1/random.random(), self.P)), self.MAXLEVEL)
        x = SkiplistNode(level, val)
        for i in range(level):
            x.levels[i] = update[i].levels[i]
            update[i].levels[i] = x
        self.length += 1
        return x

    def discard(self, val):
        update = self._find(val, self.opt_lt)
        x = update[0].levels[0]
        if x==None or (self.opt_lt(x.val, val) or self.opt_lt(val, x.val)):
            return 0
        for i in range(len(x.levels)):
            update[i].levels[i] = x.levels[i]
        self.length -=1 
        return 1

    def bisect_right(self, val): return self._find(val, self.opt_le)[0].levels[0]
    def bisect_left(self, val): return self._find(val, self.opt_lt)[0].levels[0]
    def opt_le(self, lval, val): return not self.opt_lt(val, lval)
    def opt_eq(self, lval, val): return not self.opt_lt(val, lval) and not self.opt_lt(lval, val)
# below for debug
    def __iter__(self):
        """ iterate levels[0] in O(n),O(1) """
        x = self.header.levels[0]
        while x:
            yield x
            x=x.levels[0]
    def __len__(self): return self.length
    def __repr__(self):
        selflevel = self.MAXLEVEL
        while selflevel>1 and self.header.levels[selflevel-1]==None:
            selflevel -= 1
        mat = [[None]*(self.length+1) for _ in range(selflevel)]
        maxlen = 0
        for i,x in enumerate(self):
            for l in range(len(x.levels)):
                mat[l][i] = str(x)
                maxlen = max(maxlen, len(str(x)))
        
        sbuilder = []
        for level in mat[::-1]:
            level_sbuilder = []
            for e in level:
                if e!=None:
                    level_sbuilder.append(str(e).ljust(maxlen))
                else:
                    level_sbuilder.append("".ljust(maxlen))
            sbuilder.append("  ".join(level_sbuilder))

        return "-"*5+f" size:{self.length}  level:{selflevel} "+'-'*5+\
            '\n'+"\n".join(sbuilder)+'\n'+'-'*30

if __name__ == "__main__":
    d = [0,0,1]
    if d[0]:
        print("test case 1\n")
        z = Skiplist()
        z.add((9, 'a'))
        z.add((2, 'b'))
        z.add((1, 'd'))
        z.add((4, 'c'))
        z.add((5, 'e'))
        assert z.discard((1, 'd')) == 1
        assert z.discard((1, 'd')) == 0
        z.add((0, 'g'))
        print(z)
        
    if d[1]:
        print("test case 2\n")
        z2 = Skiplist()
        for e in 1,2,3,3,2,4,2:
            z2.add(e)
        print(z2)
        assert z2.discard(3)==1
        print(z2)
        assert z2.discard(3)==1
        print(z2)
        assert z2.discard(3)==0
        print(z2)
        print(z2.bisect_left(100))
        print(z2.bisect_left(-100))
        print(z2.bisect_right(100))
        print(z2.bisect_right(-100))
        print(z2.bisect_left(2))
        print(z2.bisect_right(2))
        print(list(z2))
    
    if d[2]:
        print("test case 2\n")
        z3 = Skiplist()
        for e in range(10):
            z3.add(e)
        v = z3.header.levels[0].val # O(1)
        print(v)
        z3.discard(v) # O(lg(n))
        print(z3)
        