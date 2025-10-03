#Enamurate
list_2 = ["Python", "Programming", "Is", "Fun"]
#Counter value starts from 5
result = enumerate(list_2, 5)
print(list(result))

#We will get the following output:

[(5, 'Python'), (6, 'Programming'), (7, 'Is'), (8, 'Fun')]




#join
#join() with lists
numList = ['1', '2', '3', '4']
separator = ', '
print(separator.join(numList))
Output:
1, 2, 3, 4
