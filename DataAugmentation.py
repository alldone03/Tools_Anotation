import cv2
import numpy as np
import os

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
        
        if flip_code == 1:  # Horizontal flip
            new_bbox.append([class_id, 1 - x_center, y_center, width, height])
        elif flip_code == 0:  # Vertical flip
            new_bbox.append([class_id, x_center, 1 - y_center, width, height])
        elif flip_code == -1:  # Both
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

def process_images_from_folder(image_folder, label_folder):
    nomer = 0
    for filename in os.listdir(image_folder):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(image_folder, filename)
            label_path = os.path.join(label_folder, os.path.splitext(filename)[0] + ".txt")

            # Check if the label file exists
            if not os.path.exists(label_path):
                print(f"Label file does not exist for image {filename}. Skipping augmentation.")
                continue

            image = cv2.imread(image_path)
            if image is None:
                print(f"Failed to read image {filename}. Skipping.")
                continue

            # Read bounding box from label file
            bbox = []
            with open(label_path, 'r') as f:
                for line in f:
                    class_id, x_center, y_center, width, height = map(float, line.split())
                    bbox.append([class_id, x_center, y_center, width, height])

            # Augment image and labels
            rotated = rotate_image(image, 3)
            new_bbox_rotated = rotate_bbox(bbox, image, 3)
            save_augmented_image_and_labels(rotated, new_bbox_rotated, image_path, 'rotated')

            translated = translate_image(image, 10, 20)
            new_bbox_translated = translate_bbox(bbox, 10, 20, image)
            save_augmented_image_and_labels(translated, new_bbox_translated, image_path, 'translated')

            scaled = scale_image(image, 1.5, 1.5)
            new_bbox_scaled = scale_bbox(bbox, 1.5, 1.5)
            save_augmented_image_and_labels(scaled, new_bbox_scaled, image_path, 'scaled')

            flipped = flip_image(image, 1)
            new_bbox_flipped = flip_bbox(bbox, image, 1)
            save_augmented_image_and_labels(flipped, new_bbox_flipped, image_path, 'flipped')

            nomer += 1
            print(f"Processed {filename} images.")

# Example usage
image_folder = 'C:/Users/Aldan/Desktop/sawitmini/dataset/datasedikit'
label_folder = image_folder
process_images_from_folder(image_folder, label_folder)