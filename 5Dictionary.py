#Dictionary is key value pairs

di={"even":2, "odd":2, "complex":{"x":"5x-j","y":"5x-j"}}

print(di[even])#print the first index here so prints 2
print(di[complex])#print whole dict of complex
print(di[complex][x])#we can print internat dict like this

di[imaginary]="5i" #add in the dict

del di[even] #for remove

"""now think we have di2 and di2=di then if we delete an element from di2 then that element also delete from di bcz both are pointers and point in memory so thats why we use copy"""
di2=di.copy()

print(di.get("odd"))#the only return value

di.update({"prime":2})#for add or update

print(di.keys())#only keys in a form of array

print(di.values())#only values in a form of array

print(di.items())# key and value in pair form of array

