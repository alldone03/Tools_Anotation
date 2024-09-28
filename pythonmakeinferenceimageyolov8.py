import torch
import cv2
import numpy as np
import os
from ultralytics import YOLO


model = YOLO("C:/Users/Kanaaii/Documents/ITS/4Semester/PBL/Train/runs/detect/train6/weights/best.pt")


image_folder = 'C:/Users/Kanaaii/Documents/ITS/4Semester/PBL/Train/train/images'
output_folder = 'D:/yoloaldan/Anotator/Tools_Anotation/output'


if not os.path.exists(output_folder):
    os.makedirs(output_folder)


image_files = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]

numberImage = 1

for image_file in image_files:
    image_path = os.path.join(image_folder, image_file)
    frame = cv2.imread(image_path)
    
    if frame is not None:
        myimage = frame.copy()
        results = model(frame)
        
        
        for result in results:
            for box in result.boxes:
                x, y, w, h = box.xywh[0].cpu().numpy()
                conf = box.conf.cpu().numpy().item()  
                labelidx = int(box.cls.cpu().numpy().item())
                
                
                x1 = int((x - w / 2) * frame.shape[1])
                y1 = int((y - h / 2) * frame.shape[0])
                x2 = int((x + w / 2) * frame.shape[1])
                y2 = int((y + h / 2) * frame.shape[0])
                
                
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f'{labelidx} {conf:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
        
        cv_img = np.squeeze(frame)
        cv2.imshow('Frame', cv_img)
        
        
        cv2.imwrite(f"{output_folder}/Sequence_{numberImage:05}.jpg", myimage)
        imgsizex, imgsizey = frame.shape[1], frame.shape[0]
        
        if len(results) > 0:
            label = ""
            for result in results:
                for box in result.boxes:
                    x, y, w, h = box.xywh[0].cpu().numpy()
                    labelidx = int(box.cls.cpu().numpy().item())
                    label += f"{labelidx} {(x/imgsizex):.2f} {(y/imgsizey):.2f} {(w/imgsizex):.2f} {(h/imgsizey):.2f}\n"
            
            with open(f"{output_folder}/Sequence_{numberImage:05}.txt", "w") as f:
                f.write(label)
        
        print(numberImage)
        numberImage += 1
        
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
        if numberImage >= 1000:
            break

cv2.destroyAllWindows()
