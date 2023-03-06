from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import random

# create empty image
width, height = 500, 500
image = Image.new("RGB", (width, height))

# draw a filled rectangle on the image
draw = ImageDraw.Draw(image)
draw.rectangle([(0, 0), (width, height)], fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

# add text to image
text = "Python正改变世界"
font = ImageFont.truetype("arial.ttf", 30)  # font style and size
textwidth, textheight = draw.textsize(text, font)
x = (width - textwidth) // 2
y = (height - textheight) // 2
draw.text((x, y), text, font=font, fill=(255, 255, 255))

# save the completed image
image.save('poster.png')
