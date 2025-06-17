import os
import shutil
import argparse
import yaml



# python MergeDataset.py --base_path "C:/Users/Aldan/Desktop/ImproTYT/ZENIX/CAMERA 5 ZENIX.v4i.yolov8" --output_folder "C:/Users/Aldan/Desktop/ImproTYT/ZENIX/CAMERA 5 ZENIX.v4i.yolov8/dataset/images"


# Parsing argumen dari terminal
parser = argparse.ArgumentParser(description="Gabungkan gambar dan label, lalu ambil label dari data.yaml")
parser.add_argument('--base_path', required=True, help='Folder utama yang berisi train/valid/test dan data.yaml')
parser.add_argument('--output_folder', required=True, help='Folder tujuan untuk semua file campuran (images + labels)')
parser.add_argument('--label_output', default='labels.txt', help='Nama file output untuk daftar label dari data.yaml')

args = parser.parse_args()

base_path = args.base_path
output_folder = args.output_folder
labels_txt_path = os.path.join(output_folder, args.label_output)

source_folders = ['train', 'valid', 'test']
os.makedirs(output_folder, exist_ok=True)

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

# Pindahkan semua file dari train/valid/test
for split in source_folders:
    image_path = os.path.join(base_path, split, 'images')
    label_path = os.path.join(base_path, split, 'labels')

    if os.path.exists(image_path):
        move_all_files(image_path, output_folder)
    if os.path.exists(label_path):
        move_all_files(label_path, output_folder)

# Ambil label dari data.yaml
yaml_path = os.path.join(base_path, 'data.yaml')
if os.path.exists(yaml_path):
    with open(yaml_path, 'r', encoding='utf-8') as yf:
        data_yaml = yaml.safe_load(yf)
        if 'names' in data_yaml:
            with open(labels_txt_path, 'w', encoding='utf-8') as out_file:
                out_file.write("\n".join(data_yaml['names']))
            print(f"/n[📝] File {args.label_output} berhasil dibuat dari data.yaml")
        else:
            print("[⚠️] Bagian 'names' tidak ditemukan di data.yaml")
else:
    print("[⚠️] File data.yaml tidak ditemukan!")

print("/n[✔️] Semua file berhasil dicampur ke folder output.")