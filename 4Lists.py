#list is kinda arrays in python and index start from 0

fruit=["orange","apple","banana",56,78,0.25]

print(fruit)#print in from of array

print(fruit[0])#print orange

fruit.sort() #for sort
fruit.reverse()#fro reverse

print(fruit[0:6:2])#just like string slicing there is same list slicing

print(len(fruit))#return length

print(max(fruit))#return max element

print (min(fruit))#return min element

fruit.append("alovera")#add alovera in last index

fruit.insert(position, item)# here is position not index so for first place it is 1 not 0

fruit.remove(item)#item remove

fruit.pop()#remove last element

