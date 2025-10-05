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

   no_of_ leaves = 8 #static variable this is

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





# Encapsulation

def __someFunc(self):
  self.__A=10

# here both variable and funtions are private that is object can access directly


#Pass by refernece
class Student:
    def __init__(self, name):
        self.name = name

    def change_name(self, new_name):
        self.name = new_name  # modifies the same object

s = Student("Rounak")
s.change_name("Sunanda")

print(s.name)  # ✅ Sunanda

# Python passes references to objects, not the objects themselves — and whether changes reflect outside depends on whether the object is mutable or immutable.

# Pass by reference is Functions can accept objects and return objects as well


# static function same as function only dont have self can use this annotaion @staticethod



#Class Relation
# Aggreagtion relation or has a 
# Inheritance or is a 


#Aggregation 
class Engine:
    def __init__(self, horsepower):
        self.horsepower = horsepower

    def start(self):
        print("Engine started with", self.horsepower, "HP")

class Car:
    def __init__(self, model, horsepower):
        self.model = model
        # Car HAS-A Engine
        self.engine = Engine(horsepower)

    def start(self):
        print(f"{self.model} car starting...")
        self.engine.start()


# Using the classes
my_car = Car("Tesla Model 3", 400)
my_car.start()


# Inheritance
# MRO =>  (all 5 type inheritance possible here. in multilevel if parent A B have same function then which one inherit firast in child its funcation got call)
# Parent class
class Animal:
    def speak(self):
        print("Animal makes a sound")

# Child class (inherits from Animal)
class Dog(Animal):
    def speak(self):
        print("Dog barks")

# Create objects
a = Animal()
d = Dog()

a.speak()   # Output: Animal makes a sound
d.speak()   # Output: Dog barks
# own function call first it is come under pollymorphism (Methos override)


# Super keyword call parent functions and constructor
class Animal:
    def sound(self):
        print("Animal makes sound")

class Dog(Animal):
    def sound(self):
        super().sound()  # call parent method
        print("Dog barks")

dog = Dog()
dog.sound()

class Parent:
    def __init__(self):
        print("Parent constructor called")

    def show(self):
        print("This is Parent class")

class Child(Parent):
    def __init__(self):
        # Call Parent's constructor
        super().__init__()
        print("Child constructor called")

    def show(self):
        # Call Parent's show() method
        super().show()
        print("This is Child class")

# Create object
c = Child()
c.show()


# Mthos overload and operator overload is ther but operator overload not need in develpment
# Method overload

"""Python does not support traditional method overloading like Java or C++.

If you define a method multiple times with the same name, the last definition overrides the previous ones.

But you can achieve similar behavior using default arguments or *args/**kwargs.

Example using default arguments:"""

class Calculator:
    def add(self, a, b=0, c=0):  # default values for overloading
        return a + b + c

calc = Calculator()
print(calc.add(5))        # 5 (only 'a')
print(calc.add(5, 10))    # 15 (a + b)
print(calc.add(5, 10, 15))# 30 (a + b + c)