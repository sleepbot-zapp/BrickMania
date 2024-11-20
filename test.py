class Foo:
    def __new__(cls):
        return 1
    
a = Foo()

print(a)