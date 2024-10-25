import os
from dotenv import load_dotenv

load_dotenv()
starting_directory = os.getenv("STARTING_DIRECTORY")

def print_directory_tree(starting_directory, prefix=""):
    # List the contents of the current directory
    items = os.listdir(starting_directory)
    
    # Sort the items to show directories first and files after
    items = sorted(items, key=lambda x: (not os.path.isdir(os.path.join(starting_directory, x)), x))
    
    # Get total number of items
    total_items = len(items)
    
    # Loop through each item
    for index, item in enumerate(items):
        # Define the current path
        current_path = os.path.join(starting_directory, item)
        
        # Check if this is the last item
        if index == total_items - 1:
            connector = "└── "  # Use this for the last item
        else:
            connector = "├── "  # Use this for non-last items
        
        # Print directory or file name with correct indentation
        print(prefix + connector + item)
        
        # If it's a directory, recursively call the function to print its contents
        if os.path.isdir(current_path):
            # If it's the last item, pass updated prefix to avoid the vertical line
            if index == total_items - 1:
                new_prefix = prefix + "    "
            else:
                new_prefix = prefix + "│   "
            print_directory_tree(current_path, new_prefix)

print_directory_tree(starting_directory)            


""" 
def list_directory_tree_with_os_walk(starting_directory):
    for root, directories, files in os.walk(starting_directory):
        print(f"Directory: {root}")
        for file in files:
            print(f"  File: {file}")

list_directory_tree_with_os_walk(starting_directory) 
"""

""" 
from pathlib import Path
def list_directory_tree_with_pathlib(starting_directory):
    path_object = Path(starting_directory)
    for file_path in path_object.rglob('*'):
        if file_path.is_file():
            print(f"File: {file_path}")
        elif file_path.is_dir():
            print(f"Directory: {file_path}")
list_directory_tree_with_pathlib(starting_directory)
"""