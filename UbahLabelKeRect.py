import os

def segmentation_to_bbox(label_path):
    with open(label_path, 'r') as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        parts = list(map(float, line.strip().split()))
        class_id = int(parts[0])
        coords = parts[1:]

        xs = coords[0::2]
        ys = coords[1::2]

        xmin, xmax = min(xs), max(xs)
        ymin, ymax = min(ys), max(ys)

        # Konversi ke format YOLO: center_x, center_y, width, height
        x_center = (xmin + xmax) / 2
        y_center = (ymin + ymax) / 2
        width = xmax - xmin
        height = ymax - ymin

        new_line = f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}"
        new_lines.append(new_line)
        print(new_line)

    with open(label_path, 'w') as f:
        f.write('\n'.join(new_lines))


# Path folder labels
label_folder = 'C:/Users/Aldan/Desktop/CAMERA 6 ZENIX.v1i.yolov8/dataset/images'  # Ubah ke path folder label kamu

print(f"[📂] Memproses label di folder: {label_folder}")
for filename in os.listdir(label_folder):
    if filename.endswith('.txt'):
        path = os.path.join(label_folder, filename)
        segmentation_to_bbox(path)
        print(f"[✅] Converted: {filename}")

print("\n[✔️] Semua file label berhasil dikonversi dari segmentation ke rectangle (bounding box)")