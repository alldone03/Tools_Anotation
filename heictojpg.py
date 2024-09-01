import os
from PIL import Image
from pillow_heif import register_heif_opener

# Register HEIF opener
register_heif_opener()

def convert_heic_folder(input_folder, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate through all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".heic"):
            heic_path = os.path.join(input_folder, filename)
            jpg_filename = os.path.splitext(filename)[0] + ".jpg"
            jpg_path = os.path.join(output_folder, jpg_filename)

            # Open and convert HEIC to JPG
            image = Image.open(heic_path)
            image.save(jpg_path, format='jpeg')
            print(f"Converted {heic_path} to {jpg_path}")

# Example usage
input_folder = 'D:/Kuliah/Semester_5/DatasetPPEPandu'
output_folder = 'D:/Kuliah/Semester_5/DatasetPPEPandu/converted_images'
convert_heic_folder(input_folder, output_folder)