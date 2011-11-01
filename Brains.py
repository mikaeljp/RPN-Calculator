"""RPN Calculator
Main stack holds all values.
operators for now: plus, minus, multiplication, division, power, root, square root*, square*

*default values are inserted automatically

For GUI, pressing any operator has the effect of pressing enter, then the operator
operators evaluate the top two elements of the stack

Maybe in the future the stack can be reordered?
"""

import collections
import math

class Stack():
    def __init__(self):
        self.stack = collections.deque([])
        
    def __str__(self):
        """returns a string to render the stack contents to the form"""
        return '\n'.join(map(str, self.stack))
    
    def enter(self, value):
        #if no value is passed, duplicate the last argument on the stack
        #but if 0 is passed, add it to the stack!
        #if the stack is length 0, don't do anything
        if type(value) == str and len(value) == 0:
            try:
                value = self.stack[-1]
            except IndexError:
                return
        try:
            self.stack.append(float(value))
        except ValueError:
            #if invalid data, don't do anything
            pass
        
    def delete(self):
        self.stack.pop()
        
    def delete_all(self):
        self.stack = collections.deque([])
        
    def __get_values(self):
        """returns the last two values in the stack
        if there are less than two values this function returns '0' in place of missing values"""
        if len(self.stack) > 1:
            #there are at least 2 values, return them both
            #poping them in this way reverses the order, return the stack order with [::-1]
            return (self.stack.pop(), self.stack.pop())[::-1]
        elif len(self.stack) == 1:
            #there is only one value, return it with a zero
            #for consistency with above, return the 0 in the first position
            return (self.stack.pop(), 0)
        else:
            #the stack is empty
            #instead of raising an error, return (0,0) and let the function raise an error if needed
            return (0,0)
            
    def __get_single(self):
        """returns the last value in the stack, or 0"""
        if len(self.stack) == 0:
            return 0
        else:
            return self.stack.pop()
        
    def operate(self, operation, value=None):
        if value:
            self.enter(value)
        args = self.__get_values()
        try:
            self.enter(operation(*args))
        except ZeroDivisionError:
            #if there is a division by zero, return the args to the stack and then pass the error up
            self.enter(args[0])
            self.enter(args[1])
            raise ZeroDivisionError
        
    def operate_single(self, operation, value=None):
        """used for functions that only take one value like square root"""
        if value:
            self.enter(value)
        arg = self.__get_single()
        try:
            self.enter(operation(arg))
        except ZeroDivisionError:
            self.enter(arg)
            raise ZeroDivisionError


#individual operations are defined as functions, additional functions can be added in modules    
def add(a,b):
    return a + b

def sub(a,b):
    return a - b

def mult(a,b):
    return a * b

def div(a,b):
    return a / b

def power(a,b):
    return a ** b

def square(a):
    return a ** 2

def sqroot(a):
    return a ** .5

def root(a,b):
    return a ** (1/b)

def rev_sign(a):
    return -a

def fact(a):
    return math.gamma(a + 1)
