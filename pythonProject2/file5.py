f = open("demofile2.txt", "r")
# Reading from the file
content = f.readlines()

# Variable for storing the sum
a = 0

# Iterating through the content
# Of the file
for line in content:

    for i in line:

        # Checking for the digit in
        # the string
        if i.isdigit():
            a += int(i)

print("The sum is:", a)