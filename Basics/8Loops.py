#Range
list(range(1,11)) -> [1...10]
list(range(15)) -> [0,1,2....14]
list(range(1,11,3)) -> [1,4,7,10]

*> In Python for loop run on range or  sequence like string list etc

li=[1,2,3,4,5]

"""For Loop"""
 for item in li :
    print(item)
    
 li2=[["odd",1],["even",2],["zero",0]]
for item, num in li2:
  print(item,num)
  
#if we want to print somthing 45 times we can write this also
for i in range(45) #range is not variable here
  
  
  
"""while loop"""
i=1
while(i<10):
 print(i)
 i++

 
 
 """Break and Continue"""
 
 i=1
 while(true):
  print(i)
  i++
  if i>10:
   break()#terminate the loop
   
   
   
 i=1
 while(true)
  i++
  if i%5==0:
    continue()#skip for those numbers that are divisable by 5
    
  print(i)  
