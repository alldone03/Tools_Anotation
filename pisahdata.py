
import os
import shutil
from sklearn.model_selection import train_test_split

import time

# Menggunakan argparse untuk mengambil argumen dari command line
# python pisahdata.py --img_label_dir "C:\Users\Aldan\Desktop\ImproTYT\FORTUNER\CAMERA 5 FORTUNER.v3i.yolov8\dataset_filtered_cropped_rescaled_1.5" --save_to_folder "E:\Fortuner_train"

import argparse
import os

def parse_args():
    parser = argparse.ArgumentParser(description="Script untuk mengatur path dataset")
    parser.add_argument('--img_label_dir', type=str, required=True,
                        help='Path ke folder gambar dan label (YOLO format)')
    parser.add_argument('--save_to_folder', type=str, default='./datasetTrain',
                        help='Folder tujuan untuk menyimpan hasil')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()

    img_dir = args.img_label_dir
    label_dir = img_dir  # karena satu folder
    save_to_folder = args.save_to_folder

    print("Path gambar dan label:", img_dir)
    print("Folder tujuan:", save_to_folder)

images = [f for f in os.listdir(img_dir) if f.endswith('.jpg')]
labels = [f for f in os.listdir(label_dir) if f.endswith('.txt')]

# Cek apakah folder sudah ada
if not os.path.exists(save_to_folder):
    # Jika belum ada, buat folder
    os.makedirs(save_to_folder)
    print(f"Folder '{save_to_folder}' berhasil dibuat.")
else:
    print(f"Folder '{save_to_folder}' sudah ada.")


images.sort()
labels.sort()


image_basenames = set(os.path.splitext(f)[0] for f in images)
label_basenames = set(os.path.splitext(f)[0] for f in labels)
common_basenames = list(image_basenames.intersection(label_basenames))

images = [f + '.jpg' for f in common_basenames]
labels = [f + '.txt' for f in common_basenames]


train_val_imgs, test_imgs, train_val_lbls, test_lbls = train_test_split(images, labels, test_size=0.1, random_state=42)


train_imgs, val_imgs, train_lbls, val_lbls = train_test_split(train_val_imgs, train_val_lbls, test_size=0.2222, random_state=42)


def move_files(file_list, src_dir, dest_dir):
    total = len(file_list)
    start_time = time.time()

    for i, file in enumerate(file_list, 1):
        shutil.move(os.path.join(src_dir, file), os.path.join(dest_dir, file))

        elapsed = time.time() - start_time
        avg_time = elapsed / i
        remaining_time = avg_time * (total - i)

        percent = (i / total) * 100
        print(f"[MOVE] {percent:.2f}% ({i}/{total}) | Estimasi sisa: {remaining_time:.1f} detik", end='\r')

    print("\nSelesai!")

def copy_files(file_list, src_dir, dest_dir):
    total = len(file_list)
    start_time = time.time()

    for i, file in enumerate(file_list, 1):
        shutil.copy(os.path.join(src_dir, file), os.path.join(dest_dir, file))

        elapsed = time.time() - start_time
        avg_time = elapsed / i
        remaining_time = avg_time * (total - i)

        percent = (i / total) * 100
        print(f"[COPY] {percent:.2f}% ({i}/{total}) | Estimasi sisa: {remaining_time:.1f} detik", end='\r')

    print("\nSelesai!")



os.makedirs(save_to_folder+'/train/images', exist_ok=True)
os.makedirs(save_to_folder+'/val/images', exist_ok=True)
os.makedirs(save_to_folder+'/test/images', exist_ok=True)
os.makedirs(save_to_folder+'/train/labels', exist_ok=True)
os.makedirs(save_to_folder+'/val/labels', exist_ok=True)
os.makedirs(save_to_folder+'/test/labels', exist_ok=True)



copy_files(train_imgs, img_dir, save_to_folder+'/train/images')
copy_files(val_imgs, img_dir, save_to_folder+'/val/images')
copy_files(test_imgs, img_dir, save_to_folder+'/test/images')
copy_files(train_lbls, label_dir, save_to_folder+'/train/labels')
copy_files(val_lbls, label_dir, save_to_folder+'/val/labels')
copy_files(test_lbls, label_dir, save_to_folder+'/test/labels')

print("Dataset has been split and moved to respective directories.")

import yaml

with open(img_dir+'/labels.txt', 'r') as file:
    class_names = [line.strip() for line in file]

print(class_names)

data = {
    
    'train': 'train/images',
    'val': 'val/images',
    'test': 'test/images',
    'nc': len(class_names),
    'names': class_names
}


with open(save_to_folder+'/dataset.yaml', 'w') as file:
    yaml.dump(data, file, default_flow_style=False)

print("YAML file created successfully.")
