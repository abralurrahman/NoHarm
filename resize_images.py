from PIL import Image
import os

# Define the directory containing your images and the target size
image_dir = "static/images"  # Replace with the path to your images
output_dir = "static/resized_images"  # Output directory for resized images
target_size = (150, 150)  # Target dimensions (width, height) in pixels

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Loop through all images in the directory
for filename in os.listdir(image_dir):
    if filename.endswith(('.jpg', '.jpeg', '.png')):  # Add more formats if needed
        img_path = os.path.join(image_dir, filename)
        output_path = os.path.join(output_dir, filename)

        # Open and resize the image
        with Image.open(img_path) as img:
            img_resized = img.resize(target_size, Image.Resampling.LANCZOS)  # High-quality resizing
            img_resized.save(output_path)

print("All images resized and saved to:", output_dir)
