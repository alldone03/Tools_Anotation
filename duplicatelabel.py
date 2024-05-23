import os

def find_duplicate_data_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        print(f"Processing file: {file_path}")
        find_duplicate_data(file_path)

def find_duplicate_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            lines = file.readlines()
    except UnicodeDecodeError:
        print(f"Failed to read file {file_path} with utf-8 encoding.")
        return

    # Menghapus karakter whitespace dan newline dari setiap baris, kemudian mengonversi ke set untuk mendeteksi duplikat
    unique_lines = set(line.strip() for line in lines)

    # Menampilkan data duplikat
    duplicate_lines = [line for line in lines if lines.count(line.strip()) > 1]
    print("Data Duplikat:")
    for line in duplicate_lines:
        print(line.strip())

    # Menulis ulang file tanpa baris duplikat
    with open(file_path, 'w', encoding='utf-8', errors='ignore') as file:
        for line in unique_lines:
            file.write(line + '\n')

# Path ke folder yang berisi file teks yang akan diperiksa
folder_path = 'C:/Users/Aldan Prayogi/Desktop/pythonImagedetection/labeled/Images'

find_duplicate_data_in_folder(folder_path)
print("Proses selesai.")