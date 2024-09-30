import tkinter as tk
from random import choice

class RandomNamePicker:
    def __init__(self, root, student_list):
        self.root = root
        self.student_list = student_list
        self.completed_list = []

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack()
        self.random_name_frame = tk.Frame(self.main_frame)
        self.random_name_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.completed_frame = tk.Frame(self.main_frame)
        self.completed_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        self.random_name_label = tk.Label(self.random_name_frame, text="Random Name:")
        self.random_name_label.pack()

        self.random_name_button = tk.Button(self.random_name_frame, text="Pick Random Name", command=self.pick_random_name)
        self.random_name_button.pack(pady=10)

        self.random_name_text = tk.Label(self.random_name_frame, text="")
        self.random_name_text.pack()
        self.completed_label = tk.Label(self.completed_frame, text="Completed:")
        self.completed_label.pack()

        self.completed_text = tk.Text(self.completed_frame, height=10, width=20,bg="light green")
        self.completed_text.pack()

    def pick_random_name(self):
        if self.student_list:
            random_name = choice(self.student_list)
            self.student_list.remove(random_name)
            self.completed_list.append(random_name)

            self.random_name_text['text'] = random_name
            self.completed_text.delete(1.0, tk.END)
            self.completed_text.insert(tk.END, "\n".join(self.completed_list))
        else:
            self.random_name_text['text'] = "No more students left!"

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Random UserName Picker")

    student_list = ["Kusum", "Komal", "Aisha", "Sonal", "Dev", "Ridhum"]
    app = RandomNamePicker(root, student_list)

    root.mainloop()