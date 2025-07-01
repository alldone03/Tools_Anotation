import os
import shutil

# def resize_bbox(yolo_line, scale):
#     parts = yolo_line.strip().split()
#     if len(parts) != 5:
#         return None  # skip line jika tidak sesuai
#     cls, x, y, w, h = parts
#     x, y, w, h = float(x), float(y), float(w), float(h)

#     area = w * h
#     if area < 0.000941:
#         scale = 2.6
#     else:
#         scale = scale
#     # Perbesar ukuran width dan height
#     new_w = min(w * scale, 1.0)
#     new_h = min(h * scale, 1.0)

#     # Pastikan tetap dalam batas gambar
#     new_x = max(min(x, 1.0), 0.0)
#     new_y = max(min(y, 1.0), 0.0)
#     print(f"[Class {cls}] Luas bbox setelah diperbesar: {area:.6f} (normalized)")


#     return f"{cls} {new_x:.6f} {new_y:.6f} {new_w:.6f} {new_h:.6f}\n"
def resize_bbox(yolo_line, scale):
    parts = yolo_line.strip().split()
    if len(parts) != 5:
        return None

    cls, x, y, w, h = parts
    x, y, w, h = float(x), float(y), float(w), float(h)

    min_norm = 15 / 640  # normalisasi untuk 15 pixel

    # Jika terlalu kecil, perbesar ke minimal
    if w * 640 < 15:
        w = min_norm
    if h * 640 < 15:
        h = min_norm

    # Pastikan tetap di range 0-1
    w = min(w, 1.0)
    h = min(h, 1.0)
    x = max(min(x, 1.0), 0.0)
    y = max(min(y, 1.0), 0.0)

    print(f"[Class {cls}] W*640: {w*640:.1f}, H*640: {h*640:.1f}")

    return f"{cls} {x:.6f} {y:.6f} {w:.6f} {h:.6f}\n"

def process_folder(label_folder, image_folder, scale):
    output_label_folder = label_folder.rstrip("/") + f"_rescaled_{scale}"
    output_image_folder = image_folder.rstrip("/") + f"_rescaled_{scale}"
    os.makedirs(output_label_folder, exist_ok=True)
    os.makedirs(output_image_folder, exist_ok=True)

    for file_name in os.listdir(label_folder):
        if file_name.endswith(".txt") and file_name != "labels.txt":
            input_path = os.path.join(label_folder, file_name)
            output_path = os.path.join(output_label_folder, file_name)

            with open(input_path, "r") as infile, open(output_path, "w") as outfile:
                for line in infile:
                    new_line = resize_bbox(line, scale)
                    if new_line:
                        outfile.write(new_line)

            # Copy gambar
            base_name = os.path.splitext(file_name)[0]
            for ext in [".jpg", ".jpeg", ".png"]:
                image_path = os.path.join(image_folder, base_name + ext)
                if os.path.exists(image_path):
                    shutil.copy(image_path, os.path.join(output_image_folder, base_name + ext))
                    break

    # Copy labels.txt
    labels_file = os.path.join(label_folder, "labels.txt")
    if os.path.exists(labels_file):
        shutil.copy(labels_file, os.path.join(output_label_folder, "labels.txt"))
        print("File labels.txt juga telah disalin.")

    print("\n✅ Selesai! Semua label, gambar, dan labels.txt telah diproses.")


# Contoh pemakaian
folder_label = r"C:\Users\Aldan\Desktop\ImproTYT\INNOVA\dataset_cropped"  # ganti dengan folder kamu

scale_factor = 1.5       # perbesar 1.5 kali
process_folder(folder_label,folder_label, scale_factor)