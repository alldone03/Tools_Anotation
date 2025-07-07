import os
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import glob
import csv
from collections import Counter

manual_boxes = []  # tiap item: (x1, y1, x2, y2, class_id)
data_review = []  # List of dict, satu dict untuk satu gambar
annotation_data = {}  # key: nama_file, value: list of manual boxes
start_x, start_y = 0, 0
selected_manual_index = -1  # untuk menandai kotak manual yang dipilih

# ======== KONFIGURASI =========
# image_folder = r"C:\Users\Aldan\Desktop\ImproTYT\AfterDetect\Innova"  # GANTI path ke folder kamu
image_folder = r"C:\Users\Aldan\Desktop\ImproTYT\Review03072025\Zenix"  # GANTI path ke folder kamu
csv_filename = "DatasetOK02072025_review_Zenix.csv"

image_files = sorted(glob.glob(os.path.join(image_folder, "**", "*.jpg"), recursive=True))
# img_path = image_files[current_image_index]
# label_path = img_path.replace(".jpg", ".txt")
for img in image_files:
    label_txt = img.replace(".jpg", ".txt")
    if not os.path.exists(label_txt):
        print(f"[WARNING] Tidak ditemukan label untuk: {img}")


# ======== BACA CLASS NAME DARI labels.txt =========
labels_path = os.path.join(image_folder, "labels.txt")

# class_names = []
# Step 1: load semua image
image_files = sorted(glob.glob(os.path.join(image_folder, "**", "*.jpg"), recursive=True))

# Step 2: load class names
labels_path = os.path.join(image_folder, "labels.txt")
class_names = []
with open(labels_path, "r") as f:
    class_names = [line.strip() for line in f]

# Step 3: jika CSV tidak ada, buat dan isi dari image & label
if not os.path.exists(csv_filename):
    with open(csv_filename, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["decision", "Model", "Path Gambar", "Nama File", "Jumlah Objek", "Kelas Unik", "Kelas Dominan", "Label YOLO Format"])
        for img_path in image_files:
            label_path = img_path.replace(".jpg", ".txt")
            label_lines = []
            class_ids = []
            if os.path.exists(label_path):
                with open(label_path, "r") as f_label:
                    label_lines = [line.strip() for line in f_label.readlines()]
                    class_ids = [int(line.split()[0]) for line in label_lines if line.strip()]
            jumlah_objek = len(label_lines)
            kelas_unik = sorted(set(class_ids))
            kelas_dominan = Counter(class_ids).most_common(1)[0][0] if class_ids else "-"
            nama_file = os.path.basename(img_path)

            writer.writerow([
                "",  # decision kosong dulu
                "Model",
                img_path,
                nama_file,
                jumlah_objek,
                str(kelas_unik),
                kelas_dominan,
                str(label_lines)
            ])


data_review = []
with open(csv_filename, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
    # Pastikan semua field diisi dengan kunci yang benar
        try:
            data_review.append({
                "decision": row.get("decision", ""),
                "Model": row.get("Model", "Model"),
                "Path Gambar": row["Path Gambar"],
                "Nama File": row["Nama File"],
                "jumlah_objek": int(row.get("Jumlah Objek", 0)),
                "kelas_unik": eval(row.get("Kelas Unik", "[]")),
                "kelas_dominan": row.get("Kelas Dominan", "-"),
                "label_format": eval(row.get("Label YOLO Format", "[]"))
            })
        except Exception as e:
            print(f"[ERROR load row]: {row} -> {e}")


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
    global img_scale_x, img_scale_y
    img_scale_x = original_image.width / canvas_width
    img_scale_y = original_image.height / canvas_height

    img = original_image.copy().resize((canvas_width, canvas_height))
    draw = ImageDraw.Draw(img)

    label_path = image_files[current_image_index].replace(".jpg", ".txt")
    current_boxes.clear()
    boxes = read_yolo_labels(label_path, canvas_width, canvas_height)
    listbox.delete(0, tk.END)
    
    for idx, (x1, y1, x2, y2, class_id) in enumerate(manual_boxes):
        color = get_class_color(class_id)
        label = class_names[class_id] if class_id < len(class_names) else f"Class {class_id}"
        border = 6 if idx == selected_manual_index else 3
        draw.rectangle([x1, y1, x2, y2], outline=color, width=border)
        draw.text((x1, y1 - 10), f"{label} (Tambahan)", fill=color)

    for idx, (x1, y1, x2, y2, class_id) in enumerate(boxes):
        
        color = get_class_color(class_id)
        border = 4 if idx == highlight_index else 2
        draw.rectangle([x1, y1, x2, y2], outline=color, width=border)

        label = class_names[class_id] if class_id < len(class_names) else f"Class {class_id}"
        draw.text((x1, y1 - 10), f"{label}", fill=color)

        listbox.insert(tk.END, f"{label}")
        listbox.itemconfig(idx, foreground=color)
        current_boxes.append((x1, y1, x2, y2, class_id))

    tk_image = ImageTk.PhotoImage(img)
    canvas.delete("all")
    canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)


