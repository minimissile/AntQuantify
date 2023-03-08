"""
测试图片生成
"""

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import random

# 定义图片宽高
width, height = 500, 500
image = Image.new("RGB", (width, height))

# 在图像上绘制一个填充的矩形
draw = ImageDraw.Draw(image)
draw.rectangle([(0, 0), (width, height)], fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

# 添加图片到文字上
text = "ai改变世界"
font = ImageFont.truetype("arial.ttf", 30)  # font style and size

text_width, text_height = draw.textsize(text, font)
x = (width - text_width) // 2
y = (height - text_height) // 2

draw.text((x, y), text, font=font, fill=(255, 255, 255))

# save the completed image
image.save('./poster.png')
