# Datatypes
basic-> Integer, Complex, float, boolean, string
container-> List, tupples, set, dictionary
user defined-> Class

# example of complex
print(4+5j)#4+5j
______________________________________________________________________________________________________________________________________

var = "Hello"
print(var)#so in python we dont need any datatype intialization


print(type(var))#print the datatype

#typecasting:
var2="32"
print(int(var2))


print(10*"Hello")#print ten times, only valid by string



#take in put
 var name= input("Enter your num") # in this way input taken as string
 varname= int(input("Enter your number"))#in this way we can take number input and for other datatypes we need to specify datatype here


#and we have normal arithmatic sign for calculations like +,-,*,/,%, ** (Exponent/use as power), // (Floor Division/ 9//2 = 4 and 9.0//2.0 = 4.0, -11//3 = -4, -11.0//3 = -4.0)

""" Normal SWAP using coma
    
    a=12
    b=25
    a, b=b, a
    print(a,b)
"""
# Multiline declartion
# 1. a=b=c=6
# 2. a,b,c=5,6,7
# 3. a=5;b=6;c=7

#there are membership operators which are 'in' and 'not in'

#in python we write and and or symbol as 'and' and 'or' keywords

# Keywords in pythn (Case sensitive)
import keyword, sys
print(keyword.kwlist)

[False, None, True, and, as, assert, async, await, break, class,
continue, def, del, elif, else, except, finally, for, from, global,
if, import, in, is, lambda, nonlocal, not, or, pass, raise, return,
try, while, with, yield]


# Operations
+,-,/,*,**,//,and,or,not,is, is not, &,|,~,<<,>>, in , not in
