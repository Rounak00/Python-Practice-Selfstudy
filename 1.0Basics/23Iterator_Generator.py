#Iterators
🔄 Iterable vs Iterator
1. Iterable

An iterable is any Python object capable of returning an iterator.

Examples: list, tuple, str, dict, set, etc.

It has the method __iter__() which returns an iterator.

👉 Think of it as a collection of items you can loop over.

Example:

numbers = [1, 2, 3]
print(dir(numbers))   # contains __iter__

2. Iterator

An iterator is an object that produces the items of an iterable one at a time.

It has two important methods:

__iter__() (returns itself)

__next__() (returns the next item, raises StopIteration when no items left).

👉 Think of it as a cursor that moves through an iterable.

Example:

numbers = [1, 2, 3]
iterator = iter(numbers)   # get iterator from iterable

print(next(iterator))  # 1
print(next(iterator))  # 2
print(next(iterator))  # 3
# print(next(iterator))  # raises StopIteration

3. How for loop works internally

When you write:

for num in [1, 2, 3]:
    print(num)


Python does:

Calls iter([1, 2, 3]) → gets an iterator.

Calls next() repeatedly until StopIteration is raised.

4. Custom Iterator Example

You can create your own iterator class:

class Counter:
    def __init__(self, low, high):
        self.current = low
        self.high = high

    def __iter__(self):   # returns the iterator object itself
        return self

    def __next__(self):   # defines how to get the next value
        if self.current > self.high:
            raise StopIteration
        else:
            self.current += 1
            return self.current - 1

for num in Counter(1, 5):
    print(num)


✅ Output:

1
2
3
4
5

5. Quick Difference
Feature	Iterable	Iterator
Definition	Can return an iterator (__iter__)	Produces next item (__next__)
Examples	list, tuple, set, str, dict	object from iter(list)
Usage	Can be looped over multiple times	Gets consumed once
















#Generator
⚡ Generators in Python
1. What is a Generator?

A generator is a special kind of iterator.

You create it using either:

A function with the yield keyword

A generator expression (like list comprehension but with ())

Generators don’t store all values in memory. Instead, they generate items one by one (lazy evaluation).
👉 This makes them very memory-efficient.

2. Example: Generator Function
def my_generator():
    yield 1
    yield 2
    yield 3

gen = my_generator()
print(next(gen))  # 1
print(next(gen))  # 2
print(next(gen))  # 3
# print(next(gen))  # StopIteration


Here:

yield works like return, but pauses the function and resumes from the same point when called again.

Every call to next() continues from where it left off.

3. Example: Fibonacci with Generator
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

for num in fibonacci(6):
    print(num)


✅ Output:

0
1
1
2
3
5