original_image = None
def draw_boxes(image_path):
    global current_boxes, tk_image, highlight_index, original_image, manual_boxes

    manual_boxes.clear()
    original_image = Image.open(image_path).convert("RGB")

    # Ambil nama file sebagai key
    nama_file = os.path.basename(image_path)
    if nama_file in annotation_data:
        manual_boxes.extend(annotation_data[nama_file])  # ambil data yang sudah pernah disimpan

    resize_and_render()


def on_select(event):
    global highlight_index
    selection = listbox.curselection()
    if selection:
        highlight_index = selection[0]
        draw_boxes(image_files[current_image_index])

def update_decision_and_label(decision):
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
    
    record = {
    "decision": decision,
    "model": "Model",
    "path": img_path,
    "nama_file": nama_file,
    "jumlah_objek": jumlah_objek + len(manual_boxes),
    "kelas_unik": sorted(set(class_ids + [box[4] for box in manual_boxes])),
    "kelas_dominan": Counter(class_ids + [box[4] for box in manual_boxes]).most_common(1)[0][0] if (class_ids or manual_boxes) else "-",
    "label_format": label_lines + [
        f"{box[4]} {((box[0]+box[2])/2)/canvas.winfo_width():.6f} {((box[1]+box[3])/2)/canvas.winfo_height():.6f} {(abs(box[2]-box[0])/canvas.winfo_width()):.6f} {(abs(box[3]-box[1])/canvas.winfo_height()):.6f}"
        for box in manual_boxes
    ]
}
    data_review.append(record)


    with open(csv_filename, "a", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        combined_labels = label_lines + [
            f"{box[4]} {((box[0]+box[2])/2)/canvas.winfo_width():.6f} {((box[1]+box[3])/2)/canvas.winfo_height():.6f} {(abs(box[2]-box[0])/canvas.winfo_width()):.6f} {(abs(box[3]-box[1])/canvas.winfo_height()):.6f}"
            for box in manual_boxes
        ]

        writer.writerow([
            str(decision),
            "Model",
            img_path,
            nama_file,
            jumlah_objek + len(manual_boxes),  # tambahkan total objek manual juga
            str(sorted(set(class_ids + [box[4] for box in manual_boxes]))),
            Counter(class_ids + [box[4] for box in manual_boxes]).most_common(1)[0][0] if (class_ids or manual_boxes) else "-",
            str(combined_labels)  # ✅ Ini sudah termasuk kotak manual
        ])
        

    next_image()

def next_image():
    global current_image_index, highlight_index
    if current_image_index < len(image_files) - 1:
        current_image_index += 1
        highlight_index = -1
        draw_boxes(image_files[current_image_index])
        current_filename = os.path.basename(image_files[current_image_index])
        annotation_data[current_filename] = list(manual_boxes)

def prev_image():
    global current_image_index, highlight_index
    if current_image_index > 0:
        current_image_index -= 1
        highlight_index = -1
        draw_boxes(image_files[current_image_index])
        current_filename = os.path.basename(image_files[current_image_index])
        annotation_data[current_filename] = list(manual_boxes)
        
def on_mouse_down(event):
    # Tidak perlu scaling lagi, langsung ambil dari canvas
    print("click")
    x_center = event.x
    y_center = event.y
    box_size = 2  # 2x2 pixel

    x1 = x_center - box_size // 2
    y1 = y_center - box_size // 2
    x2 = x_center + box_size // 2
    y2 = y_center + box_size // 2

    choose_class_for_box(x1, y1, x2, y2)

def on_mouse_up(event):
    pass  # tidak perlu lagi

def choose_class_for_box(x1, y1, x2, y2):
    popup = tk.Toplevel(window)
    popup.update_idletasks()
    popup_width = popup.winfo_reqwidth()
    popup_height = popup.winfo_reqheight()

    screen_width = popup.winfo_screenwidth()
    screen_height = popup.winfo_screenheight()

    x = (screen_width // 2) - (popup_width // 2)
    y = (screen_height // 2) - (popup_height // 2)
    popup.geometry(f"+{x}+{y}")

    popup.title("Pilih Label Kelas")

    tk.Label(popup, text="Pilih label untuk kotak tambahan:").pack()

    selected = tk.StringVar(popup)
    selected.set(class_names[0])  # default

    option = tk.OptionMenu(popup, selected, *class_names)
    option.pack(pady=5)

    def submit():
        class_id = class_names.index(selected.get())
        manual_boxes.append((x1, y1, x2, y2, class_id))
        # Simpan decision "salah" langsung
        update_decision_and_label("salah")
        popup.destroy()

    tk.Button(popup, text="OK", command=submit).pack(pady=5)

def export_csv():
    if not data_review:
        print("Tidak ada data untuk diekspor.")
        return
    with open(csv_filename, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "decision", "Model", "Path Gambar", "Nama File", "Jumlah Objek", "Kelas Unik", "Kelas Dominan", "Label YOLO Format"
        ])
        for row in data_review:
            writer.writerow([
                row["decision"],
                row["model"],
                row["path"],
                row["nama_file"],
                row["jumlah_objek"],
                str(row["kelas_unik"]),
                row["kelas_dominan"],
                str(row["label_format"])
            ])
    print("Export CSV selesai!")
    
def on_canvas_click(event):
    global selected_manual_index
    x, y = event.x, event.y
    selected_manual_index = -1
    for idx, (x1, y1, x2, y2, _) in enumerate(manual_boxes):
        if x1 <= x <= x2 and y1 <= y <= y2:
            selected_manual_index = idx
            break
    resize_and_render()
    

def update_image_path_label():
    import os
    short_path = os.path.relpath(image_files[current_image_index], image_folder)
    label_path.config(text=f"Path: {short_path}")

def update_decision_and_label(decision):
    global data_review

    current_data = data_review[current_image_index]
    current_data["decision"] = decision
    current_data["jumlah_objek"] = len(current_data["label_format"]) + len(manual_boxes)
    current_data["kelas_unik"] = sorted(set([int(line.split()[0]) for line in current_data["label_format"]] + [box[4] for box in manual_boxes]))
    current_data["kelas_dominan"] = Counter([int(line.split()[0]) for line in current_data["label_format"]] + [box[4] for box in manual_boxes]).most_common(1)[0][0] if (current_data["label_format"] or manual_boxes) else "-"
    
    # gabungkan semua label
    combined_labels = current_data["label_format"] + [
        f"{box[4]} {((box[0]+box[2])/2)/canvas.winfo_width():.6f} {((box[1]+box[3])/2)/canvas.winfo_height():.6f} {(abs(box[2]-box[0])/canvas.winfo_width()):.6f} {(abs(box[3]-box[1])/canvas.winfo_height()):.6f}"
        for box in manual_boxes
    ]
    current_data["label_format"] = combined_labels

    # tulis ulang semua data_review ke csv
    with open(csv_filename, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["decision", "Model", "Path Gambar", "Nama File", "Jumlah Objek", "Kelas Unik", "Kelas Dominan", "Label YOLO Format"])
        for row in data_review:
            writer.writerow([
                row["decision"],
                row["Model"],
                row["Path Gambar"],
                row["Nama File"],
                row["jumlah_objek"],
                str(row["kelas_unik"]),
                row["kelas_dominan"],
                str(row["label_format"])
            ])




# ========== GUI ==========

window = tk.Tk()
window.geometry("950x550")

frame_image = tk.Frame(window)
frame_image.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

canvas = tk.Canvas(frame_image, bg="black")
canvas.pack(fill=tk.BOTH, expand=True)

canvas.bind("<ButtonPress-1>", on_mouse_down)
canvas.bind("<ButtonRelease-1>", on_mouse_up)


frame_right = tk.Frame(window, width=300)
frame_right.pack(side=tk.RIGHT, fill=tk.Y)

listbox = tk.Listbox(frame_right, width=100)
listbox.pack(pady=5)

listbox.bind("<<ListboxSelect>>", on_select)

frame_btn = tk.Frame(frame_right)
frame_btn.pack(pady=5)

label_path = tk.Label(frame_right, text="Path: ", wraplength=280, justify="left")
label_path.pack(pady=5)

tk.Button(frame_btn, text="⏪ Prev", width=10, command=prev_image).grid(row=0, column=0, padx=2)
tk.Button(frame_btn, text="Next ⏩", width=10, command=next_image).grid(row=0, column=1, padx=2)

tk.Button(frame_right, text="✅ Benar", bg="green", fg="white", width=25, command=lambda: update_decision_and_label("benar")).pack(pady=5)
tk.Button(frame_right, text="❌ Salah", bg="red", fg="white", width=25, command=lambda: update_decision_and_label("salah")).pack(pady=5)
tk.Button(frame_right, text="✔️ Orang", bg="blue", fg="white", width=25,
          command=lambda: update_decision_and_label("orang")).pack(pady=5)
tk.Button(frame_right, text="📤 Export CSV", bg="purple", fg="white", width=25,
          command=lambda: export_csv()).pack(pady=5)


draw_boxes(image_files[current_image_index])

resize_and_render()
update_image_path_label()  # ⬅ Tambah baris ini

window.bind("<Right>", lambda e: next_image())
window.bind("<Left>", lambda e: prev_image())
window.bind("b", lambda e: update_decision_and_label("benar"))
window.bind("s", lambda e: update_decision_and_label("salah"))
window.bind("o", lambda e: update_decision_and_label("orang"))
canvas.bind("<Configure>", lambda event: resize_and_render())



window.mainloop()