class A:
    code  = 1

class B(A):
    msg = 2

b = B()
print(isinstance(b, A))