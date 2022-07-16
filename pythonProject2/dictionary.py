cars = {
    "model": "nissan",
    "year": 2012
}
print(cars)
# model = key and nissan = value
print(cars["year"])  # accessing year value we use year as key
x = cars.get("model")  # print model value
print(x)  # using get function
b = cars.keys()  # print keys
print(b)
cars["colour"] = "white"  # # modify value
c = cars.values()  # print values
print(c)
z = cars.items()  # it returns a tuple of key:value in a list
print(z)
cars["year"] = 2008  # modify value
print(z)
cars.pop("model")  # remove item in a dictionary
print(z)

for x in cars.keys():  # Loop through dictionary
    print(x)
