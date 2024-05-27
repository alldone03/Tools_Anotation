import torch
import cv2
import numpy as np
import os

# Load the YOLOv5 model
model = torch.hub.load("ultralytics/yolov8", "custom", "C:/Users/Kanaaii/Documents/ITS/4Semester/PBL/Train/runs/detect/train6/weights/best.pt")
model.conf = 0.5

# Directory containing the images
image_folder = 'C:/Users/Kanaaii/Documents/ITS/4Semester/PBL/Train/train/images'
output_folder = 'D:/yoloaldan/Anotator/Tools_Anotation/output'

# Create the output directory if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Get list of images in the directory
image_files = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]

numberImage = 1

for image_file in image_files:
    image_path = os.path.join(image_folder, image_file)
    frame = cv2.imread(image_path)
    
    if frame is not None:
        myimage = frame.copy()
        results = model(frame)
        cv_img = np.squeeze(results.render())
        cv2.imshow('Frame', cv_img)
        
        # Save the original image
        cv2.imwrite(f"{output_folder}/Sequence_{numberImage:05}.jpg", myimage)
        imgsizex, imgsizey = cv_img.shape[1], cv_img.shape[0]
        
        if results.xywh[0].cpu().numpy().size != 0:
            label = ""
            for data in results.xywh[0].cpu().numpy():
                x, y, w, h, conf, labelidx = data
                print(f"{int(labelidx)} {(x/imgsizex):.2f} {(y/imgsizey):.2f} {(w/imgsizex):.2f} {(h/imgsizey):.2f}")
                label += f"{int(labelidx)} {(x/imgsizex):.2f} {(y/imgsizey):.2f} {(w/imgsizex):.2f} {(h/imgsizey):.2f}\n"
            
            with open(f"{output_folder}/Sequence_{numberImage:05}.txt", "w") as f:
                f.write(label)
        
        print(numberImage)
        numberImage += 1
        
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
        if numberImage >= 10:
            break

cv2.destroyAllWindows()
