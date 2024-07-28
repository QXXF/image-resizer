import os
from PIL import Image
import json
from math import ceil

def calculate_sizes(width, height, max_width=1920):
    aspect_ratio = width / height
    sizes = []
    current_width = max_width
    
    while current_width >= 48:
        current_height = ceil(current_width / aspect_ratio)
        sizes.append((current_width, current_height))
        current_width = ceil(current_width / 1.5)
    
    return sizes

def resize_and_optimize_image(input_path, output_folder, filename):
    with Image.open(input_path) as img:
        original_width, original_height = img.size
        sizes = calculate_sizes(original_width, original_height)
        
        # Crea la cartella di output se non esiste
        os.makedirs(output_folder, exist_ok=True)
        
        src_set = []
        for size in sizes:
            resized_img = img.copy()
            resized_img.thumbnail(size)
            output_filename = f"{size[0]}x{size[1]}.webp"
            output_path = os.path.join(output_folder, output_filename)
            resized_img.save(output_path, "WEBP", quality=85)
            
            src_set.append({
                "src": f"{filename}/{output_filename}",
                "width": size[0],
                "height": size[1]
            })
        
        # Crea l'oggetto JSON
        image_data = {
            "src": f"{filename}/{sizes[0][0]}x{sizes[0][1]}.webp",
            "key": filename,
            "width": sizes[0][0],
            "height": sizes[0][1],
            "srcSet": src_set
        }
        
        # Salva l'oggetto JSON
        json_path = os.path.join(output_folder, "image_data.json")
        with open(json_path, "w") as json_file:
            json.dump(image_data, json_file, indent=2)

def process_images():
    input_folder = "input"
    output_folder = "output"
    
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            input_path = os.path.join(input_folder, filename)
            image_output_folder = os.path.join(output_folder, os.path.splitext(filename)[0])
            resize_and_optimize_image(input_path, image_output_folder, os.path.splitext(filename)[0])

if __name__ == "__main__":
    process_images()