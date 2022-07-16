# What should a docstring look like?

# The doc string line should begin with a capital letter and end with a period.
# The first line should be a short description.
# If there are more lines in the documentation string, the second line should be blank, visually separating the summary
# from the rest of the description.
# The following lines should be one or more paragraphs describing the object’s calling conventions,
# its side effects, etc.

#  nested functions

#  main function

def square(n):
    '''Takes in a number n, returns the square of n'''
    return n ** 2


print(square.__doc__)
help(square)  # We can also use the help() function to read the docstrings associated with various objects
# docstring for modules

#  import pickle

#  print(pickle.__doc__)
