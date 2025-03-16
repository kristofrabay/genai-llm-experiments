import os
import shutil

def flush_snapshot_directory():
    """
    Removes all files from the stock_data_snapshots directory
    while preserving the directory itself.
    """
    # Use absolute path based on the script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    snapshot_dir = os.path.join(script_dir, 'stock_data_snapshots')
    
    # Check if directory exists
    if not os.path.exists(snapshot_dir):
        print(f"Directory '{snapshot_dir}' does not exist. Creating it...")
        os.makedirs(snapshot_dir)
        print(f"Created empty directory '{snapshot_dir}'")
        return
    
    # Count files before deletion
    files = [f for f in os.listdir(snapshot_dir) if os.path.isfile(os.path.join(snapshot_dir, f))]
    file_count = len(files)
    
    # Remove all files in the directory
    for filename in files:
        file_path = os.path.join(snapshot_dir, filename)
        try:
            os.unlink(file_path)
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")
    
    print(f"Successfully removed {file_count} files from '{snapshot_dir}'")

if __name__ == "__main__":
    flush_snapshot_directory() 