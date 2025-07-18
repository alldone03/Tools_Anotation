import torch
import cv2
import numpy as np
import os
import argparse
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator


# python pythonmakeinferenceimageyolov8.py --model_path "E:\InnovaCam5OK\train4\weights\best.pt" --image_folder "C:\Users\Aldan\Desktop\IMPROTOYOTA\Camera 1\Inn\MR_cropped" --output_folder "C:\Users\Aldan\Desktop\IMPROTOYOTA\Camera 1\Inn\MR_cropped_annotated"
# python pythonmakeinferenceimageyolov8.py --model_path "C:/Users/Aldan/Desktop/ImproTYT/INNOVA/GoodDetection/train3/weights/best.pt" --image_folder "C:/Users/Aldan/Desktop/ImproTYT/INNOVA/dataset" --output_folder "C:/Users/Aldan/Desktop/ImproTYT/INNOVA/newDataset_anotatedd"

# Argument parser
parser = argparse.ArgumentParser(description='YOLO Image Annotator')
parser.add_argument('--model_path', type=str, required=True, help='Path ke file model .pt')
parser.add_argument('--image_folder', type=str, required=True, help='Folder tempat gambar input')
parser.add_argument('--output_folder', type=str, required=True, help='Folder output hasil anotasi')
args = parser.parse_args()

# Load model
model = YOLO(args.model_path)  # Set confidence threshold

# Buat folder output kalau belum ada
if not os.path.exists(args.output_folder):
    os.makedirs(args.output_folder)
    
label_file_path = os.path.join(args.output_folder, "labels.txt")
if not os.path.exists(label_file_path):
    with open(label_file_path, "w") as f:
        for class_id, class_name in model.names.items():
            f.write(f"{class_id}: {class_name}\n")

image_files = [f for f in os.listdir(args.image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]

numberImage = 1
total_detections = 0
confidences = []

x_line = 100



for image_file in image_files:
    image_path = os.path.join(args.image_folder, image_file)
    frame = cv2.imread(image_path)

    if frame is not None:
        myimage = frame.copy()
        results = model(frame,conf=0.5, iou=0.45, agnostic_nms=True, max_det=1000)
        annotator = Annotator(frame)
        for r in results:
            for box in r.boxes:
                b = box.xyxy[0]
                if b[1] > x_line:
                    c = box.cls
                    annotator.box_label(b, f"",(0, 255, 0))
                    
                    
        
        cv2.line(frame, (0, x_line), (frame.shape[1] - 1, x_line), (255, 0, 0), 2)

        for result in results:
            for box in result.boxes:
                x, y, w, h = box.xywh[0].cpu().numpy()
                conf = box.conf.cpu().numpy().item()
                labelidx = int(box.cls.cpu().numpy().item())

                x1 = int((x - w / 2) * frame.shape[1])
                y1 = int((y - h / 2) * frame.shape[0])
                x2 = int((x + w / 2) * frame.shape[1])
                y2 = int((y + h / 2) * frame.shape[0])
                
                total_detections += 1
                confidences.append(conf)
                print(f" - Class: {labelidx}, Conf: {conf:.2f}, X: {x:.1f}, Y: {y:.1f}, W: {w:.1f}, H: {h:.1f}")

                # cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 1)
                # cv2.putText(frame, f'{labelidx} {conf:.2f}', (x1, y1 - 10),
                #             cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
        
        if total_detections > 0:
            total_detection = 0
            avg_conf = sum(confidences) / total_detections
            print(f"\nTotal Deteksi: {len(result.boxes)} class")
            print(f"Rata-rata Confidence: {avg_conf:.2f}")
        else:
            print("\nTidak ada objek terdeteksi.")
            

        try:
            
            cv2.imshow('Frame', frame)
            
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        except cv2.error:
            print("Preview tidak didukung di environment ini.")

        

        output_img_path = os.path.join(args.output_folder, f"Sequence_{numberImage:05}.jpg")
        cv2.imwrite(output_img_path, myimage)

        imgsizex, imgsizey = frame.shape[1], frame.shape[0]

        if len(results) > 0:
            label = ""
            for result in results:
                for box in result.boxes:
                    x, y, w, h = box.xywh[0].cpu().numpy()
                    labelidx = int(box.cls.cpu().numpy().item())
                    label += f"{labelidx} {(x / imgsizex):.2f} {(y / imgsizey):.2f} {(w / imgsizex):.2f} {(h / imgsizey):.2f}\n"

            label_file_path = os.path.join(args.output_folder, f"Sequence_{numberImage:05}.txt")
            with open(label_file_path, "w") as f:
                f.write(label)

        print(numberImage)
        numberImage += 1
        
        if numberImage >= 1000:
            break

