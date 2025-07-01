import os
import shutil
from PIL import Image


asal = r"C:\Users\Aldan\Desktop\ImproTYT\FORTUNER\CAMERA 5 FORTUNER.v3i.yolov8\dataset_filtered_cropped"
tujuan = r"C:\Users\Aldan\Desktop\ImproTYT\FORTUNER\CAMERA 5 FORTUNER.v3i.yolov8\dataset_filtered_cropped\dataset_tanpa_bbox_area_ini"

area = (582, 558, 685, 477)

def bbox_overlap_area(x_center, y_center, w, h, x_min, x_max, y_min, y_max, img_w, img_h):
    xmin_bbox = (x_center - w / 2) * img_w
    xmax_bbox = (x_center + w / 2) * img_w
    ymin_bbox = (y_center - h / 2) * img_h
    ymax_bbox = (y_center + h / 2) * img_h

    return not (xmax_bbox < x_min or xmin_bbox > x_max or ymax_bbox < y_min or ymin_bbox > y_max)

def copy_label_tidak_di_area(folder_asal, folder_tujuan, area_pixel, ekstensi_gambar=".jpg"):
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

        with open(path_label, 'r') as f:
            lines = f.readlines()

        ada_bbox_di_area = False
        for line in lines:
            parts = line.strip().split()
            if len(parts) != 5:
                continue
            _, x, y, w, h = map(float, parts)
            if bbox_overlap_area(x, y, w, h, x_min, x_max, y_min, y_max, img_w, img_h):
                ada_bbox_di_area = True
                break

        if not ada_bbox_di_area:
            shutil.copy(path_label, os.path.join(folder_tujuan, file))
            shutil.copy(path_gambar, os.path.join(folder_tujuan, nama_dasar + ekstensi_gambar))



copy_label_tidak_di_area(asal, tujuan, area)

