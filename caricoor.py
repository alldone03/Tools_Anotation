import tkinter as tk
from PIL import Image, ImageTk

# Inisialisasi window
window = tk.Tk()
window.title("Ambil Koordinat Bounding Box")

# Buka gambar
image_path = r"C:\Users\Aldan\Desktop\ImproTYT\ZENIX\CAMERA 5 ZENIX.v4i.yolov8\dataset_filtered_cropped_rescaled_1.5\CAMERA_1_2024-09-19_05-38-02_jpg.rf.4d5f331d7d4f4b18cff6aa4ce5ca0519.jpg"  # ganti dengan nama file gambar kamu
image = Image.open(image_path)
photo = ImageTk.PhotoImage(image)

# Buat canvas
canvas = tk.Canvas(window, width=photo.width(), height=photo.height())
canvas.pack()

# Tampilkan gambar di canvas
canvas.create_image(0, 0, anchor=tk.NW, image=photo)

# Variabel global untuk posisi klik
start_x, start_y = 0, 0
rect = None

def on_mouse_down(event):
    global start_x, start_y, rect
    start_x, start_y = event.x, event.y
    # Hapus kotak lama kalau ada
    if rect:
        canvas.delete(rect)
    # Buat kotak awal
    rect = canvas.create_rectangle(start_x, start_y, start_x, start_y, outline="red", width=2)

def on_mouse_drag(event):
    # Update ukuran kotak saat mouse digeser
    canvas.coords(rect, start_x, start_y, event.x, event.y)

def on_mouse_up(event):
    end_x, end_y = event.x, event.y
    x1, y1 = min(start_x, end_x), min(start_y, end_y)
    x2, y2 = max(start_x, end_x), max(start_y, end_y)
    print("Koordinat kotak:", x1, y1, x2, y2)

# Bind mouse
canvas.bind("<Button-1>", on_mouse_down)
canvas.bind("<B1-Motion>", on_mouse_drag)
canvas.bind("<ButtonRelease-1>", on_mouse_up)

window.mainloop()