import os


def ubah_class_yolo(input_folder, output_folder):
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    
    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):  
            input_file = os.path.join(input_folder, filename)
            output_file = os.path.join(output_folder, filename)

            try:
                
                with open(input_file, 'r') as file:
                    lines = file.readlines()

                
                modified_lines = []

                
                for line in lines:
                    elements = line.split()
                    if elements[0] == '0':  
                        elements[0] = '1'    
                    
                    modified_line = ' '.join(elements)
                    modified_lines.append(modified_line)

                
                with open(output_file, 'w') as file:
                    file.write('\n'.join(modified_lines))

                print(f"Class label 0 pada file {filename} berhasil diubah menjadi 1.")

            except FileNotFoundError:
                print(f"File {input_file} tidak ditemukan.")
            except Exception as e:
                print(f"Terjadi kesalahan pada file {filename}: {e}")


input_folder = 'C:/Users/Aldan/Desktop/sawitmini/dataset/canpuranbrondol'  
output_folder = 'C:/Users/Aldan/Desktop/sawitmini/dataset/lbl_out'  


ubah_class_yolo(input_folder, output_folder)
