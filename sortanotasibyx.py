import os

def sort_yolo_labels_by_x(input_folder):
    for filename in os.listdir(input_folder):
        if filename == 'labels.txt':
            continue
        if filename.endswith(".txt"):
            file_path = os.path.join(input_folder, filename)
            
            with open(file_path, 'r') as file:
                lines = file.readlines()
            print(lines)
            
            # Parse and sort lines by the x_center value (second value in each line)
            
            sorted_lines = sorted(lines, key=lambda line: float(line.split()[1]))
            
            # Write sorted lines back to the file
            with open(file_path, 'w') as file:
                file.writelines(sorted_lines)
            print(f"Sorted {filename}")

# Replace 'path_to_input_folder' with your actual input folder path
input_folder_path = 'C:/Users/Aldan Prayogi/Desktop/pythonImagedetection/AnotatorNie/Anotator5'
sort_yolo_labels_by_x(input_folder_path)