import torch
import cv2 
import numpy as np 

model = torch.hub.load("C:/Users/Aldan Prayogi/Desktop/pythonImagedetection/yolov5","custom", "C:/Users/Aldan Prayogi/Desktop/pythonImagedetection/exp37/exp37/weights/best.pt",source='local') 
model.conf = 0.5
cap = cv2.VideoCapture('C:/Users/Aldan Prayogi/Desktop/pythonImagedetection/Sequence 01_2.mp4') 
if (cap.isOpened()== False): 
    print("Error opening video file") 
i=0
numberImage = 1
while(cap.isOpened()): 
    ret, frame = cap.read() 
    i+=1
    if i%8==0:
        # print(i)
        if ret == True: 
            myimage = frame.copy()
            results = model(frame)
            cv_img = np.squeeze(results.render())
            cv2.imshow('Frame', cv_img) 
        cv2.imwrite(f"./newdataset/saveImg/Sequence_{numberImage:05}.jpg", myimage) 
        imgsizex,imgsizey = cv_img.shape[1],cv_img.shape[0]
        if results.xywh[0].cpu().numpy().size != 0:
            label = ""
            for data in results.xywh[0].cpu().numpy():
                x,y,w,h,conf,labelidx = data
                print(f"{int(labelidx)} {(x/imgsizex):2f} {(y/imgsizey):2f} {(w/imgsizex):2f} {(h/imgsizey):2f}")
                label +=f"{int(labelidx)} {(x/imgsizex):2f} {(y/imgsizey):2f} {(w/imgsizex):2f} {(h/imgsizey):2f}\n"
                
            f = open(f"./newdataset/saveImg/Sequence_{numberImage:05}.txt", "w")
            f.write(label)
            f.close()
        print(numberImage)
        numberImage += 1
    if cv2.waitKey(25) & 0xFF == ord('q'): 
            break
    if numberImage >= 7000:
        break

cap.release() 
cv2.destroyAllWindows() 