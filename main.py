import os
import tkinter as tk
from tkinter import filedialog

def get_directory_tree(starting_directory, prefix=""):
    # List to hold each line of the directory tree
    tree_lines = []
    
    # List the contents of the current directory
    items = os.listdir(starting_directory)
    items = sorted(items, key=lambda x: (not os.path.isdir(os.path.join(starting_directory, x)), x))
    total_items = len(items)
    
    for index, item in enumerate(items):
        current_path = os.path.join(starting_directory, item)
        
        if index == total_items - 1:
            connector = "└── "
        else:
            connector = "├── "
        
        # Add the current item to the tree list
        tree_lines.append(prefix + connector + item)
        
        # If it's a directory, recursively get its contents
        if os.path.isdir(current_path):
            if index == total_items - 1:
                new_prefix = prefix + "    "
            else:
                new_prefix = prefix + "│   "
            # Extend tree_lines with the result from the recursive call
            tree_lines.extend(get_directory_tree(current_path, new_prefix))
    
    return tree_lines   


def openPath():
    filepath = filedialog.askdirectory()
    if filepath:
        tree_text.delete("1.0", tk.END)
        directory_tree = get_directory_tree(filepath)
        tree_text.insert(tk.END, "\n".join(directory_tree))


root = tk.Tk()
root.title("Directory Tree")

button = tk.Button(text="Open", command=openPath)
button.pack()

scrollbar = tk.Scrollbar(root)
scrollbar.pack( side = tk.RIGHT, fill=tk.Y )

tree_text = tk.Text(root, width=100, height=40, font=("Courier", 12), bg="gray1", fg="white")
tree_text.pack(fill=tk.BOTH, expand=True) 

scrollbar.config(command=tree_text.yview)
tree_text.config(yscrollcommand=scrollbar.set)

root.mainloop()
