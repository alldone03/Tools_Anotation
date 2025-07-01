from ultralytics import YOLO
import os
import shutil

# Inisialisasi model (ganti dengan model kamu kalau custom)
model = YOLO("C:/Users/Aldan/Desktop/ImproTYT/INNOVA/train3/train3/weights/best.pt")  # atau "runs/train/exp/weights/best.pt"

# Folder input dan output
folder_input = r"E:\datacamera"
folder_output = r"C:\Users\Aldan\Desktop\ImproTYT\INNOVA\newDataset"

# Bikin folder output jika belum ada
os.makedirs(folder_output, exist_ok=True)


for root, dirs, files in os.walk(folder_input):
    for file in files:
        if file.lower().endswith(('.jpg', '.jpeg', '.png')):
            full_path = os.path.join(root, file)

            # Ambil nama folder (sebagai tanggal)
            folder_tanggal = os.path.basename(root)  # contoh: "2025-06-18_15-59-29"

            # Deteksi objek
            hasil = model(full_path)
            jumlah_objek = len(hasil[0].boxes)

            if jumlah_objek > 20:
                # Buat nama file baru
                nama_baru = f"{folder_tanggal}_{file}"
                tujuan = os.path.join(folder_output, nama_baru)
                
                # Salin dengan nama baru
                shutil.copy(full_path, tujuan)
                print(f"Disalin sebagai: {nama_baru} ({jumlah_objek} objek)")
