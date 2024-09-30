import math
from tkinter import *
root = Tk()
root.title("Scientific Calculator")
root.configure(bg="dark grey")
root.iconbitmap('calc.ico')

e = Entry(root,borderwidth=5,width=55)
e.grid(row=0,column=0,padx=20,pady=15,columnspan = 4)
def clicked(number):
    current = e.get()
    e.delete(0,END)
    e.insert(0,str(current) + str(number))
def clear():
   e.delete(0,END)
def decimal():
    current = e.get()
    e.delete(0,END)
    e.insert(0,str(current) + str("."))
def add():
    global first_num
    global operation
    operation = "sum"
    first_num = float(e.get())
    e.delete(0,END)
def minus():
    global first_num
    global operation
    operation = "difference"
    first_num = float(e.get())
    e.delete(0, END)
def multiply():
    global first_num
    global operation
    operation = "product"
    first_num = float(e.get())
    e.delete(0, END)
def divide():
    global first_num
    global operation
    operation = "division"
    first_num = float(e.get())
    e.delete(0, END)
def modulus():
    global first_num
    global operation
    operation = "modulus"
    first_num = float(e.get())
    e.delete(0, END)
def square():
    global first_num
    global operation
    operation = "square"
    first_num = float(e.get())
    e.delete(0, END)
def power3():
    global first_num
    global operation
    operation = "power3"
    first_num = float(e.get())
    e.delete(0, END)
def findlog():
    global first_num
    global operation
    operation = "log"
    first_num = float(e.get())
    e.delete(0, END)
def cos():
    global first_num
    global operation
    operation = "cosine"
    first_num = float(e.get())
    e.delete(0, END)
def sin():
    global first_num
    global operation
    operation = "sine"
    first_num = float(e.get())
    e.delete(0, END)
def tan():
    global first_num
    global operation
    operation = "tangent"
    first_num = float(e.get())
    e.delete(0, END)
def output():
    second_num = e.get()
    e.delete(0,END)
    if operation == "sum":
        e.insert(0,first_num + float(second_num))
    elif operation == "difference":
        e.insert(0,first_num - float(second_num))
    elif operation == "product":
        e.insert(0,first_num * float(second_num))
    elif operation == "division":
        e.insert(0,first_num/ float(second_num))
    elif operation == "modulus":
        e.insert(0,first_num % float(second_num))
    elif operation == "square":
        e.insert(0,first_num * float(first_num))
    elif operation == "power3":
        e.insert(0,pow((first_num),3))
    elif operation == "log":
        e.insert(0,math.log2(first_num))
    elif operation == "sine":
        e.insert(0,math.sin(first_num))
    elif operation == "cosine":
        e.insert(0,math.cos(first_num))
    elif operation == "tangent":
        e.insert(0,math.tan(first_num))

op1 = Button(root,text="AC",width=10,padx=10,pady=5,command=clear,activebackground="dark red",bg="red")
op2 = Button(root,text="+",width=10,padx=10,pady=5,command=add,activebackground="dark grey",bg="light grey")
op3 = Button(root,text="-",width=10,padx=10,pady=5,command=minus,activebackground="dark grey",bg="light grey")
op4 = Button(root,text="*",width=10,padx=10,pady=5,command=multiply,activebackground="dark grey",bg="light grey")
op5 = Button(root,text="cos",width=10,padx=10,pady=5,command=cos,activebackground="dark grey",bg="light grey")
op6 = Button(root,text="sin",width=10,padx=10,pady=5,command=sin,activebackground="dark grey",bg="light grey")
op7 = Button(root,text="tan",width=10,padx=10,pady=5,command=tan,activebackground="dark grey",bg="light grey")
op8 = Button(root,text="log",width=10,padx=10,pady=5,command=findlog,activebackground="dark grey",bg="light grey")
op9 = Button(root,text="/",width=10,padx=10,pady=5,command=divide,activebackground="dark grey",bg="light grey")
op10 = Button(root,text="x2",width=10,padx=10,pady=5,command=square,activebackground="dark grey",bg="light grey")
op11 = Button(root,text="x3",width=10,padx=10,pady=5,command=power3,activebackground="dark grey",bg="light grey")
op12 = Button(root,text="%",width=10,padx=10,pady=5,command=modulus,activebackground="dark grey",bg="light grey")
op13 = Button(root,text=".",width=10,padx=10,pady=5,command=decimal,activebackground="dark grey",bg="light grey")
eq= Button(root,text="=",width=10,padx=10,pady=5,command=output,activebackground="green",bg="dark green")
b1 = Button(root,text="1",width=10,padx=10,pady=5,command=lambda:clicked(1),activebackground="light grey")
b2 = Button(root,text="2",width=10,padx=10,pady=5,command=lambda:clicked(2),activebackground="light grey")
b3 = Button(root,text="3",width=10,padx=10,pady=5,command=lambda:clicked(3),activebackground="light grey")
b4 = Button(root,text="4",width=10,padx=10,pady=5,command=lambda:clicked(4),activebackground="light grey")
b5 = Button(root,text="5",width=10,padx=10,pady=5,command=lambda:clicked(5),activebackground="light grey")
b6 = Button(root,text="6",width=10,padx=10,pady=5,command=lambda:clicked(6),activebackground="light grey")
b7 = Button(root,text="7",width=10,padx=10,pady=5,command=lambda:clicked(7),activebackground="light grey")
b8 = Button(root,text="8",width=10,padx=10,pady=5,command=lambda:clicked(8),activebackground="light grey")
b9 = Button(root,text="9",width=10,padx=10,pady=5,command=lambda:clicked(9),activebackground="light grey")
b0 = Button(root,text="0",width=10,padx=10,pady=5,command=lambda:clicked(0),activebackground="light grey")
op1.grid(row=1,column=0)
op2.grid(row=1,column=1)
op3.grid(row=1,column=2)
op4.grid(row=1,column=3)
op5.grid(row=2,column=0)
op6.grid(row=2,column=1)
op7.grid(row=2,column=2)
op8.grid(row=2,column=3)
b1.grid(row=6,column=0)
b2.grid(row=6,column=1)
b3.grid(row=6,column=2)
op11.grid(row=6,column=3)
b4.grid(row=5,column=0)
b5.grid(row=5,column=1)
b6.grid(row=5,column=2)
op10.grid(row=5,column=3)
b7.grid(row=4,column=0)
b8.grid(row=4,column=1)
b9.grid(row=4,column=2)
op9.grid(row=4,column=3)
op12.grid(row=7,column=0)
b0.grid(row=7,column=1)
op13.grid(row=7,column=2)
eq.grid(row=7,column=3)

mainloop()
