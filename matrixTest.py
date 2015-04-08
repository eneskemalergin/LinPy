import mat
from vec import Vec

# Creating a initial matrix by using class definition
a = mat.Mat(({1, 2}, {1, 2}), {(1, 2): 3})
print(a)

""" Supportative Functions Tests """
# They will be using for main functions

# Returns an identity matrix
# Takes only Dimensions
print(mat.identity({0,1,2}))

# converts matrix to row dictionary to convert to vector
print(mat.mat2rowdict(a))

# converts matrix to column dictionary to convert to vector
print(mat.mat2coldict(a))

# Converts a dictionary bases column into matrix
coldict = {0:Vec({0,1},{0:1,1:2}),1:Vec({0,1},{0:3,1:4})}
print(mat.coldict2mat(coldict))

# Convert a dictionary bases row into matrix
rowdict = {0:Vec({0,1},{0:2,1:4}),1:Vec({0,1},{0:6,1:8})} 
print(mat.rowdict2mat(rowdict))

# Converts nested lists into matrix
# 2 row by 2 list subset
# 4 column by 4 element from each
listlist_L = [[10,20,30,40],[50,60,70,80]] 
print(mat.listlist2mat(listlist_L)) 


b = mat.rowdict2mat(rowdict)

# Checks if 2 matrix are equal
print(mat.equal(a,b))
