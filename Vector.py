

class Vector:
    # init function

    def __init__(self, labels, function):
        self.D = labels
        self.f = function

    def getitem(v,k):
        assert k in v.D
        if k in v.f.keys():
            return v.f[k]
        else:
            return 0
    def setitem(v,k,val):
        assert k in v.D
        v.f[k] = val

    def equal(u,v):
        assert u.D == v.D
        for x in u.D:
            if getitem(u, x) != getitem(v, x):
                return False
        return True

    def add(u,v):
        assert u.D == v.D
        add.dict = {}
        for k in u.D:
            add_dict[k] = getitem(u,k) + getitem(v,k)
        return Vec(u.D, add_dict)

    def dot(u,v):
        assert u.D == v.D
        return sum([getitem(v,k)*getitem(u,k) for k in u.D])

    def scalar_mul(v, alpha):
        return Vec(v.D, {i:alpha*getitem(v,i) for i in v.D})

    def neg(v):
        return Vec(v.D, {i:-1*getitem(v,i) for i in v.D})
            
    def __mul__(self,other):
        #If other is a vector, returns the dot product of self and other
        if isinstance(other, Vector):
            return dot(self,other)
        else:
            return NotImplemented  #  Will cause other.__rmul__(self) to be invoked

    # scalar division        
    def __truediv__(self,other):  
        return (1/other)*self

    __getitem__ = getitem
    __setitem__ = setitem
    __neg__ = neg
    __rmul__ = scalar_mul
    __add__ = add
    __eq__ = equal

    # sum() function for vectors
    def __radd__(self, other):
        if other == 0:
            return self

    # Returns the difference between a and b         
    def __sub__(a,b):
        return a+(-b)


    def is_almost_zero(self):
        s = 0
        for x in self.f.values():
            if isinstance(x, int) or isinstance(x, float):
                s += x*x
            elif isinstance(x, complex):
                s += x*x.conjugate()
            else: return False
        return s < 1e-20

    def __str__(v):
        D_list = sorted(v.D, key=repr)
        numdec = 3
        wd = dict([(k,(1+max(len(str(k)), len('{0:.{1}G}'.format(v[k], numdec))))) if isinstance(v[k], int) or isinstance(v[k], float) else (k,(1+max(len(str(k)), len(str(v[k]))))) for k in D_list])
        s1 = ''.join(['{0:>{1}}'.format(str(k),wd[k]) for k in D_list])
        s2 = ''.join(['{0:>{1}.{2}G}'.format(v[k],wd[k],numdec) if isinstance(v[k], int) or isinstance(v[k], float) else '{0:>{1}}'.format(v[k], wd[k]) for k in D_list])
        return "\n" + s1 + "\n" + '-'*sum(wd.values()) +"\n" + s2

    def __hash__(self):
        h = hash(frozenset(self.D))
        for k,v in sorted(self.f.items(), key = lambda x:repr(x[0])):
            if v != 0:
                h = hash((h, hash(v)))
        return h

    def __repr__(self):
        return "Vec(" + str(self.D) + "," + str(self.f) + ")"

    def copy(self):
        return Vector(self.D, self.f.copy())