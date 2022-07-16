#  Data in a computer is stored in files
#   differ in content and file extensions
#   Files are usually stored in folders (or directories).
#   Write a program to count the number of lines in a text file.
#   Write a program to count the frequency of each word in a text file.
#   Write out text data using a print statement with additional file attribute.
#   Opening and Closing Files

#   Python has several functions for creating, reading, updating, and deleting files.

f = open("C:\port.txt", "r") as f:
# print(f.read())  # By default, the read() method returns the whole text, but you can also specify how many characters
# you want to return:
# print(f.readline()) # read line by line
# print(f.readline()) # print next line
s = len(f.readline())
print(s)

for x in f:
    print(x)

f.close()  # It is a good practice to always close the file when you are done with it.
