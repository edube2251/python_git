# mark classification:
mark = 0
mark = int(input(" Please enetr you mark "))
if mark < 0 :
    print(" YOU CANT ENTER A NEGETIVE MARK ")
elif mark < 50:
    print(" FAIL ")
elif mark < 60 :
    print(" PASS ")
elif mark < 70:
    print(" CREDIT ")
elif mark <= 100 :
    print(" DISTINTION ")
else:
    print("pecertange is out of 100, please enter correct mark ")
