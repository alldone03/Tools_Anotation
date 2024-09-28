import os
import shutil

# Path ke folder dataset dan file label.txt
dataset_folder = 'C:/Users/Aldan/Desktop/sawitmini/dataset/canpuranbrondol'
# label_file = 'C:/Users/Aldan Prayogi/Desktop/pythonImagedetection/labeled/labels.txt'

# Jumlah anotator
num_anotators = 5
anotator_folders = "AnotatorNie"

# Buat folder anotator jika belum ada
for i in range(1, num_anotators + 1):
    folder_name = f'{anotator_folders}/Anotator{i}'
    os.makedirs(folder_name, exist_ok=True)

# Dapatkan semua file dalam folder dataset dan urutkan
files = sorted(os.listdir(dataset_folder))

# Hitung jumlah file dan jumlah anotator
total_files = len(files)

# Hitung jumlah file per anotator
files_per_anotator = total_files // num_anotators
extra_files = total_files % num_anotators  # File sisa yang tidak terbagi rata

start_index = 0

# Bagikan file ke folder anotator
for i in range(1, num_anotators + 1):
    end_index = start_index + files_per_anotator
    if i <= extra_files:  # Jika ada file sisa, tambahkan satu file tambahan ke anotator ini
        end_index += 1
    
    anotator_folder = f'{anotator_folders}/Anotator{i}'
    
    for file in files[start_index:end_index]:
        src_path = os.path.join(dataset_folder, file)
        dest_path = os.path.join(anotator_folder, file)
        shutil.copy(src_path, dest_path)
    
    # Salin label.txt ke folder anotator
    label_dest_path = os.path.join(anotator_folder, 'labels.txt')
    src_path = os.path.join(dataset_folder, 'labels.txt')
    shutil.copy(src_path, label_dest_path)
    
    start_index = end_index  # Update start_index untuk anotator berikutnya

print("Dataset dan label.txt berhasil dibagi ke dalam folder anotator.")