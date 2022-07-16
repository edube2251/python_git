#   Python does not have built-in support for Arrays, but Python Lists can be used instead.
#   An array is a special variable, which can hold more than one value at a time.
subjects = ["history", "science", "geograpy", "maths"]
x = subjects[0]
print(x)

subjects[3]= "ndebele"
print(subjects)
p = len(subjects)
print(p)

for x in subjects:
    print(x)
subjects.pop(3)
subjects.remove("science")
