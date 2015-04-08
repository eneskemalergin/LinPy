# Test
import vec

# Creating Zero Vector.
zeroVector = vec.zero_vec(('a', 'b', 'c', 'd'))
print(zeroVector)

print('-'*80)

# Creating Vectors with already defined values
vector = vec.Vec({'a', 'b', 'c', 'd'},{'a':1, 'b':2, 'c':3, 'd':4})
print(vector)

print('-'*80)

# Getting Specified indexe's value
print(vec.getitem(zeroVector, 'b'))

print('-'*80)

# Assinging item in specified region.
vec.setitem(zeroVector, 'b', 1)
print(zeroVector)

print('-'*80)

# Checks if equal or not
print(vec.equal(zeroVector, vector))

print('-'*80)

# Adds two vectors into one
print(vec.add(zeroVector, vector))

print('-'*80)

# get dot product of two vector:
print(vec.dot(zeroVector, vector))

print('-'*80)

# Multiply a vector by a constant
print(vec.scalar_mul(vector, 2))

print('-'*80)

# Gets the negation of a vector
print(vec.neg(vector))

# Add Length of the vector