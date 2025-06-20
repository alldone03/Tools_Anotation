import cv2
import numpy as np
import os
import time
import torchvision.transforms as T
from PIL import Image

def rotate_image(image, angle):
    (h, w) = image.shape[:2]
    center = (w / 2, h / 2)
    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, matrix, (w, h))
    return rotated

def translate_image(image, x, y):
    matrix = np.float32([[1, 0, x], [0, 1, y]])
    translated = cv2.warpAffine(image, matrix, (image.shape[1], image.shape[0]))
    return translated

def scale_image(image, fx, fy):
    scaled = cv2.resize(image, None, fx=fx, fy=fy)
    return scaled

def flip_image(image, flip_code):
    flipped = cv2.flip(image, flip_code)
    return flipped

def rotate_bbox(bbox, image, angle):
    h, w = image.shape[:2]
    cx, cy = w / 2, h / 2
    new_bbox = []
    for box in bbox:
        class_id, x_center, y_center, width, height = box
        x_center = x_center * w
        y_center = y_center * h
        width = width * w
        height = height * h

        coords = [(x_center - width/2, y_center - height/2), 
                  (x_center + width/2, y_center - height/2), 
                  (x_center + width/2, y_center + height/2), 
                  (x_center - width/2, y_center + height/2)]

        new_coords = []
        for x, y in coords:
            x_new = cx + (x - cx) * np.cos(np.radians(angle)) - (y - cy) * np.sin(np.radians(angle))
            y_new = cy + (x - cx) * np.sin(np.radians(angle)) + (y - cy) * np.cos(np.radians(angle))
            new_coords.append((x_new, y_new))

        x_coords, y_coords = zip(*new_coords)
        x_center_new = (min(x_coords) + max(x_coords)) / 2 / w
        y_center_new = (min(y_coords) + max(y_coords)) / 2 / h
        width_new = (max(x_coords) - min(x_coords)) / w
        height_new = (max(y_coords) - min(y_coords)) / h
        
        
        new_bbox.append([class_id, x_center_new, y_center_new, width_new, height_new])
    return new_bbox

def translate_bbox(bbox, tx, ty, image):
    h, w = image.shape[:2]
    tx /= w
    ty /= h
    new_bbox = []
    for box in bbox:
        class_id, x_center, y_center, width, height = box
       
        new_bbox.append([class_id, x_center + tx, y_center + ty, width, height])
    return new_bbox

def scale_bbox(bbox, fx, fy):
    new_bbox = []
    for box in bbox:
        class_id, x_center, y_center, width, height = box
        
        new_bbox.append([class_id, x_center, y_center, width * fx, height * fy])
    return new_bbox

def flip_bbox(bbox, image, flip_code):
    h, w = image.shape[:2]
    new_bbox = []
    for box in bbox:
        class_id, x_center, y_center, width, height = box
        
        if flip_code == 1:  
            new_bbox.append([class_id, 1 - x_center, y_center, width, height])
        elif flip_code == 0:  
            new_bbox.append([class_id, x_center, 1 - y_center, width, height])
        elif flip_code == -1:  
            new_bbox.append([class_id, 1 - x_center, 1 - y_center, width, height])
    return new_bbox

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

# ColorJitter
def color_jitter(image):
    image_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    transform = T.ColorJitter(brightness=0.4, contrast=0.4, saturation=0.4, hue=0.1)
    jittered = transform(image_pil)
    return cv2.cvtColor(np.array(jittered), cv2.COLOR_RGB2BGR)

# RandomErasing
def random_erasing(image):
    image_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    transform = T.Compose([
        T.ToTensor(),
        T.RandomErasing(p=1.0, scale=(0.02, 0.2), ratio=(0.3, 3.3), value='random'),
        T.ToPILImage()
    ])
    erased = transform(image_pil)
    return cv2.cvtColor(np.array(erased), cv2.COLOR_RGB2BGR)

# MotionBlur
def motion_blur(image, kernel_size=15):
    # Membuat kernel blur horizontal
    kernel = np.zeros((kernel_size, kernel_size))
    kernel[int((kernel_size - 1)/2), :] = np.ones(kernel_size)
    kernel = kernel / kernel_size
    blurred = cv2.filter2D(image, -1, kernel)
    return blurred

# GaussianNoise
def gaussian_noise(image, mean=0, std=15):
    noise = np.random.normal(mean, std, image.shape).astype(np.uint8)
    noisy = cv2.add(image, noise)
    return noisy

