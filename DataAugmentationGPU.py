import cv2
import numpy as np
import os
import albumentations as A

def draw_bboxes(image, bbox):
    h, w = image.shape[:2]
    for box in bbox:
        class_id, x_center, y_center, width, height = box
        x_center = int(x_center * w)
        y_center = int(y_center * h)
        width = int(width * w)
        height = int(height * h)
        x_min = x_center - width // 2
        y_min = y_center - height // 2
        x_max = x_center + width // 2
        y_max = y_center + height // 2
        cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
    return image

def save_augmented_image_and_labels(image, bbox, image_path, prefix):
    directory, filename = os.path.split(image_path)
    name, ext = os.path.splitext(filename)
    new_image_filename = f"{prefix}_{name}{ext}"
    new_label_filename = f"{prefix}_{name}.txt"

    cv2.imwrite(os.path.join(directory, new_image_filename), image)
    with open(os.path.join(directory, new_label_filename), 'w') as f:
        for box in bbox:
            class_id, x_center, y_center, width, height = box
            x_center = min(x_center, 1)
            y_center = min(y_center, 1)
            width = min(width, 1)
            height = min(height, 1)
            f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

def process_images_from_folder(image_folder, label_folder):
    transform = A.Compose([
        A.RandomBrightnessContrast(p=0.5),
        A.HueSaturationValue(p=0.5),
        A.RandomSunFlare(flare_roi=(0, 0, 1, 0.5), angle_lower=0.1, angle_upper=1.0, num_flare_circles_lower=6, p=0.4),
        A.HorizontalFlip(p=0.5),
    ], bbox_params=A.BboxParams(format='yolo', label_fields=['class_labels']))

    for filename in os.listdir(image_folder):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(image_folder, filename)
            label_path = os.path.join(label_folder, os.path.splitext(filename)[0] + ".txt")

            if not os.path.exists(label_path):
                print(f"Tidak ada file label untuk {filename}. Lewati.")
                continue

            image = cv2.imread(image_path)
            if image is None:
                print(f"Gagal membaca {filename}. Lewati.")
                continue

            bbox = []
            with open(label_path, 'r') as f:
                for line in f:
                    class_id, x_center, y_center, width, height = map(float, line.split())
                    bbox.append([class_id, x_center, y_center, width, height])

            albumentations_bbox = [box[1:] for box in bbox]
            class_labels = [int(box[0]) for box in bbox]

            try:
                transformed = transform(image=image, bboxes=albumentations_bbox, class_labels=class_labels)
                aug_image = transformed['image']
                aug_bbox = transformed['bboxes']
                aug_labels = transformed['class_labels']
                new_bbox = [[label] + list(box) for label, box in zip(aug_labels, aug_bbox)]
                save_augmented_image_and_labels(aug_image, new_bbox, image_path, 'aug')
                print(f"Sukses augmentasi: {filename}")
            except Exception as e:
                print(f"Error augmentasi {filename}: {e}")

# Ganti path ini sesuai lokasi dataset kamu
image_folder = 'C:/Users/Aldan/Desktop/sawitmini/dataset/datasedikit'
label_folder = image_folder
process_images_from_folder(image_folder, label_folder)