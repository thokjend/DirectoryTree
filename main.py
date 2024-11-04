import os
import tkinter as tk
import datetime
from tkinter import filedialog

history = []
history_index = -1

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
        time = os.stat(current_path).st_birthtime
        formatted_time = datetime.datetime.fromtimestamp(time).strftime('%d-%m-%Y %H:%M:%S')
        
        if index == total_items - 1:
            connector = "└── "
        else:
            connector = "├── "
        
        # Add the current item to the tree list
        if os.path.isdir(current_path):
            directory_count += 1
            tree_lines.append((f"{prefix}{connector}{item}   [Created: {formatted_time}]", current_path))
            # Extend tree_lines with the result from the recursive call
            new_prefix = prefix + ("    " if index == total_items - 1 else "│   ")
            sub_tree, sub_file_count, sub_directory_count, sub_file_size = get_directory_tree(current_path, new_prefix)
            tree_lines.extend(sub_tree)
            file_count += sub_file_count
            directory_count += sub_directory_count
            file_size += sub_file_size
        else:
            file_count += 1
            file_size += os.stat(current_path).st_size
            tree_lines.append((f"{prefix}{connector}{item}   [Created: {formatted_time}]", None))
    
    return tree_lines, file_count, directory_count, file_size

def format_size(size_in_bytes):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_in_bytes < 1024:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024
    return f"{size_in_bytes:.2f} TB"

def openPath():
    global filepath, history, history_index
    filepath = filedialog.askdirectory()
    if filepath:
        history = [filepath]
        history_index = 0
        update_navigation_buttons()
        path_label.config(text=f"Current Path: {filepath}")
        input_box.config(state="normal")
        load_directory_tree(filepath)
    else:
        input_box.config(state="disabled")

def load_directory_tree(path):
    global directory_tree, file_count, directory_count, file_size, history_index
    directory_tree, file_count, directory_count, file_size = get_directory_tree(path)
    path_label.config(text=f"Current Path: {path}")
    display_tree(directory_tree, show_totals=True)
    if history and history[history_index] != path:
        history.append(path)
        history_index += 1
        update_navigation_buttons()

def display_tree(lines, show_totals=False):
    tree_text.delete("1.0", tk.END)  # Clear the text area
    for idx, (line, path) in enumerate(lines):
        # Split the line into parts: prefix, connector, directory name, and time
        parts = line.split("   [Created: ")  # Split on the time part
        main_text = parts[0]
        time_text = f"   [Created: {parts[1]}" if len(parts) > 1 else ""
        
        # Extract the directory name only
        prefix, directory_name = main_text.rsplit(" ", 1)  # Split on the last space
        full_line = f"{prefix} {directory_name}{time_text}\n"
        
        # Insert the line
        line_index = f"{idx + 1}.0"
        tree_text.insert(line_index, full_line)
        
        # Highlight only the directory name part
        directory_name_start = f"{idx + 1}.{len(prefix) + 1}"
        directory_name_end = f"{idx + 1}.{len(prefix) + 1 + len(directory_name)}"
        
        if path:  # Bind click event only for directories
            tree_text.tag_add(f"dir_{idx}", directory_name_start, directory_name_end)
            tree_text.tag_bind(f"dir_{idx}", "<Button-1>", lambda e, p=path: load_directory_tree(p))
            tree_text.tag_config(f"dir_{idx}", foreground="yellow")  # Apply color only to the directory name
    
    if show_totals:
        tree_text.insert(tk.END, f"\n\nTotal files: {file_count}")
        tree_text.insert(tk.END, f"\nTotal directories: {directory_count}")
        tree_text.insert(tk.END, f"\nTotal size: {format_size(file_size)}")

def check(e):
    typed = input_box.get().lower()
    if typed == "":
        display_tree(directory_tree, show_totals=True)  # Show full tree with totals if search box is empty
    else:
        filtered_lines = [(line, path) for line, path in directory_tree if typed in line.lower()]
        display_tree(filtered_lines)


def go_back():
    global history_index
    if history_index > 0:
        history_index -= 1
        load_directory_tree(history[history_index])
        update_navigation_buttons()

def go_forward():
    global history_index
    if history_index < len(history) - 1:
        history_index += 1
        load_directory_tree(history[history_index])
        update_navigation_buttons()

def update_navigation_buttons():
    back_button.config(state="normal" if history_index > 0 else "disabled")
    forward_button.config(state="normal" if history_index < len(history) - 1 else "disabled")


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

input_box = tk.Entry(frame, font=("Helvetica", 16), bd=2, relief=tk.SUNKEN, width=40, state="disabled")
input_box.pack(pady=(5, 20))
input_box.bind("<KeyRelease>", check)

nav_frame = tk.Frame(frame, bg="gray15")
nav_frame.pack(pady=(5, 5))

back_button = tk.Button(nav_frame, text="←", state="disabled", command=go_back)
back_button.pack(side=tk.LEFT, padx=5)

forward_button = tk.Button(nav_frame, text="→", state="disabled", command=go_forward)
forward_button.pack()

path_label = tk.Label(frame, text="Current Path: ", font=("Helvetica", 14, "bold"), bg="gray15", fg="white")
path_label.pack(pady=(5, 10))

# Text area for the directory tree output with a scrollbar
scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

tree_text = tk.Text(frame, width=125, height=40, font=("Courier", 12), bg="gray10", fg="white", yscrollcommand=scrollbar.set)
tree_text.pack(fill=tk.BOTH, expand=True)
scrollbar.config(command=tree_text.yview)

root.mainloop()
