import subprocess

# Contoh 3 kali jalanin dengan argumen berbeda
commands = [
    ["python", "DataAugmentation.py", "--folderimage", "E:/DatasetUBC/CAMERA 6 FORTUNER.v2i.yolov8/dataset/images"],
    ["python", "DataAugmentation.py", "--folderimage", "E:/DatasetUBC/CAMERA 6 INNOVA.v1i.yolov8/dataset/images"],
    ["python", "DataAugmentation.py", "--folderimage", "E:/DatasetUBC/CAMERA 6 ZENIX.v1i.yolov8/dataset/images"],
    ["python", "DataAugmentation.py", "--folderimage", "E:/DatasetUBC/CAMERA 8 FORTUNER.v1i.yolov8/dataset/images"],
    ["python", "DataAugmentation.py", "--folderimage", "E:/DatasetUBC/CAMERA 8 INNOVA.v1i.yolov8/dataset/images"],
    ["python", "DataAugmentation.py", "--folderimage", "E:/DatasetUBC/CAMERA 8 ZENIX.v1i.yolov8/dataset/images"],
    ["python", "DataAugmentation.py", "--folderimage", "E:/DatasetUBC/CAMERA 9 FORTUNER.v1i.yolov8/dataset/images"],
    ["python", "DataAugmentation.py", "--folderimage", "E:/DatasetUBC/CAMERA 9 INNOVA.v1i.yolov8/dataset/images"],
    ["python", "DataAugmentation.py", "--folderimage", "E:/DatasetUBC/CAMERA 9 ZENIX.v1i.yolov8/dataset/images"],
]




# "E:\DatasetUBC\CAMERA 6 FORTUNER.v2i.yolov8"
# "E:\DatasetUBC\CAMERA 6 INNOVA.v1i.yolov8"
# "E:\DatasetUBC\CAMERA 6 ZENIX.v1i.yolov8"
# "E:\DatasetUBC\CAMERA 8 FORTUNER.v1i.yolov8"
# "E:\DatasetUBC\CAMERA 8 INNOVA.v1i.yolov8"
# "E:\DatasetUBC\CAMERA 8 ZENIX.v1i.yolov8"
# "E:\DatasetUBC\CAMERA 9 FORTUNER.v1i.yolov8"
# "E:\DatasetUBC\CAMERA 9 INNOVA.v1i.yolov8"
# "E:\DatasetUBC\CAMERA 9 ZENIX.v1i.yolov8"

processes = []

for cmd in commands:
    process = subprocess.Popen(cmd)
    processes.append(process)

# Tunggu semua selesai
for process in processes:
    process.wait()