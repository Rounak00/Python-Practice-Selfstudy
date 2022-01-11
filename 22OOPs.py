 #........................Classes & Objects....................
#instance variable
  class Student:
    pass

harry = Student()
larry = Student()

harry.name = "Harry"
harry.std = 12
harry.section = 1
larry.std = 9
larry.subjects = ["hindi", "physics"]
print(harry.section, larry.subjects)  
#   NB: if we make a empty class then we write there pass keyword

#clAss variable
class Employee:
    no_of_leaves = 8
    pass

harry = Employee()
rohan = Employee()

harry.name = "Harry"
harry.salary = 455
harry.role = "Instructor"

rohan.name = "Rohan"
rohan.salary = 4554
rohan.role = "Student"

print(Employee.no_of_leaves)
print(Employee.__dict__)
Employee.no_of_leaves = 9  #value of class variable's cant change by objects 
print(Employee.__dict__) #dict is a attribute that print  class or object's variables
print(Employee.no_of_leaves)


#..................Self & __init__() (Constructors)........................
class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age

p1 = Person("John", 36)
print(p1.name) 
#Output: John

#.................Class Methods In Python .................
# syntax:
#class myClass:
#     @classmethod
#     def myfunc (cls, arg1, arg2, ...):  #here cls is the class
                         

class Employee:

   no_of_ leaves = 8

  def init__ (self, aname, asalary, arole):
     self.name = aname
     self.salary = asalary
     self.role = arole

  def printdetails (self):

      return f"The Name is (self.name). Salary is (self.salary) and role is (self.role)"

  @classmethod

      def change_leaves (cls, newleaves): cls.no of leaves = newleaves



harry = Employee ("Harry", 255, "Instructor")

rohan Employee ("Rohan", 455, "Student")

rohan.change_leaves (34)

print (harry.no_of_leaves)

















