from vec import Vec

# Creates and identity matrix
def identity(D, ):
    return Mat((D,D), {(d,d):1 for d in D})
# Supportive Function
def keys(d):
    #return d.keys() if isinstance(d, dict) else range(len(d))
    if isinstance(d, dict):
        return d.keys()
    else:
        return range(len(d))


# Supportive Function
def value(d):
    return next(iter(d.values())) if isinstance(d, dict) else d[0]

# Mapps the matrix bases on row
def mat2rowdict(A):
    return {row:Vec(A.D[1], {col:A[row,col] for col in A.D[1]}) for row in A.D[0]}

# Mapps the matrix bases on column
def mat2coldict(A):
    return {col:Vec(A.D[0], {row:A[row,col] for row in A.D[0]}) for col in A.D[1]}

# Converts dictionary that bases on column into matrix
def coldict2mat(coldict):
    row_labels = value(coldict).D
    return Mat((row_labels, set(keys(coldict))), {(r,c):coldict[c][r] for c in keys(coldict) for r in row_labels})

# Converts dictionary that bases on row into matrix
def rowdict2mat(rowdict):
    col_labels = value(rowdict).D
    return Mat((set(keys(rowdict)), col_labels), {(r,c):rowdict[r][c] for r in keys(rowdict) for c in col_labels})

def efficient_rowdict2mat(rowdict):
    col_labels = value(rowdict).D
    M = Mat((set(keys(rowdict)), col_labels), {})
    for r in rowdict:
        for c in rowdict[r].f:
            M[r,c] = rowdict[r][c]
    return M

# Converts nested list into matrix
def listlist2mat(L):
    m,n = len(L), len(L[0])
    return Mat((set(range(m)),set(range(n))), {(r,c):L[r][c] for r in range(m) for c in range(n)})

def submatrix(M, rows, cols):
    return Mat((M.D[0]&rows, M.D[1]&cols), {(r,c):val for (r,c),val in M.f.items() if r in rows and c in cols})

def equal(A, B):
    assert A.D == B.D
    for k in A.f.keys() | B.f.keys():
        if A[k] != B[k]:
            return False

    return True

def getitem(M, k):
    assert k[0] in M.D[0] and k[1] in M.D[1]
    if k in M.f:
        return M.f[k]
    else:
        return 0

def setitem(M, k, val):
    assert k[0] in M.D[0] and k[1] in M.D[1]
    M.f[k] = val


def add(A, B):
    assert A.D == B.D
    return Mat(A.D, { k:getitem(A,k)+getitem(B,k) for k in A.f.keys() | B.f.keys() })

def scalar_mul(M, x):
    return Mat(M.D, {k:x*getitem(M,k) for k in M.f})

def transpose(M):
    return Mat((M.D[1], M.D[0]), {(q,p):v for (p,q),v in M.f.items()})

def vector_matrix_mul(v, M):
#    assert M.D[0] == v.D
    result_vec = Vec(M.D[1], {})
    for (i,j) in M.f.keys():
        result_vec[j] = result_vec[j] + M[i,j] * v[i]
    return result_vec

def matrix_vector_mul(M, v):
#    assert M.D[1] == v.D
    result_vec = Vec(M.D[0],{})
    for (i,j) in M.f.keys():
        result_vec[i] = result_vec[i] + M[i,j] * v[j]
    return result_vec

def matrix_matrix_mul(A, B):
#    assert A.D[1] == B.D[0]
    AB = Mat((A.D[0],B.D[1]), {})
    for i in A.D[0]:
        for j in B.D[1]:
            for n in A.D[1]:
                AB[i,j] = AB[i,j] + A[i,n] * B[n,j]

    return AB

################################################################################

class Mat:
    def __init__(self, labels, function):
        self.D = labels
        self.f = function

    __getitem__ = getitem
    __setitem__ = setitem
    transpose = transpose

    __len__ = len
    def __neg__(self):
        return (-1)*self

    def __mul__(self,other):
        if Mat == type(other):
            return matrix_matrix_mul(self,other)
        elif Vec == type(other):
            return matrix_vector_mul(self,other)
        else:
            return scalar_mul(self,other)
            #this will only be used if other is scalar (or not-supported). mat and vec both have __mul__ implemented

    def __rmul__(self, other):
        if Vec == type(other):
            return vector_matrix_mul(other, self)
        else:  # Assume scalar
            return scalar_mul(self, other)

    __add__ = add

    def __radd__(self, other):
        if other == 0:
            return self

    def __sub__(a,b):
        return a+(-b)

    __eq__ = equal

    def copy(self):
        return Mat(self.D, self.f.copy())

    # When calling print(), __str__ function works.    
    def __str__(M, rows=None, cols=None):
        if rows == None: rows = sorted(M.D[0], key=repr)
        if cols == None: cols = sorted(M.D[1], key=repr)
        separator = ' | '
        numdec = 3
        pre = 1+max([len(str(r)) for r in rows])
        colw = {col:(1+max([len(str(col))] + [len('{0:.{1}G}'.format(M[row,col],numdec)) if isinstance(M[row,col], int) or isinstance(M[row,col], float) else len(str(M[row,col])) for row in rows])) for col in cols}
        s1 = ' '*(1+ pre + len(separator))
        s2 = ''.join(['{0:>{1}}'.format(str(c),colw[c]) for c in cols])
        s3 = ' '*(pre+len(separator)) + '-'*(sum(list(colw.values())) + 1)
        s4 = ''.join(['{0:>{1}} {2}'.format(str(r), pre,separator)+''.join(['{0:>{1}.{2}G}'.format(M[r,c],colw[c],numdec) if isinstance(M[r,c], int) or isinstance(M[r,c], float) else '{0:>{1}}'.format(M[r,c], colw[c]) for c in cols])+'\n' for r in rows])
        return '\n' + s1 + s2 + '\n' + s3 + '\n' + s4

    def pp(self, rows, cols):
        print(self.__str__(rows, cols))

    def __repr__(self):
        "evaluatable representation"
        return "Mat(" + str(self.D) +", " + str(self.f) + ")"

    def __iter__(self):
        raise TypeError('%r object is not iterable' % self.__class__.__name__)
