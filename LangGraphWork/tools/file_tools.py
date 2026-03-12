from langchain_core.tools import tool
import os
import inspect

current_dir = os.path.dirname(os.path.abspath(__file__)) # tools/ folder
project_root = os.path.dirname(current_dir) # LangGraphWork/ folder
BASE_DIR = os.path.join(project_root, "workspace")

if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)

def safe_path(path):
    """Guarantees that the provided path is within the BASE_DIR to prevent directory traversal."""
    joined = os.path.abspath(os.path.join(BASE_DIR, path))
    if not joined.startswith(BASE_DIR):
        raise PermissionError("Bu dizin dışına çıkma yetkin yok!")
    return joined

@tool
def list_files_recursive(path: str = ".", max_depth: int = 2):
    """
    Lists files and folders in a tree structure up to a specified depth.
    max_depth: How many levels of subdirectories to include (Default 2, Max 4).
    """
    try:
        target_root = BASE_DIR
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

        return "\n".join(output) if len(output) > 1 else "Dizin boş."

    except Exception as e:
        return f"Hata: {str(e)}"

@tool
def create_file(filename: str, content: str = ""):
    """Create a new file with the given name and content in the determined directory."""
    try:
        target = safe_path(filename)
        with open(target, "w", encoding="utf-8") as f:
            f.write(content)
        return f"{filename} oluşturuldu."
    except Exception as e:
        return f"Hata: {str(e)}"
    
@tool
def create_folder(foldername: str):
    """Creates a new folder with the given name in the determined directory."""
    try:
        target = safe_path(foldername)
        os.makedirs(target, exist_ok=True)
        return f"{foldername} klasörü oluşturuldu."
    except Exception as e:
        return f"Hata: {str(e)}"
    
@tool
def delete_file(filename: str):
    """Deletes the specified file."""
    try:
        target = safe_path(filename)
        if os.path.exists(target):
            os.remove(target)
            return f"{filename} silindi."
        else:
            return f"{filename} bulunamadı."
    except Exception as e:
        return f"Hata: {str(e)}"
    
def get_all_tools():
    """Finds all functions in this module that are decorated with @tool and returns them as a list."""
    members = inspect.getmembers(inspect.getmodule(get_all_tools))
    
    return [obj for name, obj in members if hasattr(obj, "name") and hasattr(obj, "description")]

ALL_TOOLS = get_all_tools()