import os

def count_classifications_in_file(file_path):
    class_counts = {}
    
    with open(file_path, 'r') as file:
        lines = file.readlines()
        
        for line in lines:
            parts = line.split()
            
            try:
                class_id = int(float(parts[0]))  # Convert to float first and then to int
            except (ValueError, IndexError):
                print(f"Skipping line due to format issue: {line.strip()}")
                continue
            
            if class_id in class_counts:
                class_counts[class_id] += 1
            else:
                class_counts[class_id] = 1
    
    return class_counts

def count_classifications_in_folder(folder_path):
    overall_class_counts = {}
    
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            file_class_counts = count_classifications_in_file(file_path)
            
            for class_id, count in file_class_counts.items():
                if class_id in overall_class_counts:
                    overall_class_counts[class_id] += count
                else:
                    overall_class_counts[class_id] = count
    
    return overall_class_counts

# Contoh penggunaan
folder_path = 'D:/Kuliah/Semester_5/DatasetPPEPandu/converted_images'
class_counts = count_classifications_in_folder(folder_path)
print(class_counts)
