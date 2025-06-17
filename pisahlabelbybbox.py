import os
import shutil

# Folder gabungan gambar dan label
FOLDER_LABEL = r"C:\Users\Aldan\Desktop\ImproTYT\ZENIX\CAMERA 5 ZENIX.v4i.yolov8\dataset\images"
OUTPUT_FOLDER = r"C:\Users\Aldan\Desktop\ImproTYT\ZENIX\CAMERA 5 ZENIX.v4i.yolov8\dataset_filtered"

# Bikin folder output kalau belum ada
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

for file in sorted(os.listdir(FOLDER_LABEL)):
    if file.endswith(".txt"):
        file_path = os.path.join(FOLDER_LABEL, file)

        with open(file_path, 'r') as f:
            lines = f.readlines()
            jumlah_bbox = len(lines)


            print(f"{file}: {jumlah_bbox} bounding box")
            if jumlah_bbox >= 15:
                # Pindah file label
                dst_label = os.path.join(OUTPUT_FOLDER, file)
                shutil.copy(file_path, dst_label)

                # Pindah file gambar (nama sama dengan label)
                base_name = os.path.splitext(file)[0]
                found = False
                for ext in ['.jpg', '.png', '.jpeg']:
                    image_file = os.path.join(FOLDER_LABEL, base_name + ext)
                    if os.path.exists(image_file):
                        dst_img = os.path.join(OUTPUT_FOLDER, base_name + ext)
                        shutil.copy(image_file, dst_img)
                        found = True
                        print(f"[✅] {base_name + ext} dan {file} Copy ke {OUTPUT_FOLDER}")
                        break
                if not found:
                    print(f"[⚠️] Gambar untuk {file} tidak ditemukan.")