"""
Modes of opening file in Python:
There are many modes of opening a file in Python, unlike other languages Python has provided its users a variety of options. We will discuss seven of them in this tutorial.

r : r mode opens a file for read-only. We do not have permission to update or change any data in this mode.
w : w mode does not concern itself with what is present in the file. It just opens a file for writing and if there is already some data present in the file, it overwrites it.
x : x is used to create a new file. It does not work for an already existing file, as in such cases the operation fails.
a : a stands for append, which means to add something to the end of the file. It does exactly the same. It just adds the data we like in write(w) mode but instead of overwriting it just adds it to the end of the file. It also does not have the permission of reading the file.
t : t mode is used to open our file in text mode and only proper text files can be opened by it. It deals with the file data as a string.
b : b stands for binary and this mode can only open the binary files, that are read in bytes. The binary files include images, documents, or all other files that require specific software to be read.
+ : In plus mode, we can read and write a file simultaneously. The mode is mostly used in cases where we want to update our file.
 r and t is default mode
"""

f= open(file name and extention in double column, mode in double column)#return a file pointer

content=f.read()#if we give a number in read function then it read that many letters and if we do it again then next letters 
print(content)
f.close()#whenever open please close this it's a great practice

f.readline()#use for readline one by one bby calls mean first time only print 1 then print 2 and then print 3lines

f.readline()#print all line in a list at once


"""Write"""
f=open("filename with extention","w")
f.write("Hello sir") #for every run writing is change and cant store previous writing so for that we should use 'a' instead of 'w' bcz a is append mode
f.close()

a=f.write("Hello sir")#it returns how many characters we write in  this line

"""Read+Write"""
f=open("filename with extention","r+") #for read and write mode both



"""tell()"""
print(f.tell())#shows us where is the file pointer return index number

"""seek()"""
f.seek(10)#replace file pointer in that particular index


"""Using block"""
with open("filename with extention") as f: #dont need to close the file now
     a=f.read(4)
     print(a)#first 4 elements







