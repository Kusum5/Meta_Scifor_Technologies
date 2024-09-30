from tkinter import *
from PIL import ImageTk,Image

root = Tk()
root.title("Image Slider")
img1 = ImageTk.PhotoImage(Image.open('img2.jpg'))
img2 = ImageTk.PhotoImage(Image.open('img1.jpg'))
img3 = ImageTk.PhotoImage(Image.open("img3.jpg"))
img4 = ImageTk.PhotoImage(Image.open("img4.jpg"))
imagelist=[img1,img2,img3,img4]

label = Label(image=img4,width=1000,height=500,border=20,bg="black")
label.grid(row=0,column=0,columnspan=3)

def forward(imagenumber):
    global label
    global backbutton
    global forwardbutton

    label.grid_forget()
    label = Label(image=imagelist[imagenumber-1])
    forwardbutton = Button(root, text=">>", command=lambda: forward(imagenumber + 1))
    backbutton = Button(root, text="<<", command=lambda: back(imagenumber - 1))
    if imagenumber == 4:
       forwardbutton = Button(root,text=">>",state=DISABLED)
    label.grid(row=0,column=0,columnspan =3)
    forwardbutton.grid(row=1,column=2)
    backbutton.grid(row=1,column=0)
    status = Label(root, text="Image " + str(imagenumber) + "of" + str(len(imagelist)), bd=1, relief=SUNKEN, anchor=E)
    status.grid(row=2, column=0, columnspan=3, sticky=W + E)
def back(imagenumber):
    global label
    global backbutton
    global forwardbutton
    label.grid_forget()
    forwardbutton = Button(root, text=">>", command=lambda: forward(imagenumber + 1))
    backbutton = Button(root, text="<<", command=lambda: back(imagenumber - 1))
    label.grid(row=0, column=0, columnspan=3)
    forwardbutton.grid(row=1, column=2)
    backbutton.grid(row=1, column=0)
    if imagenumber== 1:
        backbutton = Button(root,text="<<",state=DISABLED)

backbutton = Button(root,text="<<",command=back, state=DISABLED)
button2 = Button(root,text="Exit",command=root.quit)
forwardbutton = Button(root,text=">>",command=lambda: forward(2))
backbutton.grid(row=1,column=0)
button2.grid(row=1,column=1)
forwardbutton.grid(row=1,column=2,pady=10)
mainloop()