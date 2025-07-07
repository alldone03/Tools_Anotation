import os
import matplotlib.pyplot as plt
from collections import Counter
import time

# Mulai stopwatch
start_time = time.time()

# Path ke folder dataset dan labels.txt
folder_path = r"C:\Users\Aldan\Desktop\ImproTYT\ZENIX\CAMERA 5 ZENIX.v4i.yolov8\dataset_filtered_cropped_rescaled_1.5"  # ganti sesuai lokasi folder kamu

labels_txt_path = os.path.join(folder_path, 'labels.txt')

# Baca nama label
with open(labels_txt_path, 'r') as f:
    label_names = [line.strip() for line in f.readlines()]

# Hitung class_id dari file label
label_counter = Counter()
for filename in os.listdir(folder_path):
    if filename.endswith(".txt") and filename != 'labels.txt':
        with open(os.path.join(folder_path, filename), 'r') as f:
            for line in f:
                if line.strip():
                    class_id = int(line.strip().split()[0])
                    label_counter[class_id] += 1

# Hitung waktu proses
elapsed_time = time.time() - start_time
print(f"Waktu proses: {elapsed_time:.2f} detik")

labels = [label_names[i] for i in label_counter.keys()]
counts = list(label_counter.values())

# Plot
plt.figure(figsize=(10, 6))
bars = plt.bar(labels, counts)

# Warna bar
colors = plt.cm.tab20.colors
for i, bar in enumerate(bars):
    bar.set_color(colors[i % len(colors)])

# Menampilkan jumlah data di atas bar
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 5, int(yval), ha='center', va='bottom') # +5 for a little space above the bar

plt.xticks(rotation=90)
plt.ylabel("Instances")
plt.title("Jumlah Tiap Label (YOLO Format)")
plt.tight_layout()
plt.show()
# plt.savefig('yolo_label_counts_bar.png')