# write a program that validates if a student is evidence and he is 36 years old
# and returns program name and code""

class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def print_student_details(self):

        print(self.age, self.name, self.number)


class Part1 (Student):

    def __init__(self, name, age):
        Student.__init__(self, name.name, age,)

Part1 = Student(input("enter name : \n"), int(input("enter Age : ")))
Part1.StNumber = "N0155555K"


class Program:
    def __init__(pr, code, name,):

        pr.code = code
        pr.name = name
Prog1 = Program("SSC", "Computer Science ")
if Part1.name == "evidence" and Part1.age == 36:
    print("Your name is : ", Part1.name, "You are :", Part1.age, "Years old ", "and Your student number is :"
    , Part1.StNumber)
    print("Your program code is : ", Prog1.code, "and your program name is : ", Prog1.name)
else:
    print("enter correct details")


















