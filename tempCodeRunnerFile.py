for _, row in best_per_file.iterrows():
#     model = row["Model"]
#     src_path = row["Path Gambar"]
#     img_name = row["Nama File"]
#     label_data = row["Label YOLO Format"]
    
#     datetime_folder = os.path.basename(os.path.dirname(src_path))
#     new_filename = f"{datetime_folder}_{img_name}"  # contoh: 2025-06-24_10-30-33_CAMERA_1.jpg
#     new_txtname = new_filename.replace(".jpg", ".txt")

    

#     # Ambil nama folder datetime dari path (misalnya: E:\datacamera2\2025-06-24_10-30-33\CAMERA_1.jpg)
#     datetime_folder = os.path.basename(os.path.dirname(src_path))  # hasilnya: 2025-06-24_10-30-33

#     # Penamaan baru file: gabungan datetime dan nama file
#     new_filename = f"{datetime_folder}_{img_name}"

#     # Folder model di dalam output_root
#     model_folder = os.path.join(output_root, model)
#     os.makedirs(model_folder, exist_ok=True)

#     dst_path = os.path.join(model_folder, new_filename)
    
    
#     if isinstance(label_data, str) and label_data.strip() != "[]":
#         try:
#             yolo_lines = ast.literal_eval(label_data)
#             dst_txt_path = os.path.join(model_folder, new_txtname)
#             with open(dst_txt_path, "w") as f:
#                 for line in yolo_lines:
#                     f.write(f"{line}\n")
#             print(f"📝 Label disimpan di {dst_txt_path}")
#         except Exception as e:
#             print(f"⚠ Gagal simpan label: {e}")
#     # Copy file
#     try:
        
#         shutil.copy(src_path, dst_path)
#         print(f"✔ {img_name} -> {dst_path}")
#     except FileNotFoundError:
#         print(f"⚠ File tidak ditemukan: {src_path}")
    