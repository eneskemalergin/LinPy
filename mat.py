from Vec import Vec

class Matrix:
    def __init__(self, labels, function):
        self.D = labels
        self.f = function
    
    def add(A, B):
        assert A.D == B.D
        return Mat(A.D, { k:getitem(A,k)+getitem(B,k) for k in A.f.keys() | B.f.keys() })

    __add__ = add

    def scalar_mul(M, x):
        return Mat(M.D, {k:x*getitem(M,k) for k in M.f})

    def transpose(M):   
        return Mat((M.D[1], M.D[0]), {(q,p):v for (p,q),v in M.f.items()})
    
    transpose = transpose
    
    def vector_matrix_mul(v, M):
        assert M.D[0] == v.D
        result_vec = Vec(M.D[1], {})
        for (i,j) in M.f.keys():
            result_vec[j] = result_vec[j] + M[i,j] * v[i]
        return result_vec

    def matrix_vector_mul(M,v):
        assert M.D[1] == v.D
        result_vec = Vec(M.D[0],{})
        for (i,j) in M.f.keys():
            result_vec[i] = result_vec[i] + M[i,j] * v[j]
        return result_vec        
    
    def matrix_matrix_mul(A,B):
        assert A.D[1] == B.D[0]
        AB = Mat((A.D[0],B.D[1]), {})
        for i in A.D[0]:
            for j in B.D[1]:
                for n in A.D[1]:
                    AB[i,j] = AB[i,j] + A[i,n] * B[n,j]

        return AB
        
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


    def __radd__(self, other):
        if other == 0:
            return self

    def __sub__(a,b):
        return a+(-b)


    def copy(self):
        return Mat(self.D, self.f.copy())

        # String represnetation for print()
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

        # Evaluateable represenation
    def __repr__(self):
        return "Mat(" + str(self.D) +", " + str(self.f) + ")"

    def __iter__(self):
        raise TypeError('%r object is not iterable' % self.__class__.__name__)