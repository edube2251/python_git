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









    
