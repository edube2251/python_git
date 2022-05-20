# 42. Write a Python program to calculate the sum and average of n integer numbers (input from the user). Input 0 to finish.
sum = 0
avg = 0
lst1 = []

# For list of strings/chars
lst1 = [int(item) for item in input("Enter the list items separated by space : ").split(" ")]
print("\n")
for i in lst1:
    sum = sum + i
    avg = sum / (len(lst1))
print("Average of the above numbers are: ", avg)
print("\n")
print("sum of the above numbers are: ", sum)

	


