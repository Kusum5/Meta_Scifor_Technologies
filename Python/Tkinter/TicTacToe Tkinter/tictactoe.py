import tkinter as tk
from tkinter import messagebox
class tictactoe:
    def __init__(self,root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.geometry("400x400")
        self.root.configure(bg = "light grey")
        self.currentplayer = "X"
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.createwidgets()

    def createwidgets(self):
        for row in range(3):
           for col in range(3):
               button = tk.Button(self.root,text="",font=('normal',32),width=5,height=2,command= lambda r=row,c=col: self.button_click(r,c))
               button.grid(row=row,column=col)
               self.buttons[row][col] = button

    def button_click(self,row,col):
        if self.buttons[row][col]['text'] == "" and not self.checkWinner():
            self.buttons[row][col]['text'] = self.currentplayer
            if self.checkWinner():
                messagebox.showinfo(f"Player {self.currentplayer} wins")
            elif self.checkdraw():
                messagebox.showinfo(("Draw"))
            else:
                self.currentplayer = "O" if self.currentplayer == "X" else "X"

    def checkWinner(self):
        for row in range(3):
            if self.buttons[row][0]['text'] == self.buttons[row][1]['text'] == self.buttons[row][2]['text'] != "":
                return True

        for col in range(3):
            if self.buttons[0][col]['text'] == self.buttons[1][col]['text'] == self.buttons[2][col]['text']!="":
                return True
        if self.buttons[0][0]['text']== self.buttons[1][1]['text'] == self.buttons[2][2]['text'] !="":
            return True
        if self.buttons[0][2]['text']== self.buttons[1][1]['text'] == self.buttons[2][0]['text'] !="":
            return True
        return False

    def checkdraw(self):
        for row in range(3):
            for col in range(3):
                if self.buttons[row][col]['text'] == "":
                    return False
        return True

if __name__ =="__main__":
    root= tk.Tk()
    app = tictactoe(root)
    root.mainloop()