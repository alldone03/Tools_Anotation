from ultralytics import YOLO
import os
import csv
from collections import Counter

# Daftar model yang akan digunakan (ganti path sesuai milikmu)
model_paths = {
    "Innvova": r"C:\Users\Aldan\Desktop\ImproTYT\INNOVA\GoodDetection\train3\weights\best.pt",
    # "Fortuner": "runs/train/exp/weights/best.pt",
    # "Zenix": "runs/train/exp2/weights/best.pt"
}

# Load semua model
models = {name: YOLO(path, verbose=False) for name, path in model_paths.items()}

# Folder gambar
folder_input = r"E:\datacamera"
csv_output = r"E:\datacamera\Detection.csv"

# Siapkan CSV
header = ['Model', 'Path Gambar', 'Nama File', 'Jumlah Objek', 'Kelas Unik', 'Kelas Dominan', 'Label YOLO Format']

with open(csv_output, mode='w', newline='') as file_csv:
    writer = csv.writer(file_csv)
    writer.writerow(header)

    # Telusuri semua gambar
    for root, dirs, files in os.walk(folder_input):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                path_gambar = os.path.join(root, file)

                for model_name, model in models.items():
                    hasil = model(path_gambar)
                    boxes = hasil[0].boxes
                    jumlah_objek = len(boxes)

                    if jumlah_objek == 0:
                        kelas_unik = []
                        kelas_dominan = "-"
                        yolo_labels = []
                    else:
                        kelas = boxes.cls.tolist()
                        kelas_int = [int(k) for k in kelas]
                        kelas_unik = sorted(set(kelas_int))
                        kelas_dominan = Counter(kelas_int).most_common(1)[0][0]

                        xywhn = boxes.xywhn.tolist()
                        yolo_labels = [
                            f"{int(cls)} {round(x,6)} {round(y,6)} {round(w,6)} {round(h,6)}"
                            for cls, (x, y, w, h) in zip(kelas, xywhn)
                        ]

                    writer.writerow([
                        model_name,
                        path_gambar,
                        file,
                        jumlah_objek,
                        kelas_unik,
                        kelas_dominan,
                        yolo_labels
                    ])
                    file_csv.flush()

                    print(f"{file} - {model_name}: {jumlah_objek} objek, kelas {kelas_unik}")