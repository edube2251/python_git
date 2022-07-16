array1 = [6, 5, 4, 3, 2, 1]  # reverse function
print(array1.index(5))
array1.reverse()
print(array1)
print(array1.index(5))  # check item index
print(array1.count(1))

#  adding items in an array

sum = 0
for i in array1:
    sum = sum + i
print("sum of numbers in an array is ", sum)


# 42. Write a Python program to calculate the sum and average of n integer numbers (input from the user). Input 0 to
# finish.
sum = 0
avg = 0
lst1 = []

# For list of strings/chars
lst1 = [int(x) for x in input("Enter the list items separated by space : ").split(" ")] # how to impute an array
print("this is the list created from input", lst1)
print("\n")
for i in lst1:
    sum = sum + i
    avg = sum / (len(lst1))
print("Average of the above numbers are: ", avg)
print("\n")
print("sum of the above numbers are: ", sum)





