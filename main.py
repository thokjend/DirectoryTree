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
        formatted_time = datetime.datetime.fromtimestamp(time).strftime('%d-%m-%Y %H:%M:%S')
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

# Adding padding around each widget
frame = tk.Frame(root, pady=10, padx=10, bg="gray15")
frame.pack(fill=tk.BOTH, expand=True)

# Styling and positioning the button
button = tk.Button(frame, text="Open Directory", font=("Helvetica", 12), command=openPath, bg="lightgray", fg="black")
button.pack(side=tk.TOP, fill=tk.X, pady=(10, 20))

# Styling the label and input box with spacing
label = tk.Label(frame, text="Search Directory", font=("Helvetica", 14, "bold"), bg="gray15", fg="white")
label.pack(pady=(5, 5))

input_box = tk.Entry(frame, font=("Helvetica", 16), bd=2, relief=tk.SUNKEN, width=40)
input_box.pack(pady=(5, 20))

# Text area for the directory tree output with a scrollbar
scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

tree_text = tk.Text(frame, width=100, height=40, font=("Courier", 12), bg="gray10", fg="white", yscrollcommand=scrollbar.set)
tree_text.pack(fill=tk.BOTH, expand=True)
scrollbar.config(command=tree_text.yview)

root.mainloop()