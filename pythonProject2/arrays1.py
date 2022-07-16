#  two-dimensional arrays
#  Two dimensional array is an array within an array
#  daily temperatures

"""Day 1 - 11 12 5 2
Day 2 - 15 6 10
Day 3 - 10 8 12 5
Day 4 - 12 15 8 6"""
#  output
#  T = [[11, 12, 5, 2], [15, 6,10], [10, 8, 12, 5], [12,15,8,6]]
#  from array import *

T = [[11, 12, 5, 2], [15, 6, 10], [10, 8, 12, 5], [12, 15, 8, 6]]

print(T[0])  # accessing the list in a list of a list

print(T[1][2])  # t[1] is the list, [2] index of an item to access in an array

#  To print out the entire two-dimensional array we can use python for loop as shown below.
T = [[11, 12, 5, 2], [15, 6, 10], [10, 8, 12, 5], [12, 15, 8, 6]]
p = T.pop([0][0])
print(T[0])
for r in T:
    for c in r:
        print(c, end=" ")
    print()

#  inserting values
#  We can insert new data elements at specific position by using the insert() method and specifying the index.
print("\n")
T = [[11, 12, 5, 2], [15, 6, 10], [10, 8, 12, 5], [12, 15, 8, 6]]

T.insert(2, [0, 5, 11, 13, 6])

for r in T:
    for c in r:
        print(c, end=" ")
    print()
#  updating values specific elements
T = [[11, 12, 5, 2], [15, 6, 10], [10, 8, 12, 5], [12, 15, 8, 6]]

T[2] = [11, 9]
T[0][3] = 7
for r in T:
    for c in r:
        print(c, end=" ")
    print()

#  deleting values
T = [[11, 12, 5, 2], [15, 6, 10], [10, 8, 12, 5], [12, 15, 8, 6]]

del T[3]

for r in T:
    for c in r:
        print(c, end=" ")
    print()


