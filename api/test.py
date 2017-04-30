#!/usr/bin/env python
default_data = {}
class MyClass:
    """A simple example class"""
    i = 12345
    name = "test"
    def f(self):
        print 'hello world'

for i in range(10):
    #print i
    default_data[i] = MyClass()

print default_data[2].name
default_data[2].name = "neuer name"
print default_data[2].name
default_data[2].f()

