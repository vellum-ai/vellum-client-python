class A:
    foo: str


class B(A):
    pass


class C(A):
    pass


print(B.__annotations__)
print(C.__annotations__)
# On python 3.9 this is True, but on 3.11 it's False!
print(id(C.__annotations__) == id(B.__annotations__))


B.__annotations__["bar"] = int
print(B.__annotations__)
print(C.__annotations__)  # on 3.9, this is updated with `bar`, but on 3.11 it's not!
