import os

# Ganti dengan path ke folder label kamu
FOLDER_LABEL = r"C:\Users\Aldan\Desktop\ImproTYT\FORTUNER\CAMERA 5 FORTUNER.v3i.yolov8\dataset_filtered_cropped_rescaled_1.5"


# Ambil semua file .txt di folder
for file in sorted(os.listdir(FOLDER_LABEL)):
    if file.endswith(".txt"):
        file_path = os.path.join(FOLDER_LABEL, file)

        with open(file_path, 'r') as f:
            lines = f.readlines()
            jumlah_bbox = len(lines)
            

        print(f"{file}: {jumlah_bbox} bounding box")