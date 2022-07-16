class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        print("Good morning mr :", self.name, "you are ", str(self.age), "years old")


p1 = Person("Evidence", 36)
print(p1.age)


class Student(Person):
    def __init__(self, name, age):
        Person.__init__(self, name, age)
        Student.enrollementYear = 2020


s1 = Student("Prince", 20)
(s1.greet())
print(s1.name, "You enrolled for your course in  : ", s1.enrollementYear)


class Graduate(Person):
    def __init__(self, name, age):
        Person.__init__(self, name, age)
        Graduate.graduationayear = 2021
        Graduate.occupation = "Database administrator"
        Graduate.speciality = "sql server administration"


g1 = Graduate("Martine", 30)
print(g1.name, "you graduated in : ",Graduate.graduationayear,"your occupation is ", Graduate.occupation)
