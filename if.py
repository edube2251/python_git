# If statements

a = int(input("enter value of a \n "))
b = int(input("enter value of b \n "))

if b > a:
  print(str(b) + " is greater than "+ str(a))
elif a == b:
  print(str(a) + " and " + str (b)+  " are equal ")
else:
  print(str(a)+ " is greater than " + str(b))
