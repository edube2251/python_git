import os

#  "a" - Append - will append to the end of the file

#  "w" - Write - will overwrite any existing content

f = open("demofile2.txt", "a")
f.write("Now the file has more content!")
f.close()

# open and read the file after the appending:
f = open("demofile2.txt", "r")
print(f.read())

# to create a file

# "x" - Create - will create a file, returns an error if the file exist

# "a" - Append - will create a file if the specified file does not exist

# "w" - Write - will create a file if the specified file does not exist

x = open("myfile.txt", "w")
x.write("this is my second file")
x.close()
x = open("myfile.txt", "r")
print(x.read())


# os.remove("myfile.txt") # deleting a file

# os.rmdir("test") # deleting a folder

