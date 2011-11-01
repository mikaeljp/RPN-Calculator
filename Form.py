import Tkinter
import tkMessageBox
import math
import functools

import Brains

class App():
    def __init__(self, master):
        
        self.calc = Brains.Stack()
        
        #the message field displays the stack in memory
        #after every operation that affects the stack the method __refresh() 
        #should be called to update the message text variable
        self.message_text = Tkinter.StringVar()
        self.message = Tkinter.Message(textvariable=self.message_text)
        self.message.grid(row=0, column=0, rowspan=4)
        
        #the active_value label displays the currently active number
        #if the enter command is sent, it will be null, which is fine
        #if an operator is called, the active_value should be added to the stack before
        #the operation is executed.
        self.active_value_text = Tkinter.StringVar()
        self.active_value = Tkinter.Label(textvariable=self.active_value_text)
        self.active_value.grid(row=5, column=0, columnspan=6)
        
        
        
        #-------------------------ButtonDex-----------------------------#        
        #buttons are defined in the buttonDex with a grid location and button command
        #The keys used in the dictionary are the bound keys for the button
        #After the buttons are created the button object is stored over the configuration dictionary
        #The listener looks up key bindings by Event.keysym, so leave off the '<' and '>' from special keys
        #When the keys are bound the brackets will be added if needed
        
        self.buttonDex = {
            '0':{'guide':{'row':3, 'column':1}, 'btn':'0'},
            'period':{'guide':{'row':3, 'column':2}, 'btn':'.'},
            'Return':{'guide':{'row':3, 'column':3}, 'btn':[u'\u21B5', self.enter]},
            '1':{'guide':{'row':2, 'column':1}, 'btn':'1'},
            '2':{'guide':{'row':2, 'column':2}, 'btn':'2'},
            '3':{'guide':{'row':2, 'column':3}, 'btn':'3'},
            '4':{'guide':{'row':1, 'column':1}, 'btn':'4'},
            '5':{'guide':{'row':1, 'column':2}, 'btn':'5'},
            '6':{'guide':{'row':1, 'column':3}, 'btn':'6'},
            '7':{'guide':{'row':0, 'column':1}, 'btn':'7'},
            '8':{'guide':{'row':0, 'column':2}, 'btn':'8'},
            '9':{'guide':{'row':0, 'column':3}, 'btn':'9'},
            'plus':{'guide':{'row':0, 'column':4}, 'btn':['+', self.operate, Brains.add]},
            'minus':{'guide':{'row':1, 'column':4}, 'btn':['-', self.operate, Brains.sub]},
            'asterisk':{'guide':{'row':2, 'column':4}, 'btn':['x', self.operate, Brains.mult]},
            'slash':{'guide':{'row':3, 'column':4}, 'btn':['/', self.operate, Brains.div]},
            'asciicircum':{'guide':{'row':0, 'column':5}, 'btn':['x^y', self.operate, Brains.power]},
            'm':{'guide':{'row':2, 'column':5}, 'btn':['(-x)', self.operate_single, Brains.rev_sign]},
            'c':{'guide':{'row':2, 'column':7}, 'btn':['c', self.delete]},
            'C':{'guide':{'row':3, 'column':7}, 'btn':['C', self.delete_all]},
            'E':{'guide':{'row':0, 'column':6}, 'btn':['Exp(x)', self.operate_single, math.exp]},
            'l':{'guide':{'row':1, 'column':6}, 'btn':['ln(x)', self.operate_single, math.log]},
            'p':{'guide':{'row':0, 'column':7}, 'btn':['pi', self.build_active, math.pi]},
            'e':{'guide':{'row':1, 'column':7}, 'btn':['e', self.build_active, math.e]},
            'exclam':{'guide':{'row':3, 'column':5}, 'btn':['x!', self.operate_single, Brains.fact]},
            }
        
        #since I want all the buttons to be sticky NSEW here's a grid function that does that
        sticky_grid = functools.partial(Tkinter.Widget.grid, sticky=Tkinter.NSEW)
        
        #Pass over the buttonDex and create all the buttons, then store them in the same dictionary
        for btn in self.buttonDex.keys():
            btn_obj = self.make_btn(*self.buttonDex[btn]['btn'])
            sticky_grid(btn_obj, **self.buttonDex[btn]['guide'])
            self.buttonDex[btn] = btn_obj
        
       
        
        #-------------------------Operation Buttons---------------------------#
        
        self.btn_square = Tkinter.Button(text='x^2', command=lambda func=Brains.square: self.operate_single(func))
        sticky_grid(self.btn_square, row=1, column=5)
        
        self.btn_sqrt = Tkinter.Button(text='sqrt(x)', command=lambda func=math.sqrt: self.operate_single(func))
        sticky_grid(self.btn_sqrt, row=2, column=6)
        
        self.btn_yroot = Tkinter.Button(text='y root(x)', command=lambda func=Brains.root: self.operate(func))
        sticky_grid(self.btn_yroot, row=3, column=6)
        
        
    def make_btn(self, btn_text, cmd=None, param=None):
        if not cmd:
            cmd=functools.partial(self.build_active, btn_text)
        if not param:
            cmd=functools.partial(cmd)
        else:
            cmd=functools.partial(cmd, param)
        return Tkinter.Button(text=btn_text, command=cmd)
        
        
    def __refresh(self):
        self.message_text.set(str(self.calc))
        
    def build_active(self, value):
        """this method adds to the active_value_text variable"""
        self.active_value_text.set(self.active_value_text.get() + str(value))
        
    def enter(self):
        #send the active value to the stack.
        #if the active_value is empty, the calculator will duplicate the last value on the stack
        self.calc.enter(self.active_value_text.get())
        self.active_value_text.set('')
        self.__refresh()
        
    def operate(self, operation):
        #if there is an active value, enter it before operating
        if self.active_value_text.get():
            self.enter()
        try:
            self.calc.operate(operation)
        except ZeroDivisionError:
            tkMessageBox.showerror('Error', 'Division by zero')
        self.__refresh()
        
    def operate_single(self, operation):
        if self.active_value_text.get():
            self.enter()
        try:
            self.calc.operate_single(operation)
        except ZeroDivisionError:
            tkMessageBox.showerror('Error', 'Division by zero')
        self.__refresh()
        
    def delete(self):
        #first, if there is an active value, then clear that
        if self.active_value_text.get():
            self.active_value_text.set('')
            return
        #otherwise, delete the topmost item on the stack
        try:
            self.calc.delete()
        except IndexError:
            pass
        self.__refresh()
        
    def delete_all(self):
        self.active_value_text.set('')
        self.calc.delete_all()
        self.__refresh()
    
    def listener(self, event):
        self.buttonDex[event.keysym].invoke()
        
root = Tkinter.Tk()
root.title('RPN Calculator')

app = App(root)

for key in app.buttonDex.keys():
    if len(key) > 1:
        key = '<' + key + '>'
    root.bind(key, app.listener)
    
    



root.mainloop()

