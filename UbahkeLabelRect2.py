import os

def convert_polygon_to_bbox(points):
    x_coords = points[::2]
    y_coords = points[1::2]

    x_min = min(x_coords)
    x_max = max(x_coords)
    y_min = min(y_coords)
    y_max = max(y_coords)

    x_center = (x_min + x_max) / 2
    y_center = (y_min + y_max) / 2
    width = x_max - x_min
    height = y_max - y_min

    return x_center, y_center, width, height

def convert_labels_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt") and filename != "labels.txt":
            filepath = os.path.join(folder_path, filename)
            print(f"[📂] Memproses file: {filepath}")
            new_lines = []

            with open(filepath, "r") as file:
                lines = file.readlines()

            for line in lines:
                parts = list(map(float, line.strip().split()))
                class_id = int(parts[0])
                if len(parts) == 5:
                    new_lines.append(line.strip())
                else:
                    x_center, y_center, width, height = convert_polygon_to_bbox(parts[1:])
                    new_line = f"{class_id} {x_center} {y_center} {width} {height}"
                    new_lines.append(new_line)

            with open(filepath, "w") as file:
                for line in new_lines:
                    file.write(line + "\n")

# Ganti path ke folder label kamu
folder_path = 'C:/Users/Aldan/Desktop/IMPROTOYOTA/CAMERA 8 FORTUNER.v1i.yolov8/dataset/images'
convert_labels_in_folder(folder_path)