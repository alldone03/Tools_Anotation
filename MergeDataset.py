import os
import shutil

base_path = "C:/Users/Aldan/Desktop/IMPROTOYOTA/CAMERA 5 ZENIX.v3i.yolov8"
source_folders = ['train', 'valid', 'test']
target_image = os.path.join(base_path, 'dataset', 'images')
target_label = os.path.join(base_path, 'dataset', 'labels')

os.makedirs(target_image, exist_ok=True)
os.makedirs(target_label, exist_ok=True)

def move_all_files(source_subfolder, dest_folder):
    for root, _, files in os.walk(source_subfolder):
        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(dest_folder, file)

            base, ext = os.path.splitext(file)
            counter = 1
            while os.path.exists(dst_file):
                dst_file = os.path.join(dest_folder, f"{base}_{counter}{ext}")
                counter += 1

            shutil.move(src_file, dst_file)
            print(f"[✅] {file} dipindah ke {dest_folder}")

# Proses semua folder sumber
# for split in source_folders:
#     image_path = os.path.join(base_path, split, 'images')
#     label_path = os.path.join(base_path, split, 'labels')

#     if os.path.exists(image_path):
#         move_all_files(image_path, target_image)
#     if os.path.exists(label_path):
#         move_all_files(label_path, target_label)
for split in source_folders:
    image_path = os.path.join(base_path, split, 'images')
    label_path = os.path.join(base_path, split, 'labels')

    if os.path.exists(image_path):
        move_all_files(image_path, target_image)
        move_all_files(label_path, target_image)
    

print("\n[✔️] Semua gambar dan label berhasil digabung ke folder 'dataset/images' dan 'dataset/labels'")