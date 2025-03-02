import json
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkFont

class TodoList:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        try:
            with open('tasks.json', 'r') as file:
                self.tasks = json.load(file)
        except FileNotFoundError:
            self.tasks = []

    def save_tasks(self):
        with open('tasks.json', 'w') as file:
            json.dump(self.tasks, file, indent=2)

    def add_task(self, description):
        task = {
            'id': len(self.tasks) + 1,
            'description': description,
            'completed': False,
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.tasks.append(task)
        self.save_tasks()
        return task

    def complete_task(self, task_id):
        for task in self.tasks:
            if task['id'] == task_id:
                task['completed'] = True
                self.save_tasks()
                return True
        return False

    def delete_task(self, task_id):
        for task in self.tasks:
            if task['id'] == task_id:
                self.tasks.remove(task)
                self.save_tasks()
                return True
        return False

class TodoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.todo = TodoList()
        self.setup_window()
        self.create_widgets()
        self.load_tasks()
        
    def setup_window(self):
        self.title("Modern Todo App")
        self.geometry("600x500")
        self.configure(bg="#f0f0f0")
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", background="#ffffff", fieldbackground="#ffffff", foreground="#333333")
        style.configure("TButton", padding=6, relief="flat", background="#007bff")
        
    def create_widgets(self):
        # Top frame for input
        input_frame = tk.Frame(self, bg="#f0f0f0")
        input_frame.pack(padx=20, pady=20, fill="x")
        
        # Task entry
        self.task_entry = ttk.Entry(input_frame, font=("Helvetica", 12))
        self.task_entry.pack(side="left", expand=True, fill="x", padx=(0, 10))
        
        # Add button
        add_btn = ttk.Button(input_frame, text="Add Task", command=self.add_task)
        add_btn.pack(side="right")
        
        # Task list
        self.tree = ttk.Treeview(self, columns=("ID", "Task", "Status", "Date"), show="headings", height=15)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Task", text="Task")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Date", text="Created")
        
        # Column widths
        self.tree.column("ID", width=50)
        self.tree.column("Task", width=300)
        self.tree.column("Status", width=100)
        self.tree.column("Date", width=150)
        
        self.tree.pack(padx=20, pady=(0, 20), fill="both", expand=True)
        
        # Buttons frame
        btn_frame = tk.Frame(self, bg="#f0f0f0")
        btn_frame.pack(padx=20, pady=(0, 20), fill="x")
        
        # Action buttons
        complete_btn = ttk.Button(btn_frame, text="Mark Complete", command=self.complete_task)
        complete_btn.pack(side="left", padx=5)
        
        delete_btn = ttk.Button(btn_frame, text="Delete Task", command=self.delete_task)
        delete_btn.pack(side="left", padx=5)
        
        # Bind enter key to add task
        self.task_entry.bind("<Return>", lambda e: self.add_task())
        
    def load_tasks(self):
        self.tree.delete(*self.tree.get_children())
        for task in self.todo.tasks:
            status = "✓ Complete" if task['completed'] else "Pending"
            self.tree.insert("", "end", values=(
                task['id'],
                task['description'],
                status,
                task['created_at']
            ))
            
    def add_task(self):
        description = self.task_entry.get().strip()
        if description:
            self.todo.add_task(description)
            self.task_entry.delete(0, tk.END)
            self.load_tasks()
        else:
            messagebox.showwarning("Warning", "Please enter a task description")
            
    def complete_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a task to complete")
            return
            
        task_id = int(self.tree.item(selected[0])['values'][0])
        self.todo.complete_task(task_id)
        self.load_tasks()
        
    def delete_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a task to delete")
            return
            
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this task?"):
            task_id = int(self.tree.item(selected[0])['values'][0])
            self.todo.delete_task(task_id)
            self.load_tasks()

def main():
    app = TodoApp()
    app.mainloop()

if __name__ == "__main__":
    main()