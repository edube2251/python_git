<<<<<<< HEAD
# dictionary practice

MyCar = {
    "Brand":"Nissan_march",
    "model" : "K11",
    "Year"  : "2008",
    "color" : "Blue"
    }
print(MyCar)
print("\n")

# dispay length

print(len(MyCar))
print("\n")
#Get the value of the "model" key:

x = MyCar.get("model")
print(x)
print()
#Get a list of the keys:
p = MyCar.keys()

print(p)
print("\n")
#add key and a value

MyCar["engine"]="2cam"

print(MyCar)
print("\n")
#print values
f= MyCar.values()
print(f)
print("\n")
#Make a change in the original dictionary
MyCar["Year"]= "2012"
print(MyCar)
print("\n")
#Get a list of the key:value pairs
s= MyCar.items()
print(s)
print("\n")
#remove items
MyCar.pop("engine")
print(MyCar)









    
=======
# dictionary practice

MyCar = {
    "Brand":"Nissan_march",
    "model" : "K11",
    "Year"  : "2008",
    "color" : "Blue"
    }
print(MyCar)
print()
# dispay length

print(len(MyCar))
print()
#Get the value of the "model" key:

x = MyCar.get("model")
print(x)
print()
#Get a list of the keys:
p = MyCar.keys()

print(p)
print()
#add key and a value

MyCar["engine"]="2cam"

print(MyCar)
print()
#print values
f= MyCar.values()
print(f)
print()
#Make a change in the original dictionary
MyCar["Year"]= "2012"
print(MyCar)
print()
#Get a list of the key:value pairs
s= MyCar.items()
print(s)
print()
#remove items
MyCar.pop("engine")
print(MyCar)









    
>>>>>>> 762bfa2697b800dc6d67d8120951101c8ebdd6f0
