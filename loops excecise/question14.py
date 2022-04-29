# question 1
s = input("Input a string  ")
d=0
c=0
for i in s:
    if i.isdigit():
        d = d + 1
    elif i.isalpha():
        c = c+1
    else:
        pass
print("Letters " , c)
print("Digits ", d)
