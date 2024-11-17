import tkinter as tk
from tkinter import messagebox
import json
import os

# File to store tasks
TASK_FILE = "tasks.json"


class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")
        self.root.geometry("500x400")
        self.tasks = []

        # Create UI
        self.create_widgets()

        # Load tasks from file
        self.load_tasks()

    def create_widgets(self):
        # Task List
        self.task_listbox = tk.Listbox(self.root, font=("Arial", 12), width=50, height=15)
        self.task_listbox.pack(pady=10)

        # Buttons
        self.add_button = tk.Button(self.root, text="Add Task", command=self.add_task)
        self.add_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.delete_button = tk.Button(self.root, text="Delete Task", command=self.delete_task)
        self.delete_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.save_button = tk.Button(self.root, text="Save Tasks", command=self.save_tasks)
        self.save_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.load_button = tk.Button(self.root, text="Load Tasks", command=self.load_tasks)
        self.load_button.pack(side=tk.LEFT, padx=10, pady=10)

    def add_task(self):
        # Create a new window for task input
        def save_new_task():
            title = title_entry.get().strip()
            desc = desc_entry.get("1.0", tk.END).strip()
            if title:
                self.tasks.append({"title": title, "description": desc})
                self.refresh_task_list()
                new_task_window.destroy()
            else:
                messagebox.showerror("Error", "Task title is required.")

        new_task_window = tk.Toplevel(self.root)
        new_task_window.title("Add Task")

        tk.Label(new_task_window, text="Task Title").pack(pady=5)
        title_entry = tk.Entry(new_task_window, width=40)
        title_entry.pack(pady=5)

        tk.Label(new_task_window, text="Task Description").pack(pady=5)
        desc_entry = tk.Text(new_task_window, width=40, height=5)
        desc_entry.pack(pady=5)

        save_button = tk.Button(new_task_window, text="Save Task", command=save_new_task)
        save_button.pack(pady=10)

    def delete_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            task_title = self.tasks[selected_index[0]]["title"]
            del self.tasks[selected_index[0]]
            self.refresh_task_list()
            messagebox.showinfo("Task Deleted", f"Task '{task_title}' has been deleted.")
        else:
            messagebox.showerror("Error", "No task selected.")

    def refresh_task_list(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            self.task_listbox.insert(tk.END, task["title"])

    def save_tasks(self):
        try:
            with open(TASK_FILE, "w") as file:
                json.dump(self.tasks, file, indent=4)
            messagebox.showinfo("Tasks Saved", "Tasks have been saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save tasks: {e}")

    def load_tasks(self):
        if os.path.exists(TASK_FILE):
            try:
                with open(TASK_FILE, "r") as file:
                    self.tasks = json.load(file)
                self.refresh_task_list()
                messagebox.showinfo("Tasks Loaded", "Tasks have been loaded successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load tasks: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()
