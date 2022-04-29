# question 10
for i in range (50+1):
    if i % 3==0 and i % 5==0:
        print("fizzbuzz")
        continue
    elif i % 5==0:
        print("buzz")
        continue
    elif i % 3==0: 
        print()
        continue
print(i)

