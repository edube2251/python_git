a = "evidence dube"
gender = "male"
print(a.upper())  # upper case
print(a.lower())  # lowe case
print(a[:5])
print(a.split(), a.strip(), )
print(a.replace("e", "*"))  # string replace
print(a[::-1])  # negative indexing
print(a.upper()[0::])
print(a[2:len(a)])  # length of a string
print(a.center(50))  # tab
print(a + " " + gender)  # string concatenation
print(a.count("e"))  # number of letters in a string
# research on escape characters eg \n for new line
print(a[::-1])  # reverse string
for i in a:  # loop through
    print(i, end=" ")
for i in a:
    print(i)
list1 = {2, 3, 4, 5}
print(type(list1))  # check data type

# check on other string methods
# https://www.w3schools.com/python/python_strings_methods.asp