def save_augmented_image_and_labels(image, bbox, image_path, prefix):
    directory, filename = os.path.split(image_path)
    name, ext = os.path.splitext(filename)
    new_image_filename = f"{prefix}_{name}{ext}"
    new_label_filename = f"{prefix}_{name}.txt"

    cv2.imwrite(os.path.join(directory, new_image_filename), image)

    with open(os.path.join(directory, new_label_filename), 'w') as f:
        for box in bbox:
            class_id, x_center, y_center, width, height = box
            if x_center > 1:
                x_center = 1
            if y_center >1 :
                y_center=1
            if width >1 :
                width=1
            if height >1 :
                height=1
            f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

def preview_and_confirm(image, bbox):
    image_with_bboxes = draw_bboxes(image.copy(), bbox)
    cv2.imshow("Preview", image_with_bboxes)
    key = cv2.waitKey(0)
    cv2.destroyAllWindows()
    if key == ord('y') or key == ord('Y'):
        return True
    return False

def apply_sunlight_filter(image, strength=0.7):
    h, w = image.shape[:2]
    overlay = image.copy()
    sun_center = (int(w * 0.8), int(h * 0.2))  

    for y in range(h):
        for x in range(w):
            distance = np.sqrt((x - sun_center[0])**2 + (y - sun_center[1])**2)
            brightness = max(0, 1 - distance / (w / 1.2)) * strength
            overlay[y, x] = np.clip(overlay[y, x] + brightness * 255, 0, 255)

    return overlay.astype(np.uint8)

def change_brightness(image, factor):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv = np.array(hsv, dtype=np.float32)
    hsv[..., 2] = hsv[..., 2] * factor
    hsv[..., 2] = np.clip(hsv[..., 2], 0, 255)
    bright_img = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
    return bright_img

def process_images_from_folder(image_folder, label_folder):
    nomer = 0
    start_time = time.time()  # Mulai timer

    # Hitung jumlah file gambar yang valid
    image_files = [f for f in os.listdir(image_folder) if f.endswith((".jpg", ".png"))]
    total_files = len(image_files)

    for filename in image_files:
        file_start = time.time()

        image_path = os.path.join(image_folder, filename)
        label_path = os.path.join(label_folder, os.path.splitext(filename)[0] + ".txt")

        if not os.path.exists(label_path):
            print(f"Label file does not exist for image {filename}. Skipping augmentation.")
            continue

        image = cv2.imread(image_path)
        if image is None:
            print(f"Failed to read image {filename}. Skipping.")
            continue

        bbox = []
        with open(label_path, 'r') as f:
            for line in f:
                class_id, x_center, y_center, width, height = map(float, line.split())
                bbox.append([class_id, x_center, y_center, width, height])

        # rotated = rotate_image(image, 3)
        # new_bbox_rotated = rotate_bbox(bbox, image, 3)
        # save_augmented_image_and_labels(rotated, new_bbox_rotated, image_path, 'rotated')

        translated = translate_image(image, 10, 20)
        new_bbox_translated = translate_bbox(bbox, 10, 20, image)
        save_augmented_image_and_labels(translated, new_bbox_translated, image_path, 'translated')

        scaled = scale_image(image, 1.5, 1.5)
        new_bbox_scaled = scale_bbox(bbox, 1.5, 1.5)
        save_augmented_image_and_labels(scaled, new_bbox_scaled, image_path, 'scaled')

        bright = change_brightness(image, 1.0)
        save_augmented_image_and_labels(bright, bbox, image_path, 'bright')

        dark = change_brightness(image, 0.5)
        save_augmented_image_and_labels(dark, bbox, image_path, 'dark')

        dark3 = change_brightness(image, 0.3)
        save_augmented_image_and_labels(dark3, bbox, image_path, 'dark3')

        aug1 = color_jitter(image)
        save_augmented_image_and_labels(aug1, bbox, image_path, "colorjitter")

        # aug2 = random_erasing(image)
        # save_augmented_image_and_labels(aug2, bbox, image_path, "randomerasing")

        aug3 = motion_blur(image)
        save_augmented_image_and_labels(aug3, bbox, image_path, "motionblur")

        aug4 = gaussian_noise(image)
        save_augmented_image_and_labels(aug4, bbox, image_path, "gaussiannoise")
        
        nomer += 1
        progress = (nomer / total_files) * 100

        elapsed = time.time() - start_time
        avg_time = elapsed / nomer
        remaining = avg_time * (total_files - nomer)

        print(f"Processed {filename} ({progress:.2f}%) | Estimasi sisa: {remaining:.1f} detik", end='\r')

    total_time = time.time() - start_time
    print(f"\nSelesai! Total waktu: {total_time:.2f} detik")



import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--folderimage", type=str, required=True, help="Path ke folder gambar")
args = parser.parse_args()

image_folder = args.folderimage
label_folder = image_folder

process_images_from_folder(image_folder, label_folder)

# python DataAugmentation.py --folderimage "C:\Users\Aldan\Desktop\IMPROTOYOTA\CAMERA 5 FORTUNER.v2i.yolov8\mydata"

