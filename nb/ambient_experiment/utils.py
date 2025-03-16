import os
import base64
from datetime import datetime
import re
import matplotlib.pyplot as plt
from IPython.display import Image, display

def get_latest_stock_image():
    """
    Scans the stock_data_snapshots directory and returns the path to the latest image.
    Uses alphabetical sorting which works with the timestamp format in filenames.
    
    Returns:
        str: Path to the latest stock image, or None if no images found
    """
    # Get the stock_data directory path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    snapshot_dir = os.path.join(script_dir, 'stock_data', 'stock_data_snapshots')
    
    if not os.path.exists(snapshot_dir):
        print(f"Warning: Snapshot directory '{snapshot_dir}' does not exist")
        return None
    
    # Get all PNG files in the directory
    image_files = [f for f in os.listdir(snapshot_dir) 
                  if os.path.isfile(os.path.join(snapshot_dir, f)) and f.endswith('.png')]
    
    if not image_files:
        print(f"No image files found in '{snapshot_dir}'")
        return None
    
    # Sort files alphabetically (newest last with your naming convention)
    sorted_files = sorted(image_files)
    
    # Return the full path to the latest file
    latest_file = sorted_files[-1]
    return os.path.join(snapshot_dir, latest_file)

def encode_image(image_path):
    """
    Encodes an image file to base64 string.
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        str: Base64 encoded string of the image, or None if file not found
    """
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except FileNotFoundError:
        print(f"Error: Image file not found at '{image_path}'")
        return None
    except Exception as e:
        print(f"Error encoding image: {e}")
        return None

def display_stock_image(image_path=None):
    """
    Displays a stock image in a Jupyter notebook.
    
    Args:
        image_path (str, optional): Path to the image file. If None, displays the latest image.
        
    Returns:
        None: Displays the image in the notebook
    """
        
    if image_path is None:
        print("No image available to display")
        return
    
    # Check if file exists
    if not os.path.exists(image_path):
        print(f"Error: Image file not found at '{image_path}'")
        return
    
    else:
        # Display the image in the notebook
        display(Image(filename=image_path))

# Example usage
if __name__ == "__main__":
    pass