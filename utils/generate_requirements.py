import os
import ast
import nbformat
import setuptools
import pkg_resources
from pathlib import Path

def extract_imports_from_py(file_path):
    """Extract import statements from a Python file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            tree = ast.parse(file.read())
        except:
            print(f"Could not parse {file_path}")
            return set()
    
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for name in node.names:
                imports.add(name.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module.split('.')[0])
    return imports

def extract_imports_from_ipynb(file_path):
    """Extract import statements from a Jupyter notebook."""
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            nb = nbformat.read(file, as_version=4)
        except:
            print(f"Could not parse {file_path}")
            return set()

    imports = set()
    for cell in nb.cells:
        if cell.cell_type == 'code':
            try:
                tree = ast.parse(cell.source)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for name in node.names:
                            imports.add(name.name.split('.')[0])
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            imports.add(node.module.split('.')[0])
            except:
                continue
    return imports

def get_installed_packages():
    """Get a dictionary of installed packages and their versions."""
    return {pkg.key: pkg.version for pkg in pkg_resources.working_set}

def main():
    # Get the project root directory (assuming this script is in utils/)
    project_root = Path(__file__).parent.parent
    
    # Initialize set for all imports
    all_imports = set()
    
    # Folders to skip
    skip_folders = {'.venv', 'venv', '.env', 'env', '__pycache__', '.git', '.pytest_cache', '.ipynb_checkpoints'}
    
    # Walk through all directories
    print(f"\nScanning project root: {project_root}\n")
    for root, dirs, files in os.walk(project_root):
        # Modify dirs in place to skip certain directories
        dirs[:] = [d for d in dirs if d not in skip_folders]
        
        relative_path = Path(root).relative_to(project_root)
        print(f"Scanning folder: {relative_path}")
        
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                imports = extract_imports_from_py(file_path)
                if imports:
                    print(f"  Found {len(imports)} imports in {file}")
                all_imports.update(imports)
            elif file.endswith('.ipynb'):
                file_path = os.path.join(root, file)
                imports = extract_imports_from_ipynb(file_path)
                if imports:
                    print(f"  Found {len(imports)} imports in {file}")
                all_imports.update(imports)
    
    print("\nAnalyzing imports...")
    # Remove standard library modules
    stdlib_modules = set(sys.stdlib_module_names)
    third_party_imports = {imp for imp in all_imports if imp not in stdlib_modules}
    
    # Get installed versions
    installed_packages = get_installed_packages()
    
    # Create requirements.txt
    print("\nGenerating requirements.txt...")
    with open('requirements.txt', 'w') as f:
        for package in sorted(third_party_imports):
            if package in installed_packages:
                f.write(f'{package}=={installed_packages[package]}\n')
            else:
                f.write(f'{package}\n') # Not installed
                print(f"Warning: Package '{package}' is imported but not installed")
    
    print(f"\nDone! Found {len(third_party_imports)} third-party packages.")

if __name__ == '__main__':
    import sys
    main() 