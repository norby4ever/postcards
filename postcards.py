from PIL import Image, ImageDraw, ImageFont
import os

def dif(px1, px2):
    return (px1[0] - px2[0]) + (px1[1] - px2[1]) + (px1[2] - px2[2]) > 50
    

def area_detect(fname):
    img = Image.open(fname)
    width, height = img.size
    cx, cy = width // 2, height // 2
    rgb = img.convert('RGB')
    x0, x1, y0, y1 = cx, cx, cy, cy
    while not dif(rgb.getpixel((cx, cy)), rgb.getpixel((x0, cy))) and x0 > 1:
        x0 -= 1
    while not dif(rgb.getpixel((cx, cy)), rgb.getpixel((x1, cy))) and x1 < width - 1:
        x1 += 1
    while not dif(rgb.getpixel((cx, cy)), rgb.getpixel((cx, y0))) and y0 > 1:
        y0 -= 1
    while not dif(rgb.getpixel((cx, cy)), rgb.getpixel((cx, y1))) and y1 < height - 1:
        y1 += 1
    draw = ImageDraw.Draw(img)
    draw.rectangle((x0, y0, x1, y1), outline=(0, 100, 200, 200))
    
    fsize = 5
    text = "Стас Михайлов\nискренне поздравляет вас\nс днём рождения! <3"
    font = ImageFont.truetype('arial.ttf', fsize)
    temp = ImageDraw.ImageDraw(img)
    text_hsize, text_vsize = temp.multiline_textsize(text=text, font=font, spacing=0)
    hsize = x1 - x0
    vsize = y1 - y0
    
    while text_hsize < hsize and text_vsize < vsize:
        fsize += 1
        font = ImageFont.truetype('arial.ttf', fsize)
        text_hsize, text_vsize = temp.multiline_textsize(text=text, font=font, spacing=0)
    draw.text(((x0 + x1) // 2, (y0 + y1) // 2), text, align='center', anchor='mm', font=font)    
    img.save('0' + fname)

images = [i for i in os.listdir() if i.endswith('jpg') and i[0] != '0']
for i in images:
    area_detect(i)

"""
fsize = 5
text = "Стас Михайлов\nискренне поздравляет вас\nс днём рождения! <3"
draw = ImageDraw.Draw(img)
font = ImageFont.truetype('arial.ttf', fsize)
temp = ImageDraw.ImageDraw(img)
text_hsize, text_vsize = temp.multiline_textsize(text=text, font=font, spacing=0)
x0, y0, x1, y1 = 100, 100, 400, 300
hsize = x1 - x0
vsize = y1 - y0
draw.rectangle((x0, y0, x1, y1), outline=(0, 100, 200, 200))
while text_hsize < hsize and text_vsize < vsize:
    fsize += 1
    font = ImageFont.truetype('arial.ttf', fsize)
    text_hsize, text_vsize = temp.multiline_textsize(text=text, font=font, spacing=0)
draw.text(((x0 + x1) // 2, (y0 + y1) // 2), text, align='center', anchor='mm', font=font)
img.save('res.jpg', "JPEG")
"""