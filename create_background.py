from PIL import Image, ImageDraw

# Create a new image with a light blue gradient background
width = 1920
height = 1080
image = Image.new('RGB', (width, height))
draw = ImageDraw.Draw(image)

# Create a gradient from light blue to white
for y in range(height):
    r = int(135 + (255 - 135) * (y / height))
    g = int(206 + (255 - 206) * (y / height))
    b = int(235 + (255 - 235) * (y / height))
    draw.line([(0, y), (width, y)], fill=(r, g, b))

# Save the image
image.save('background2.png') 