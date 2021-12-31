def fun1(*args): #in args takes as a tuple
  for item in args:
    print
  
  
har=[1,2,3,4,5]
fun1(*har)
"""
**kwargs:
The full form of **kwargs is keyword arguments. It passes the data to the argument in the form of a dictionary. Let's take the same example we used in the case of *args. The only difference now is that the student's registration, along with the student's name, has to be entered. So what **kwargs does is, it sends argument in the form of key and value pair. So the student's name and their registration both can be sent as a parameter using a single ** kwargs statement.

Same as we discussed for args*, the name kwargs does not matter. We can write any other name in its place, such as **attendance. The only mandatory thing is the double asterisks we placed before the name.   
"""

def funargs(normal, *argsrohan, **kwargsbala):
    print(normal)
    for item in argsrohan:
        print(item)
    print("\nNow I would Like to introduce some of our heroes")
    for key, value in kwargsbala.items():
        print(f"{key} is a {value}")


# function_name_print("Harry", "Rohan", "Skillf", "Hammad", "Shivam")

har = ["Harry", "Rohan", "Skillf", "Hammad",
       "Shivam", "The programmer"]
normal = "I am a normal Argument and the students are:"
kw = {"Rohan":"Monitor", "Harry":"Fitness Instructor",
      "The Programmer": "Coordinator", "Shivam":"Cook"}
funargs(normal, *har, **kw)
  
