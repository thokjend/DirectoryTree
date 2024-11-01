import os
import tkinter as tk
import datetime
from tkinter import filedialog

def get_directory_tree(starting_directory, prefix=""):
    # List to hold each line of the directory tree
    tree_lines = []
    file_count = 0
    directory_count = 0
    file_size = 0
    
    # List the contents of the current directory
    items = os.listdir(starting_directory)
    items = sorted(items, key=lambda x: (not os.path.isdir(os.path.join(starting_directory, x)), x))
    total_items = len(items)
    
    for index, item in enumerate(items):
        current_path = os.path.join(starting_directory, item)
        time = os.stat(current_path).st_ctime
        formatted_time = datetime.datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')
        #dt = str(datetime.datetime.fromtimestamp(time))
        
        if index == total_items - 1:
            connector = "└── "
        else:
            connector = "├── "
        
        # Add the current item to the tree list
        tree_lines.append(f"{prefix}{connector}{item}   [Created: {formatted_time}]")
        
        # If it's a directory, recursively get its contents
        if os.path.isdir(current_path):
            directory_count += 1
            if index == total_items - 1:
                new_prefix = prefix + "    "    
            else:
                new_prefix = prefix + "│   "
            # Extend tree_lines with the result from the recursive call
            sub_tree, sub_file_count, sub_directory_count, sub_file_size = get_directory_tree(current_path, new_prefix)
            tree_lines.extend(sub_tree)
            file_count += sub_file_count
            directory_count += sub_directory_count
            file_size += sub_file_size
            
        else:
            file_count += 1
            file_size += os.stat(current_path).st_size
    
    return tree_lines, file_count, directory_count, file_size

def format_size(size_in_bytes):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_in_bytes < 1024:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024
    return f"{size_in_bytes:.2f} TB"

def openPath():
    filepath = filedialog.askdirectory()
    if filepath:
        tree_text.delete("1.0", tk.END)
        directory_tree, file_count, directory_count, file_size = get_directory_tree(filepath)
        tree_text.insert(tk.END, "\n".join(directory_tree))
        tree_text.insert(tk.END, f"\n\nTotal files: {file_count}")
        tree_text.insert(tk.END, f"\nTotal directories: {directory_count}")
        tree_text.insert(tk.END, f"\nTotal size: {format_size(file_size)}")

root = tk.Tk()
root.title("Directory Tree")

button = tk.Button(text="Open", command=openPath)
button.pack(side = tk.TOP, fill=tk.X)

scrollbar = tk.Scrollbar(root)
scrollbar.pack( side = tk.RIGHT, fill=tk.Y )

tree_text = tk.Text(root, width=100, height=40, font=("Courier", 12), bg="gray1", fg="white")
tree_text.pack(fill=tk.BOTH, expand=True) 

scrollbar.config(command=tree_text.yview)
tree_text.config(yscrollcommand=scrollbar.set)

root.mainloop()
