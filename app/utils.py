# unused variable + duplicate string + magic number
MY_CONST = 42

def bad_smell(x):
    tmp = 123   # unused
    if x == 1:
        print("hello")
    elif x == 1:  # duplicated condition
        print("hello")
    return x + 3.14  # magic number (float literal)
