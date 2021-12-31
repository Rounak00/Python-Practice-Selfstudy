#basically global keyword use for to change global variable value in local scope

x = 89
def harry():
    x = 20
    def rohan():
        global x
        x = 88
    # print("before calling rohan()", x)
    rohan()
    print("after calling rohan()", x)#print 20 bcz of local scope

harry()
print(x)#print 88
