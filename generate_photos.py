import os
import sys

def generate_photo_html(folder_path, folder_name=None):
    """
    Generate HTML code for all images in a folder
    
    Args:
        folder_path: Path to the folder containing images
        folder_name: Optional custom folder name for the path (defaults to folder_path)
    """
    
    # Get list of image files
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.JPG', '.JPEG', '.PNG')
    
    try:
        files = [f for f in os.listdir(folder_path) if f.endswith(image_extensions)]
        files.sort()  # Sort alphabetically
    except FileNotFoundError:
        print(f"Error: Folder '{folder_path}' not found!")
        return
    
    if not files:
        print(f"No image files found in '{folder_path}'")
        return
    
    # Use folder name from path if not provided
    if folder_name is None:
        folder_name = os.path.basename(folder_path)
    
    print(f"\nFound {len(files)} images in '{folder_path}'")
    print("\n=== HTML CODE FOR PHOTO GRID ===\n")
    
    # Generate HTML for photo grid items
    for i, filename in enumerate(files):
        print(f'            <div class="photo-item" onclick="openLightbox({i})">')
        print(f'                <img src="{folder_name}/{filename}" alt="{filename}">')
        print(f'            </div>')
    
    print("\n=== JAVASCRIPT IMAGE ARRAY ===\n")
    print("        const images = [")
    
    # Generate JavaScript array
    for filename in files:
        print(f"            '{folder_name}/{filename}',")
    
    print("        ];")
    print(f"\n=== TOTAL: {len(files)} images ===\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_photos.py <folder_path> [folder_name]")
        print("\nExample:")
        print("  python generate_photos.py 101725-DiscoveryPark")
        print("  python generate_photos.py ./photos/nature nature")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    folder_name = sys.argv[2] if len(sys.argv) > 2 else None
    
    generate_photo_html(folder_path, folder_name)


#python generate_photos.py 101725-DiscoveryPark-compressed