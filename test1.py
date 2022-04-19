fruits={'apple','banana','graps','gwava'}
animals={'cow','goat','pig','cat','apple'}
#set union
frutsAnimals= fruits.union (animals)
print(frutsAnimals)
# intersection (elements in set animals and in fruits)
section = fruits. intersection(animals)
print('\n')                          
print(section)
#asymetric difference
x = fruits.symmetric_difference(animals)
print('\n')
print(x)
p=int(input('enetr the value of P \n'))

q = int(input ('enter the value of Q \n'))
print('\n')
y = p * q
print('the answer is : ' + str(y))

z = int(input('enter score'))

if z > 2 :
   print('you win')
else:
   print('you loose')







