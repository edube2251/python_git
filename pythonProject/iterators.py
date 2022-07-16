class myNumbers:
    def __int__(self):
        self.a = 1
        return 1

    def __next__(self):
        if self.a <= 20:
            x = self.a
            self.a = self.a + 1
            return x

        else:
            raise StopIteration
myclass = myNumbers
myiter = iter(myclass)


for x in myiter:
    print(x)





