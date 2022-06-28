from PIL import Image, ImageDraw, ImageFont
import os

def dif(px1, px2):
    return (px1[0] - px2[0]) + (px1[1] - px2[1]) + (px1[2] - px2[2]) > 50
    

def area_detect(fname, text):
    img = Image.open(fname)
    width, height = img.size
    cx, cy = width // 2, height // 2
    rgb = img.convert('RGB')
    x0, x1, y0, y1 = cx - 450, cx + 450, cy - 300, cy + 300

    draw = ImageDraw.Draw(img)
    
    fsize = 5
    
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
text = input('Введите поздравление: ')
for i in images:
    area_detect(i, text)

