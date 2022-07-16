f = open("c:\port.txt", "r")

d1 = {}  # create an empty dictionary

for line in f:  # Use for loop to read the contents of the file line by line.
    words = line.split()
    print(words)

    for words in words:
        if words in d1:
            d1[words] = d1[words] + 1
        else:
            d1[words] = 1

print(d1)
