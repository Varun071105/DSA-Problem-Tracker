
import json
import datetime
import tkinter as tk
from tkinter import messagebox, ttk
import os

DATA_FILE = "dsa_problems.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

class DSATrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DSA Problem Tracker")
        self.root.geometry("700x400")
        self.data = load_data()

        # Input fields
        self.title_var = tk.StringVar()
        self.topic_var = tk.StringVar()
        self.difficulty_var = tk.StringVar()
        self.platform_var = tk.StringVar()
        self.status_var = tk.StringVar()
        self.date_var = tk.StringVar(value=str(datetime.date.today()))

        # UI layout
        self.create_form()
        self.create_table()
        self.refresh_table()

    def create_form(self):
        tk.Label(self.root, text="Problem Title").grid(row=0, column=0)
        tk.Entry(self.root, textvariable=self.title_var).grid(row=0, column=1)

        tk.Label(self.root, text="Topic").grid(row=1, column=0)
        tk.Entry(self.root, textvariable=self.topic_var).grid(row=1, column=1)

        tk.Label(self.root, text="Difficulty").grid(row=0, column=2)
        ttk.Combobox(self.root, textvariable=self.difficulty_var, values=["Easy", "Medium", "Hard"]).grid(row=0, column=3)

        tk.Label(self.root, text="Platform").grid(row=1, column=2)
        tk.Entry(self.root, textvariable=self.platform_var).grid(row=1, column=3)

        tk.Label(self.root, text="Status").grid(row=2, column=0)
        ttk.Combobox(self.root, textvariable=self.status_var, values=["Solved", "Unsolved"]).grid(row=2, column=1)

        tk.Label(self.root, text="Date").grid(row=2, column=2)
        tk.Entry(self.root, textvariable=self.date_var).grid(row=2, column=3)

        tk.Button(self.root, text="Add Problem", command=self.add_problem).grid(row=3, column=1, pady=10)

    def create_table(self):
        columns = ("title", "topic", "difficulty", "platform", "status", "date")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=100)
        self.tree.grid(row=4, column=0, columnspan=4, padx=10, pady=10)

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for item in self.data:
            self.tree.insert("", "end", values=(item["title"], item["topic"], item["difficulty"],
                                                item["platform"], item["status"], item["date_solved"]))

    def add_problem(self):
        problem = {
            "title": self.title_var.get(),
            "topic": self.topic_var.get(),
            "difficulty": self.difficulty_var.get(),
            "platform": self.platform_var.get(),
            "status": self.status_var.get(),
            "date_solved": self.date_var.get()
        }

        if not all(problem.values()):
            messagebox.showwarning("Input Error", "Please fill all fields.")
            return

        self.data.append(problem)
        save_data(self.data)
        self.refresh_table()
        messagebox.showinfo("Success", "Problem added successfully!")
        for var in [self.title_var, self.topic_var, self.difficulty_var, self.platform_var, self.status_var]:
            var.set("")
        self.date_var.set(str(datetime.date.today()))

if __name__ == "__main__":
    root = tk.Tk()
    app = DSATrackerApp(root)
    root.mainloop()
