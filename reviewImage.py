import os
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import glob
import csv
from collections import Counter

# ======== KONFIGURASI =========
# image_folder = r"C:\Users\Aldan\Desktop\ImproTYT\AfterDetect\Innova"  # GANTI path ke folder kamu
image_folder = r"C:\Users\Aldan\Desktop\ImproTYT\INNOVA\dataset_cropped_rescaled_1.5"  # GANTI path ke folder kamu
csv_filename = "hasil_review.csv"

# ======== BACA CLASS NAME DARI labels.txt =========
labels_path = os.path.join(image_folder, "labels.txt")
class_names = []

with open(labels_path, "r") as f:
    for line in f:
        print(line)
      
        class_names.append(line.strip())

# Ambil semua gambar JPG
image_files = sorted(glob.glob(f"{image_folder}/*.jpg"))
current_image_index = 0
current_boxes = []
highlight_index = -1

color_map = [
    "red", "orange", "yellow", "lime", "cyan", "deepskyblue",
    "magenta", "violet", "gold", "hotpink", "turquoise",
    "lawngreen", "dodgerblue", "salmon", "aqua"
]
def get_class_color(class_id):
    return color_map[class_id % len(color_map)]

# Buat file CSV jika belum ada
if not os.path.exists(csv_filename):
    with open(csv_filename, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "decision",'Model', 'Path Gambar', 'Nama File', 'Jumlah Objek', 'Kelas Unik', 'Kelas Dominan', 'Label YOLO Format'
        ])

# ========== FUNGSI GUI ==========
def read_yolo_labels(label_path, img_width, img_height):
    boxes = []
    if not os.path.exists(label_path):
        return boxes
    with open(label_path, "r") as f:
        for line in f:
            parts = line.strip().split()
            class_id = int(parts[0])
            x_center = float(parts[1]) * img_width
            y_center = float(parts[2]) * img_height
            w = float(parts[3]) * img_width
            h = float(parts[4]) * img_height
            x1 = int(x_center - w / 2)
            y1 = int(y_center - h / 2)
            x2 = int(x_center + w / 2)
            y2 = int(y_center + h / 2)
            boxes.append((x1, y1, x2, y2, class_id))
    return boxes

def resize_and_render():
    global tk_image, original_image
    if original_image is None:
        return

    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    img = original_image.copy().resize((canvas_width, canvas_height))
    draw = ImageDraw.Draw(img)

    label_path = image_files[current_image_index].replace(".jpg", ".txt")
    current_boxes.clear()
    boxes = read_yolo_labels(label_path, canvas_width, canvas_height)
    listbox.delete(0, tk.END)

    for idx, (x1, y1, x2, y2, class_id) in enumerate(boxes):
        color = get_class_color(class_id)
        border = 4 if idx == highlight_index else 2
        draw.rectangle([x1, y1, x2, y2], outline=color, width=border)

        label = class_names[class_id] if class_id < len(class_names) else f"Class {class_id}"
        draw.text((x1, y1 - 10), f"{idx}: {label}", fill=color)

        listbox.insert(tk.END, f"{idx}: {label}")
        listbox.itemconfig(idx, foreground=color)
        current_boxes.append((x1, y1, x2, y2, class_id))

    tk_image = ImageTk.PhotoImage(img)
    canvas.delete("all")
    canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)


original_image = None
def draw_boxes(image_path):
    global current_boxes, tk_image, highlight_index, original_image
    original_image = Image.open(image_path).convert("RGB")
    resize_and_render()


def on_select(event):
    global highlight_index
    selection = listbox.curselection()
    if selection:
        highlight_index = selection[0]
        draw_boxes(image_files[current_image_index])

def save_decision(decision):
    img_path = image_files[current_image_index]
    label_path = img_path.replace(".jpg", ".txt")
    label_lines = []
    class_ids = []

    if os.path.exists(label_path):
        with open(label_path, "r") as f:
            label_lines = [line.strip() for line in f.readlines()]
            class_ids = [int(line.split()[0]) for line in label_lines if line.strip()]

    jumlah_objek = len(label_lines)
    kelas_unik = list(sorted(set(class_ids)))
    kelas_dominan = Counter(class_ids).most_common(1)[0][0] if class_ids else "-"
    
    nama_file = os.path.basename(img_path)
    folder_name = os.path.basename(os.path.dirname(img_path))  # Ambil parent folder

    with open(csv_filename, "a", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            str(decision),
            "Model",
            img_path,
            nama_file,
            jumlah_objek,
            str(kelas_unik),
            kelas_dominan,
            str(label_lines)
        ])

    next_image()

def next_image():
    global current_image_index, highlight_index
    if current_image_index < len(image_files) - 1:
        current_image_index += 1
        highlight_index = -1
        draw_boxes(image_files[current_image_index])

def prev_image():
    global current_image_index, highlight_index
    if current_image_index > 0:
        current_image_index -= 1
        highlight_index = -1
        draw_boxes(image_files[current_image_index])

# ========== GUI ==========

window = tk.Tk()
window.geometry("950x550")

frame_image = tk.Frame(window)
frame_image.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

canvas = tk.Canvas(frame_image, bg="black")
canvas.pack(fill=tk.BOTH, expand=True)

frame_right = tk.Frame(window, width=300)
frame_right.pack(side=tk.RIGHT, fill=tk.Y)

listbox = tk.Listbox(frame_right, width=100)
listbox.pack(pady=5)

listbox.bind("<<ListboxSelect>>", on_select)

frame_btn = tk.Frame(frame_right)
frame_btn.pack(pady=5)

tk.Button(frame_btn, text="⏪ Prev", width=10, command=prev_image).grid(row=0, column=0, padx=2)
tk.Button(frame_btn, text="Next ⏩", width=10, command=next_image).grid(row=0, column=1, padx=2)

tk.Button(frame_right, text="✅ Benar", bg="green", fg="white", width=25, command=lambda: save_decision("benar")).pack(pady=5)
tk.Button(frame_right, text="❌ Salah", bg="red", fg="white", width=25, command=lambda: save_decision("salah")).pack(pady=5)
tk.Button(frame_right, text="✔️ Orang", bg="blue", fg="white", width=25,
          command=lambda: save_decision("orang")).pack(pady=5)

draw_boxes(image_files[current_image_index])

window.bind("<Right>", lambda e: next_image())
window.bind("<Left>", lambda e: prev_image())
window.bind("b", lambda e: save_decision("benar"))
window.bind("s", lambda e: save_decision("salah"))
window.bind("o", lambda e: save_decision("orang"))
canvas.bind("<Configure>", lambda event: resize_and_render())


window.mainloop()