#String index start from 0
#In python both single and double quote are string
mystr="Hello Sir"

print(mystr[1]) #print e

print(mystr[0:4])#its called string slicing (start from 0 and then stop at 4 dont print it so we need to take extra)

print(mtstr[0:8:2])#here last is skip sequence so its print =>   HloSr

print(mtstr[::-1])#Print in revverse order
"""*If we use negetive numbers in string slicing then its represent from back
   *if we use negetive in last skip sequence then it shows string fully from back with simple -1 and if we use -2 then from back but skip in every second character
   
"""

print(len(mystr))#print length

print(mystr.isalnum())#print false, tru if there is no spaces

print(mystr.isalpha())#print false

print(mystr.endwith("ir"))#print true bcz its end with 'ir'

print(mystr.count("l"))#prints 2

print(mystr.capitalize())#make capital only first alphabet

print(mystr.find("llo"))#only print start place index

print(mystr.lower())#make string in lowercase

print(mystr.upper())#make string in uppercase

print(mystr.replace("item","new item"))


"heloo my name is {name} and age is {age}".format(name="Rounak", age=25, weight=445)
