#  A function is a block of code which only runs when it is called.
#  You can pass data, known as parameters, into a function.
# A function can return data as a result.
def my_function():
    """demonstrate how to declare function in python"""
    print("Hello from a function")

# my_function()
print("Using __doc__:")
print(my_function().__doc__)


#  A parameter is the variable listed inside the parentheses in the function definition
#  An argument is the value that is sent to the function when it is called.
#  parameters = arguments

def my_function(name, surname):  # we use def to define a function , name and surname are parameter
    print(name + " " + surname + "  this is your name and surname")


my_function(name=input("Enter your first name \n "), surname=input("Enter your first surname name \n "))  # name and


# surname on calling function method are known as arguments, and they are passed to the function

# arbitrary arguments


def my_kids(*kids):  # If the number of arguments is unknown, add a * before the parameter name:
    print("The youngest child is " + kids[2])


my_kids("Emil", "Tobias", "Linus")


# You can also send arguments with the key = value syntax.
# This way the order of the arguments does not matter.

def my_relatives(relative1, relative2, relative3):
    print("My favorite relative is " + relative3)


my_relatives(relative1="Evidence", relative2="bettina", relative3="vimbai")  # relative3 is key and vimbai is value


# If the number of keyword arguments is unknown, add a double ** before the parameter name:
def my_kids1(**kid):  # This way the function will receive a dictionary of arguments, and can access the items
    # accordingly:Example
    print(("His last name is " + kid["lname"]))


my_kids1(fname="mandla", lname="ndlovu")


# default parameters
def my_country(country="zimbabwe"):
    print("i am from " + country)


my_country("sweden")
my_country()  # If we call the function without argument, it uses the default value:


# passing alist as na argument
def my_food(food):
    for x in food:
        print(x)


fruits = ["mango", "banana", "apple"]

my_food(fruits)


#  return values
def my_return(x):
    return 5 * x


print(my_return(10))


# research on recursive functions
def addition(num):
    if num:
        # call same function by reducing number by 1
        return num + addition(num - 1)
    else:
        return 0


res = addition(10)
print(res)

# find max value in a list
x = [4, 6, 8, 24, 12, 2]
print(max(x))

# find min value in a list
x = [4, 6, 8, 24, 12, 2]
print(min(x))
# absolute positive value

x = abs(-7.25)
print(x)

# power of a value
x = pow(4, 3)
print(x)


