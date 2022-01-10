#map:
items = [1, 2, 3, 4, 5]
a=list(map((lambda x: x **3), items))  #map(data's function,item) here datatype is int
print(a)
#Output: [1, 8, 27, 64, 125]

#Filter
a = [1,2,3,4,5,6]
b = [2,5,0,7,3]
c= list(filter(lambda x: x in a, b))
print(c) # prints out [2, 5, 3]

#Reducefrom functools import reduce
from functools import reduce

list1 = [1,2,3,4,2]
num = reduce(lambda x,y:x*y, list1)

print(num)

# output: 48
