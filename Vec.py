def list2vec(L):
    return Vec(set(range(len(L))), {k:L[k] for k in range(len(L))})

def zero_vec(D):
    return Vec(D, {})

# Return the value of specified index of vector
def getitem(v,k):
    assert k in v.D
    if k in v.f.keys():
        return v.f[k]
    else:
        return 0    

# No need to reassing, it will change.
def setitem(v,k,val):
    assert k in v.D
    v.f[k] = val

# Checks if given two vectors are equal or not
def equal(u, v):
    return u.D == v.D and u.f == v.f

def add(u,v):
    add_dict = {}
    for k in u.D:
        add_dict[k] = getitem(u, k) + getitem(v, k)
    return Vec(u.D, add_dict)


def dot(u,v):
    return sum([getitem(v,k)*getitem(u,k) for k in u.D])

def scalar_mul(v, alpha):
    return Vec(v.D, {i:alpha*getitem(v,i) for i in v.D})

def neg(v):
    return Vec(v.D, {i:-1*getitem(v,i) for i in v.D})


class Vec:
    """
    A vector has two fields:
    D - the domain (a set)
    f - a dictionary mapping (some) domain elements to field elements
        elements of D not appearing in f are implicitly mapped to zero
    """
    def __init__(self, labels, function):
        self.D = labels
        self.f = function

    __getitem__ = getitem
    __setitem__ = setitem
    __neg__ = neg
    __rmul__ = scalar_mul #if left arg of * is primitive, assume it's a scalar

    def __mul__(self,other):
        #If other is a vector, returns the dot product of self and other
        if isinstance(other, Vec):
            return dot(self,other)
        else:
            return NotImplemented  #  Will cause other.__rmul__(self) to be invoked

    def __truediv__(self,other):  # Scalar division
        return (1/other)*self

    __add__ = add

    def __radd__(self, other):
        if other == 0:
            return self

    def __sub__(a,b):
        return a+(-b)

    __eq__ = equal

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
        "pretty-printing"
        D_list = sorted(v.D, key=repr)
        numdec = 3
        wd = dict([(k,(1+max(len(str(k)), len('{0:.{1}G}'.format(v[k], numdec))))) if isinstance(v[k], int) or isinstance(v[k], float) else (k,(1+max(len(str(k)), len(str(v[k]))))) for k in D_list])
        s1 = ''.join(['{0:>{1}}'.format(str(k),wd[k]) for k in D_list])
        s2 = ''.join(['{0:>{1}.{2}G}'.format(v[k],wd[k],numdec) if isinstance(v[k], int) or isinstance(v[k], float) else '{0:>{1}}'.format(v[k], wd[k]) for k in D_list])
        return "\n" + s1 + "\n" + '-'*sum(wd.values()) +"\n" + s2

    def __hash__(self):
        "Here we pretend Vecs are immutable so we can form sets of them"
        h = hash(frozenset(self.D))
        for k,v in sorted(self.f.items(), key = lambda x:repr(x[0])):
            if v != 0:
                h = hash((h, hash(v)))
        return h

    def __repr__(self):
        return "Vec(" + str(self.D) + "," + str(self.f) + ")"

    def copy(self):
        return Vec(self.D, self.f.copy())
