import os
import cv2
import subprocess
image_folder = 'D:/Kuliah/Semester_5/DatasetPPEPandu/converted_images'
            
def process_images_from_folder(image_folder, label_folder):
    nomer = 0
    for filename in os.listdir(image_folder):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(image_folder, filename)
            label_path = os.path.join(label_folder, os.path.splitext(filename)[0] + ".txt")

            # Check if the label file exists
            if not os.path.exists(label_path):
                # print(f"Label file does not exist for image {filename}. Skipping augmentation.")
                continue

            image = cv2.imread(image_path)
            if image is None:
                # print(f"Failed to read image {filename}. Skipping.")
                continue

            # Read bounding box from label file
            bbox = []
            try:
                with open(label_path, 'r') as f:
                    for line in f:
                        class_id, x_center, y_center, width, height = map(float, line.split())
                        bbox.append([class_id, x_center, y_center, width, height])
            except Exception as e:
                # print(f"Processed {label_path} images.")
                print(f"{label_path}")
                # subprocess.run(["notepad ", label_path]) 
                print(e)
                continue
            # Augment image and labels
            
            nomer += 1
            
            
process_images_from_folder(image_folder, image_folder)