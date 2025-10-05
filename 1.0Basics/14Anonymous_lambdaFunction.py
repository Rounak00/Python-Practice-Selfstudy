#lambad or anonymous function

minus(a,b):
  return a-b

# now in lambda
minus=lambda a,b:a-b


#Higher order function
def return_sum(func, L):
    result = 0

    for i in L:
        if func(i):
            result = result + i

    return result


# List of numbers
L = [11, 14, 21, 23, 56, 78, 45, 29, 28]

# Lambda functions
x = lambda num: num % 2 == 0     # even numbers
y = lambda num: num % 2 != 0     # odd numbers
z = lambda num: num % 3 == 0     # divisible by 3

# Calling function with different lambdas
print(return_sum(x, L))  # sum of even numbers
print(return_sum(y, L))  # sum of odd numbers
print(return_sum(z, L))  # sum of numbers divisible by 3
