import cv2
import os

# --- Konfigurasi ---
input_folder = r"C:\Users\Aldan\Desktop\IMPROTOYOTA\Camera 1\Inn\AR"
output_folder = r"C:\Users\Aldan\Desktop\IMPROTOYOTA\Camera 1\Inn\AR_cropped"
scale_x, scale_y = 0, 0
# scale_x, scale_y = 1.5, 1.5
# crop_rel = (0.27, 0.20, 0.43, 0.47)  # x_rel, y_rel, w_rel, h_rel
# crop_rel = (0.21, 0.20, 0.52, 0.52)  # x_rel, y_rel, w_rel, h_rel crop_relative(img, 0.21, 0.20, 0.52, 0.52)
crop_rel = (0.21, 0.20, 0.6, 0.6)  # x_rel, y_rel, w_rel, h_rel crop_relative(img, 0.21, 0.20, 0.52, 0.52)

# crop_rel = (0.30, 0.27, 0.41, 0.41)  # x_rel, y_rel, w_rel, h_rel

os.makedirs(output_folder, exist_ok=True)

# --- Fungsi ---
def scale_image(img, scale_x, scale_y):
    w = int(img.shape[1] * scale_x)
    h = int(img.shape[0] * scale_y)
    return cv2.resize(img, (w, h))

def crop_relative(img, x_rel, y_rel, w_rel, h_rel):
    h, w = img.shape[:2]
    x = int(w * x_rel)
    y = int(h * y_rel)
    cw = int(w * w_rel)
    ch = int(h * h_rel)
    return img[y:y+ch, x:x+cw], x, y, cw, ch

def adjust_label(label_line, img_w, img_h, crop_x, crop_y, crop_w, crop_h):
    cls, x, y, w, h = map(float, label_line.strip().split())
    abs_x = x * img_w
    abs_y = y * img_h
    abs_w = w * img_w
    abs_h = h * img_h

    # Hitung posisi baru
    new_x = abs_x - crop_x
    new_y = abs_y - crop_y

    if new_x < 0 or new_y < 0 or new_x > crop_w or new_y > crop_h:
        return None  # Label keluar dari crop

    # Normalisasi ulang ke ukuran crop
    norm_x = new_x / crop_w
    norm_y = new_y / crop_h
    norm_w = abs_w / crop_w
    norm_h = abs_h / crop_h

    return f"{int(cls)} {norm_x:.6f} {norm_y:.6f} {norm_w:.6f} {norm_h:.6f}"

# --- Proses semua file ---
for file in os.listdir(input_folder):
    if file.endswith('.jpg') or file.endswith('.png'):
        img_path = os.path.join(input_folder, file)
        label_path = os.path.splitext(img_path)[0] + '.txt'

        image = cv2.imread(img_path)
        # cv2.imshow('Original Image', image)
        # cv2.waitKey(0)
        if scale_x == 0 or scale_y == 0:
            scaled = image.copy()
        else:
            scaled = scale_image(image, scale_x, scale_y)
        cropped, cx, cy, cw, ch = crop_relative(scaled, *crop_rel)

        # Simpan gambar hasil crop
        out_img_path = os.path.join(output_folder, file)
        cv2.imwrite(out_img_path, cropped)

        # Proses label jika ada
        if os.path.exists(label_path):
            with open(label_path, 'r') as f:
                lines = f.readlines()

            new_labels = []
            for line in lines:
                new_line = adjust_label(line, scaled.shape[1], scaled.shape[0], cx, cy, cw, ch)
                if new_line:
                    new_labels.append(new_line)

            # Simpan label baru
            out_label_path = os.path.splitext(out_img_path)[0] + '.txt'
            with open(out_label_path, 'w') as f:
                f.write('\n'.join(new_labels))