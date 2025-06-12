import cv2

# 1. Import gambar
image = cv2.imread('C:/Users/Aldan/Desktop/IMPROTOYOTA/CAMERA 5 INNOVA.v4i.yolov8/dataset/images/CAMERA_1_2024-08-27_08-45-45_jpg.rf.ddbbb69166ea508614705cda4c87a437.jpg')  # Ganti 'gambar.jpg' dengan nama file kamu

# 2. Tampilkan gambar asli
cv2.imshow('Gambar Asli', image)

# 3. Fungsi untuk skalakan gambar
def scale_image(img, scale_x, scale_y):
    width = int(img.shape[1] * scale_x)
    height = int(img.shape[0] * scale_y)
    return cv2.resize(img, (width, height))

# 4. Skalakan gambar
scaled = scale_image(image, 1.5, 1.5)

# 5. Tampilkan gambar hasil skala
cv2.imshow('Gambar Diperbesar', scaled)

cv2.waitKey(0)
cv2.destroyAllWindows()

        