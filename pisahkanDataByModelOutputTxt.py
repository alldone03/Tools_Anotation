from ultralytics import YOLO
import os
import csv
from collections import Counter

# Daftar model yang akan digunakan (ganti path sesuai milikmu)
model_paths = {
    # "Fortuner": r"D:\TMMINImpro\ImproTYT\ModelOK\ModelCam9\Fortuner\weights\best.pt",
    # "Innova": r"D:\TMMINImpro\ImproTYT\ModelOK\ModelCam9\Innova\weights\best.pt",
    # "Zenix": r"D:\TMMINImpro\ImproTYT\ModelOK\ModelCam9\Zenix\weights\best.pt"
    # "Fortuner": r"D:\TMMINImpro\ImproTYT\ModelOK\ModelCam6\Fortuner\weights\best.pt",
    # "Innova": r"D:\TMMINImpro\ImproTYT\ModelOK\ModelCam6\Innova\weights\best.pt",
    # "Zenix": r"D:\TMMINImpro\ImproTYT\ModelOK\ModelCam6\Zenix\weights\best.pt"
    "Fortuner": r"D:\TMMINImpro\ImproTYT\ModelCam8\Fortuner\weights\best.pt",
    "Innova": r"D:\TMMINImpro\ImproTYT\ModelCam8\Innova\weights\best.pt",
    "Zenix": r"D:\TMMINImpro\ImproTYT\ModelCam8\Zenix\weights\best.pt"
}

# Load semua model
models = {name: YOLO(path, verbose=True) for name, path in model_paths.items()}

# Folder gambar
folder_input = r"D:\TMMINImpro\newdata16"
csv_output = folder_input+r"\Detection_camera_8.csv"

# Simpan label dari tiap model ke file
for name, model in models.items():
    class_names = model.names  # dict {0: 'car', 1: 'bus', ...}
    label_file = f"labels_{name}.txt"
    with open(f'{folder_input}\{label_file}', "w") as f:
        for i in range(len(class_names)):
            f.write(f"{class_names[i]}\n")
    print(f"Label dari model '{name}' disimpan ke: {label_file}")


# Siapkan CSV
header = ['Model', 'Path Gambar', 'Nama File', 'Jumlah Objek', 'Kelas Unik', 'Kelas Dominan', 'Label YOLO Format']

with open(csv_output, mode='w', newline='') as file_csv:
    writer = csv.writer(file_csv)
    writer.writerow(header)

    # Telusuri semua gambar
    for root, dirs, files in os.walk(folder_input):
        for file in files:
            if file.lower().endswith(('camera_4.jpg', '.jpeg', '.png')):
                path_gambar = os.path.join(root, file)

                for model_name, model in models.items():
                    hasil = model(path_gambar,conf=0.6,verbose=False)
                    boxes = hasil[0].boxes
                    jumlah_objek = len(boxes)
                    

                    if jumlah_objek == 0:
                        continue
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

                    print(f"{path_gambar} - {model_name}: {jumlah_objek} objek")