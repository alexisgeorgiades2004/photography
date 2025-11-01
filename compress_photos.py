from PIL import Image
import os
import sys

def compress_images(input_folder, output_folder=None, max_width=2000, quality=85):
    """
    Compress all images in a folder for web use
    
    Args:
        input_folder: Path to folder with original photos
        output_folder: Path to save compressed photos (defaults to input_folder + '-compressed')
        max_width: Maximum width in pixels (default 2000px)
        quality: JPEG quality 1-100 (default 85, good balance)
    """
    
    # Set output folder
    if output_folder is None:
        output_folder = f"{input_folder}-compressed"
    
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Supported image formats
    image_extensions = ('.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG')
    
    # Get all image files
    try:
        files = [f for f in os.listdir(input_folder) if f.endswith(image_extensions)]
    except FileNotFoundError:
        print(f"Error: Folder '{input_folder}' not found!")
        return
    
    if not files:
        print(f"No image files found in '{input_folder}'")
        return
    
    print(f"\nCompressing {len(files)} images from '{input_folder}'...")
    print(f"Output folder: '{output_folder}'")
    print(f"Settings: Max width={max_width}px, Quality={quality}\n")
    
    total_original_size = 0
    total_compressed_size = 0
    
    for i, filename in enumerate(files, 1):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)
        
        try:
            # Open image
            with Image.open(input_path) as img:
                # Get original size
                original_size = os.path.getsize(input_path)
                total_original_size += original_size
                
                # Convert RGBA to RGB if needed (for JPEG)
                if img.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                
                # Resize if wider than max_width
                if img.width > max_width:
                    ratio = max_width / img.width
                    new_height = int(img.height * ratio)
                    img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
                
                # Save with compression
                # Force JPEG for better compression
                output_filename = os.path.splitext(filename)[0] + '.jpg'
                output_path = os.path.join(output_folder, output_filename)
                
                img.save(output_path, 'JPEG', quality=quality, optimize=True)
                
                # Get compressed size
                compressed_size = os.path.getsize(output_path)
                total_compressed_size += compressed_size
                
                reduction = (1 - compressed_size / original_size) * 100
                
                print(f"[{i}/{len(files)}] {filename}")
                print(f"    {original_size / 1024 / 1024:.2f} MB → {compressed_size / 1024 / 1024:.2f} MB ({reduction:.1f}% reduction)")
        
        except Exception as e:
            print(f"[{i}/{len(files)}] ERROR processing {filename}: {e}")
    
    # Summary
    print(f"\n{'='*60}")
    print(f"COMPRESSION COMPLETE!")
    print(f"{'='*60}")
    print(f"Total original size:    {total_original_size / 1024 / 1024:.2f} MB")
    print(f"Total compressed size:  {total_compressed_size / 1024 / 1024:.2f} MB")
    print(f"Total saved:            {(total_original_size - total_compressed_size) / 1024 / 1024:.2f} MB")
    print(f"Overall reduction:      {(1 - total_compressed_size / total_original_size) * 100:.1f}%")
    print(f"\nCompressed images saved to: {output_folder}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Photo Compression Script for Web")
        print("=" * 50)
        print("\nUsage:")
        print("  python compress_photos.py <input_folder> [output_folder] [max_width] [quality]")
        print("\nExamples:")
        print("  python compress_photos.py 101725-DiscoveryPark")
        print("  python compress_photos.py 101725-DiscoveryPark compressed-photos")
        print("  python compress_photos.py 101725-DiscoveryPark compressed 1920 80")
        print("\nDefaults:")
        print("  output_folder: <input_folder>-compressed")
        print("  max_width:     2000px")
        print("  quality:       85 (1-100, higher = better quality but larger)")
        sys.exit(1)
    
    input_folder = sys.argv[1]
    output_folder = sys.argv[2] if len(sys.argv) > 2 else None
    max_width = int(sys.argv[3]) if len(sys.argv) > 3 else 2000
    quality = int(sys.argv[4]) if len(sys.argv) > 4 else 85
    
    compress_images(input_folder, output_folder, max_width, quality)

    #python compress_photos.py 101825-PumpkinPatch