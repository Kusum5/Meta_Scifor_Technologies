#Jhony, a 10th grade kid has recently started to learn python tkinter and is so much keen
# to understand how an MS Paint works and wants to create a very small replica of it in
# his own system using python with the following buttons pen brush color eraser brush/pen size changer
from tkinter import *
root = Tk()
root.title("Paint")
root.configure(bg = "light grey")
root.geometry("500x280")
#def usepen():

paintarea = Canvas(root,width=500)
paintarea.grid(row=0,column=2,rowspan=6)
pen = Label(root,text="pen",bg = "light grey")
pen.grid(row=0,column=0,padx=10)
penbutton = Button(root,text="p",bg = "light grey")
penbutton.grid(row=0,column=1)
brush = Label(root,text="brush",bg = "light grey")
brush.grid(row=1,column=0)
brushbutton = Button(root,text="b",bg = "light grey")
brushbutton.grid(row=1,column=1)
color = Label(root,text="color",bg = "light grey")
color.grid(row=2,column=0)
colorbutton = Button(root,text="c",bg = "light grey")
colorbutton.grid(row=2,column=1)
eraser = Label(root,text="eraser",bg = "light grey")
eraser.grid(row=3,column=0)
eraserbutton= Button(root,text="e",bg = "light grey",)
eraserbutton.grid(row=3,column=1)
penscale = Scale(root,bg = "light grey")
penscale.grid(row=4,column=0)
size = Label(root,text="Pen Size",bg = "light grey")
size.grid(row=5,column=0,columnspan=2)
mainloop()