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









    
