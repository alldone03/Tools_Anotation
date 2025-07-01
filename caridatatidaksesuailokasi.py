
import os
import shutil
from PIL import Image


folder_asal = r"C:\Users\Aldan\Desktop\ImproTYT\FORTUNER\CAMERA 5 FORTUNER.v3i.yolov8\dataset_filtered_cropped"
folder_output = r"C:\Users\Aldan\Desktop\ImproTYT\FORTUNER\CAMERA 5 FORTUNER.v3i.yolov8\dataset_filtered_cropped_dataset_kelas_tertentu"
area = (389, 197, 504, 151)

def bbox_di_area(x_center, y_center, w, h, x_min, x_max, y_min, y_max, img_w, img_h):
    xmin_bbox = (x_center - w / 2) * img_w
    xmax_bbox = (x_center + w / 2) * img_w
    ymin_bbox = (y_center - h / 2) * img_h
    ymax_bbox = (y_center + h / 2) * img_h

    # Cek apakah overlap dengan area
    return not (xmax_bbox < x_min or xmin_bbox > x_max or ymax_bbox < y_min or ymin_bbox > y_max)

def copy_kalau_15_16_tidak_di_area(folder_asal, folder_tujuan, area_pixel, kelas_target=[15, 16], ekstensi_gambar=".jpg"):
    os.makedirs(folder_tujuan, exist_ok=True)
    x_min = min(area_pixel[0], area_pixel[2])
    x_max = max(area_pixel[0], area_pixel[2])
    y_min = min(area_pixel[1], area_pixel[3])
    y_max = max(area_pixel[1], area_pixel[3])

    for file in os.listdir(folder_asal):
        if not file.endswith(".txt"):
            continue

        path_label = os.path.join(folder_asal, file)
        nama_dasar = os.path.splitext(file)[0]
        path_gambar = os.path.join(folder_asal, nama_dasar + ekstensi_gambar)

        if not os.path.exists(path_gambar):
            print(f"Gambar tidak ditemukan: {path_gambar}")
            continue

        with Image.open(path_gambar) as img:
            img_w, img_h = img.size

        with open(path_label, "r") as f:
            lines = f.readlines()

        # Ambil hanya bbox kelas 15 dan 16
        target_boxes = [
            list(map(float, line.strip().split()))
            for line in lines if line.strip() and int(line.strip().split()[0]) in kelas_target
        ]

        if not target_boxes:
            continue  # Tidak ada kelas 15 atau 16

        # Cek apakah semua bbox kelas target berada di luar area
        semua_di_luar = all(
            not bbox_di_area(x, y, w, h, x_min, x_max, y_min, y_max, img_w, img_h)
            for _, x, y, w, h in target_boxes
        )

        if semua_di_luar:
            shutil.copy(path_label, os.path.join(folder_tujuan, file))
            shutil.copy(path_gambar, os.path.join(folder_tujuan, nama_dasar + ekstensi_gambar))
            
copy_kalau_15_16_tidak_di_area(folder_asal, folder_output, area)