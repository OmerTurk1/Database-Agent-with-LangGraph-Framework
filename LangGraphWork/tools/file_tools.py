import shutil
import sys
from langchain_core.tools import tool, BaseTool
import os
import inspect

current_dir = os.path.dirname(os.path.abspath(__file__)) # tools/ folder
project_root = os.path.dirname(current_dir) # LangGraphWork/ folder
BASE_DIR = os.path.join(project_root, "workspace")

if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)

def _safe_path(path):
    """Guarantees that the provided path is within the BASE_DIR to prevent directory traversal."""
    joined = os.path.abspath(os.path.join(BASE_DIR, path))
    if not joined.startswith(BASE_DIR):
        raise PermissionError("You are not allowed to access paths outside the workspace!")
    return joined

@tool
def list_files_recursive(path: str = ".", max_depth: int = 2):
    """
    Lists files and folders in a tree structure up to a specified depth.
    max_depth: How many levels of subdirectories to include (Default 2, Max 4).
    """
    try:
        target_root = BASE_DIR
        if not path==".":
            target_root = os.path.join(BASE_DIR, path)
        actual_depth_limit = min(max_depth, 4)
        
        output = []

        def build_tree(current_path, prefix="", depth=0):
            if depth > actual_depth_limit:
                return

            try:
                items = sorted(os.listdir(current_path), key=lambda x: (not os.path.isdir(os.path.join(current_path, x)), x.lower()))
            except PermissionError:
                return 

            for i, item in enumerate(items):
                full_path = os.path.join(current_path, item)
                is_last = (i == len(items) - 1)
                
                connector = "└── " if is_last else "├── "
                
                icon = "📂 " if os.path.isdir(full_path) else "📄 "
                output.append(f"{prefix}{connector}{icon}{item}")

                if os.path.isdir(full_path) and depth < actual_depth_limit:
                    new_prefix = prefix + ("    " if is_last else "│   ")
                    build_tree(full_path, new_prefix, depth + 1)

        output.append(f"📂 {os.path.basename(os.path.abspath(target_root)) or target_root}/")
        build_tree(target_root)

        return "\n".join(output) if len(output) > 1 else "List is empty."

    except Exception as e:
        return f"Error: {str(e)}"

@tool
def create_file(filename: str, content: str = ""):
    """Create a new file with the given name and content in the determined directory."""
    try:
        target = _safe_path(filename)
        with open(target, "w", encoding="utf-8") as f:
            f.write(content)
        return f"{filename} created."
    except Exception as e:
        return f"Error: {str(e)}"
    
@tool
def create_folder(foldername: str):
    """Creates a new folder with the given name in the determined directory."""
    try:
        target = _safe_path(foldername)
        os.makedirs(target, exist_ok=True)
        return f"{foldername} folder created."
    except Exception as e:
        return f"Error: {str(e)}"
    
@tool
def read_file(filename: str):
    """
    Reads and returns the content of the specified file.
    if filename is just a word, it will search on workspace;
    and if it is a path, it will search on that path.
    """
    try:
        if os.path.isabs(filename): # if it's an absolute path, use it directly
            target = filename
        else: # only filename provided, search in workspace
            target = _safe_path(filename)
        if os.path.exists(target) and os.path.isfile(target):
            with open(target, "r", encoding="utf-8") as f:
                return f.read()
        else:
            return f"{filename} could not be found"
    except Exception as e:
        return f"Error: {str(e)}"

@tool
def edit_file(filename: str, new_content: str, mode: str = "w"):
    """
    Edits an existing file by replacing its content with new_content.
    mode: "w": replace or "a": append
    """
    try:
        if mode not in ["w", "a"]:
            return "Invalid mode. Use 'w' or 'a'."
        target = _safe_path(filename)
        if os.path.exists(target) and os.path.isfile(target):
            with open(target, mode, encoding="utf-8") as f:
                f.write(new_content)
            return f"{filename} updated."
        else:
            return f"{filename} could not be found."
    except Exception as e:
        return f"Error: {str(e)}"

@tool
def rename_file_or_folder(old_name: str, new_name: str):
    """Renames a file or folder from old_name to new_name."""
    try:
        old_target = _safe_path(old_name)
        new_target = _safe_path(new_name)
        if os.path.exists(old_target):
            os.rename(old_target, new_target)
            return f"{old_name} renamed to {new_name}."
        else:
            return f"{old_name} could not be found."
    except Exception as e:
        return f"Error: {str(e)}"

@tool
def move_file_or_folder(source: str, destination: str):
    """Moves a file or folder from source to destination."""
    try:
        source_target = _safe_path(source)
        destination_target = _safe_path(destination)
        if os.path.exists(source_target):
            shutil.move(source_target, destination_target)
            return f"{source} moved to {destination}."
        else:
            return f"{source} could not be found."
    except Exception as e:
        return f"Error: {str(e)}"
    
@tool
def copy_file_or_folder(source: str, destination: str):
    """Copies a file or folder from source to destination."""
    try:
        source_target = _safe_path(source)
        destination_target = _safe_path(destination)
        if os.path.exists(source_target):
            if os.path.isdir(source_target):
                shutil.copytree(source_target, destination_target)
            else:
                shutil.copy2(source_target, destination_target)
            return f"{source} copied to {destination}."
        else:
            return f"{source} could not be found."
    except Exception as e:
        return f"Error: {str(e)}"

@tool
def delete_file(filename: str):
    """Deletes the specified file."""
    try:
        target = _safe_path(filename)
        if os.path.exists(target):
            os.remove(target)
            return f"{filename} deleted."
        else:
            return f"{filename} could not be found."
    except Exception as e:
        return f"Error: {str(e)}"
    
@tool
def delete_folder(foldername: str, delete_childs: bool = False):
    """Deletes the specified folder and all its contents."""
    try:
        target = _safe_path(foldername)
        if os.path.exists(target) and os.path.isdir(target):
            if delete_childs:
                shutil.rmtree(target)
            else:
                os.rmdir(target)
            return f"{foldername} deleted."
        else:
            return f"{foldername} could not be found."
    except Exception as e:
        return f"Error: {str(e)}"

def _get_all_tools():
    """Dynamically retrieves all functions decorated with @tool in this module."""
    module = sys.modules[__name__]
    members = inspect.getmembers(module)
    return [obj for name, obj in members if isinstance(obj, BaseTool)]

ALL_TOOLS = _get_all_tools()