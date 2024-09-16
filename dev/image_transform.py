import os
from PIL import Image
import pyheif

# Get list of HEIF and HEIC files in directory
directory = '/Users/weijithwimalasiri/Desktop/UoM_S5/CS3283_Embedded_Systems Project/Project/images'
files = [f for f in os.listdir(directory) if f.endswith('.HEIC') or f.endswith('.HEIF')]

# Create output directory if it does not exist
output_dir = os.path.join(directory, 'output')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Convert each HEIC/HEIF file to JPEG
for filename in files:
    file_path = os.path.join(directory, filename)
    
    # Use pyheif to read HEIC/HEIF image
    heif_file = pyheif.read(file_path)
    
    # Convert to PIL Image
    image = Image.frombytes(
        heif_file.mode,
        heif_file.size,
        heif_file.data,
        "raw",
        heif_file.mode,
        heif_file.stride,
    )
    
    # Save as JPEG
    image.convert('RGB').save(os.path.join(output_dir, os.path.splitext(filename)[0] + '.jpg'))

print("Conversion complete.")
