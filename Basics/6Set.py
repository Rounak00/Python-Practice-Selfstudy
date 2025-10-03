""" Set is mutable but store only unique elements non indexing and cant store motable elements so 2d set not possible"""

"""intialize-> st=set([]) or l=[], st=set(l);""" 
st=set([1,2,3,4]);

st.add(7)
st.add(7)
st.add(7)
#but only take one 7

"""we can perform union and intersection and disjoint by union() and intersextion() and isdisjoint() functions"""

"""Set Related Funcion""" -> union, difference, intersection

del st # delete set
st.remove(val)#Remove a val
st.pop()#Remove end val that is first element here

