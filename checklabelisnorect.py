import os

# Daftar folder kamera
camera_folders = [
    "C:/Users/Aldan/Desktop/IMPROTOYOTA/CAMERA 9 ZENIX.v1i.yolov8",
    "C:/Users/Aldan/Desktop/IMPROTOYOTA/CAMERA 8 FORTUNER.v1i.yolov8",
    "C:/Users/Aldan/Desktop/IMPROTOYOTA/CAMERA 8 INNOVA.v1i.yolov8",
    "C:/Users/Aldan/Desktop/IMPROTOYOTA/CAMERA 8 ZENIX.v1i.yolov8",
    "C:/Users/Aldan/Desktop/IMPROTOYOTA/CAMERA 9 FORTUNER.v1i.yolov8",
    "C:/Users/Aldan/Desktop/IMPROTOYOTA/CAMERA 9 INNOVA.v1i.yolov8"
]

# Simpan error
missing_labels = []
empty_labels = []
format_errors = []
range_errors = []
value_errors = []

for folder in camera_folders:
    image_folder = os.path.join(folder, 'dataset', 'images')
    
    print(f"\n📂 Cek folder: {image_folder}")

    if not os.path.exists(image_folder):
        print(f"[❌] Folder gambar tidak ditemukan: {image_folder}")
        continue

    image_files = [f for f in os.listdir(image_folder) if f.endswith('.jpg')]

    for img_file in image_files:
        label_file = img_file.replace('.jpg', '.txt')
        label_path = os.path.join(image_folder, label_file)

        if not os.path.exists(label_path):
            print(f"[❌] Label tidak ditemukan untuk: {img_file}")
            missing_labels.append(label_path)
            continue

        with open(label_path, 'r') as f:
            lines = f.readlines()
            if not lines:
                print(f"[⚠️] Label kosong di: {label_path}")
                empty_labels.append(label_path)
                continue

            valid = True
            for i, line in enumerate(lines):
                parts = line.strip().split()
                if len(parts) != 5:
                    print(f"[❌] Format salah di baris {i+1} file {label_path}: {line.strip()}")
                    format_errors.append(label_path)
                    valid = False
                    break

                try:
                    cls, x, y, w, h = map(float, parts)
                    if not (0 <= x <= 1 and 0 <= y <= 1 and 0 <= w <= 1 and 0 <= h <= 1):
                        print(f"[❌] Nilai di luar range 0–1 di baris {i+1} file {label_path}")
                        range_errors.append(label_path)
                        valid = False
                        break
                except ValueError:
                    print(f"[❌] Tidak bisa konversi ke float di file {label_path}, baris {i+1}")
                    value_errors.append(label_path)
                    valid = False
                    break

            if valid:
                print(f"[✅] Label OK: {label_path}")

# Ringkasan error
print("\n📋 Ringkasan Path Bermasalah:\n")

if missing_labels:
    print(f"[❌] Label Tidak Ditemukan ({len(missing_labels)}):")
    for path in missing_labels:
        print(f"  - {path}")

if empty_labels:
    print(f"\n[⚠️] Label Kosong ({len(empty_labels)}):")
    for path in empty_labels:
        print(f"  - {path}")

if format_errors:
    print(f"\n[❌] Format Salah ({len(format_errors)}):")
    for path in format_errors:
        print(f"  - {path}")

if range_errors:
    print(f"\n[❌] Nilai Di Luar Range ({len(range_errors)}):")
    for path in range_errors:
        print(f"  - {path}")

if value_errors:
    print(f"\n[❌] Tidak Bisa Konversi Float ({len(value_errors)}):")
    for path in value_errors:
        print(f"  - {path}")

if not (missing_labels or empty_labels or format_errors or range_errors or value_errors):
    print("✅ Semua label valid!")