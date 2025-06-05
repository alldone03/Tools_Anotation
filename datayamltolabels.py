import yaml
import os

# Path ke file data.yml

data_yml_path = "C:/Users/Aldan/Desktop/IMPROTOYOTA/CAMERA 5 ZENIX.v3i.yolov8/data.yaml"

# Ambil direktori dari data.yml
base_dir = os.path.dirname(os.path.abspath(data_yml_path))

# Buka dan baca file YAML
with open(data_yml_path, 'r') as f:
    data = yaml.safe_load(f)

# Ambil bagian names
names = data.get('names', [])

# Buat path untuk labels.txt di direktori yang sama
labels_txt_path = os.path.join(base_dir, 'labels.txt')

# Simpan ke labels.txt
with open(labels_txt_path, 'w') as f:
    for name in names:
        f.write(name + '\n')

print(f"labels.txt berhasil dibuat di: {labels_txt_path}")