list1 = ["apple", "banana", "cherry", "orange", "kiwi", "melon", "mango"]  # declare list
j = 0
print(list1)
print(type(list1))  # check data type
print(len(list1))
print(list1[0])  # access list
print(list1[-1])  # access list item using negative indexing
list1.append("student")  # add to alist
print(list1)
list1.remove("banana")  # remove item
print(list1)
list1.pop(1)  # remove item
print(list1)
print(list1[2:5])  # access items using range of index 2 included 5 not included
list1[0] = "banana"
print(list1)
list1.insert(0, "umviyo")
print(list1)
for i in range(len(list1)):  # loop using index and len
    print(list1[i])

while j < len(list1):
    print(list1[j], end=" ")
    j = j + 1
print("list comprehension", (x for x in list1))  # list comprehension
# homework list sorting
list2 = list1.copy()  # create a copy of list1
print(list2)
list3 = [1, 2, 3, 4]
list4 = list1 + list3
print(list4)
list5 = []
list5.extend(list3)
print(list5, "tis is list5")

# x = range(3, 20, 2)  # (start,stop,step)
# for n in x:
#  print(n)
