import os
from PIL import Image

def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def yolo_to_absolute(size, box):
    dw = size[0]
    dh = size[1]
    x = box[0] * dw
    y = box[1] * dh
    w = box[2] * dw
    h = box[3] * dh
    x_min = int(x - w / 2)
    y_min = int(y - h / 2)
    x_max = int(x + w / 2)
    y_max = int(y + h / 2)
    return (x_min, y_min, x_max, y_max)

def stretch_and_save_image(image_path, labels, output_dir):
    # Open an image file
    with Image.open(image_path) as img:
        img_width, img_height = img.size

        for label in labels:
            classification = label[0]
            x_center = label[1]
            y_center = label[2]
            width = label[3]
            height = label[4]

            # Convert YOLO format to absolute coordinates
            box = yolo_to_absolute((img_width, img_height), (x_center, y_center, width, height))

            # Create directory for the classification if it doesn't exist
            class_dir = os.path.join(output_dir, str(classification))
            create_dir(class_dir)

            # Crop the image
            cropped_img = img.crop(box)

            # Resize the cropped image to 224x224 (stretching it)
            resized_img = cropped_img.resize((224, 224))

            # Save the resized and stretched image
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            stretched_img_path = os.path.join(class_dir, f"{base_name}_{classification}.jpg")
            resized_img.save(stretched_img_path)

def process_dataset(dataset_dir, output_dir):
    # Process each image and its label
    for image_file in os.listdir(dataset_dir):
        if image_file.endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(dataset_dir, image_file)
            label_path = os.path.splitext(image_path)[0] + '.txt'
            
            if os.path.exists(label_path):
                labels = []
                with open(label_path, 'r') as file:
                    for line in file:
                        parts = line.strip().split()
                        label = [int(float(parts[0])), float(parts[1]), float(parts[2]), float(parts[3]), float(parts[4])]
                        labels.append(label)

                stretch_and_save_image(image_path, labels, output_dir)
# Define paths
dataset_dir = '../dataset4menyatu'
output_dir = './output'

# Create output directory if it doesn't exist

create_dir(output_dir)

# Process the dataset
process_dataset(dataset_dir, output_dir)