# Revised version with corrected syntax, re-attempting the processing

from PIL import Image, ImageFilter

# Load the image
image_path = 'IMG_3046.jpeg'

# Open and convert HEIC to RGB
try:
    with Image.open(image_path) as img:
        img_rgb = img.convert("RGB")  # Convert to RGB for manipulation

        # Apply background blur
        blurred_img = img_rgb.filter(ImageFilter.GaussianBlur(8))  # Moderate blur for background

        # Simulate isolating artwork by adding a sharpen effect (for demonstration purposes)
        artwork_sharpened = blurred_img.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))

        # Save the processed image
        output_path = "processed_image.jpg"
        artwork_sharpened.save(output_path, "JPEG")
        
        # Output the path to the saved image
        output_path

except Exception as e:
    e
