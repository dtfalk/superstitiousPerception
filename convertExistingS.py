from PIL import Image
import os
import numpy as np

# Load the image
image = Image.open(os.path.join(os.path.dirname(__file__), 'imageGeneration', 'templateSpecificFunctions', 'S_temp.png')).convert('L')

# Resize the image
resized_image = image.resize((25, 25),  Image.Resampling.LANCZOS).point(lambda p: 255 if p >= 240 else 0) 

# Create a new grayscale image with a white background
canvas = Image.new('L', (50, 50), 255)  # 'L' mode and '255' is white in grayscale

# Calculate the position to paste the resized image on the canvas (centering it)
x = (canvas.width - resized_image.width) // 2
y = (canvas.height - resized_image.height) // 2

# Paste the resized grayscale image onto the canvas
canvas.paste(resized_image, (x, y))

canvas.save(os.path.join(os.path.dirname(__file__), 'arraysAndImages', 'templates', 'hiAnalysis', 'images', 'S.png'))

array = np.array(canvas)
np.save(os.path.join(os.path.dirname(__file__), 'arraysAndImages', 'templates', 'hiAnalysis', 'arrays', 'S.png'), array)
