from PIL import Image, ImageDraw, ImageFont
import os
from itertools import combinations


def get_text(text, hsize, vsize):
    #тестовая картинка, только чтобы подобрать размер шрифта
    im = Image.new('RGB', (1000, 700), (0, 0, 0))
    #пока будем писать 5-м кеглем
    maxsize = 5

    font = ImageFont.truetype('arial.ttf', maxsize)
    temp = ImageDraw.ImageDraw(im)
    #вычисляем размер надписи в одну строку
    text_hsize, text_vsize = temp.multiline_textsize(text=text, font=font, spacing=0)
    #смотрим, каким максимальным кеглем его можно написать
    while text_hsize < hsize and text_vsize < vsize:
        maxsize += 1
        font = ImageFont.truetype('arial.ttf', maxsize)
        text_hsize, text_vsize = temp.multiline_textsize(text=text, font=font, spacing=0)

    #делаем список слов с пробелами между ними
    words = '* *'.join(text.split()).split('*')
    n = words.count(' ')
    #перебираем все возможные для нашего текста количества переносов строки
    for numberofenters in range(n + 1):
        #и все их возможные расстановки, вот это медленно работает :(
        all_enters = combinations(range(n), numberofenters)
        for enters in all_enters:
            temp_ans = words.copy()
            #расставляем вместо пробелов переносы строк
            for enter in enters:
                temp_ans[2 * enter + 1] = '\n'
            #собираем строку уже с переносами
            temp_text = ''.join(temp_ans)
            #берём максимальный полученный на текущий размер шрифт
            fsize = maxsize
            #пробуем его на новой строке
            text_hsize, text_vsize = temp.multiline_textsize(text=temp_text, font=font, spacing=0)
            #если влезает в поле - увеличиваем шрифт ещё
            while text_hsize < hsize and text_vsize < vsize:
                fsize += 1
                font = ImageFont.truetype('arial.ttf', fsize)
                text_hsize, text_vsize = temp.multiline_textsize(text=temp_text, font=font, spacing=0)
            #ну и если получили больше, чем было - значит, такая расстановка переносов пока оптимальная. запоминаем)
            if fsize > maxsize:
                maxsize = fsize
                ans = temp_text
    return (ans, maxsize)


def put_text(fname, textandsize):
    img = Image.open(fname)
    draw = ImageDraw.Draw(img)
    width, height = img.size

    #определяем центральный пиксель - это и для цвета, и для положения текста
    cx, cy = width // 2, height // 2
    rgb = img.convert('RGB')

    #берём цвет центрального пикселя
    central = rgb.getpixel((cx, cy))
    #если свелтый фон, надпись будет чёрная, иначе белая
    color = 'black' if sum(central) > 255 * 1.5 else 'white'
    #это границы надписи
    x0, x1, y0, y1 = cx - 450, cx + 450, cy - 300, cy + 300

    #вычисляем предельно допустимые размеры надписи
    hsize = x1 - x0
    vsize = y1 - y0

    #устанавливаем шрифт
    font = ImageFont.truetype('arial.ttf', textandsize[1])

    #наносим лучший текст - который соответствует максимальному шрифту - на открытку
    draw.text(((x0 + x1) // 2, (y0 + y1) // 2), textandsize[0], align='center', fill=color, anchor='mm', font=font)
    #и сохраняем
    img.save('0' + fname)


# перебираем все картинки, кроме тех, которые сделала сама программа
images = [i for i in os.listdir() if i.endswith('jpg') and i[0] != '0']
text = input('Введите поздравление: ')
# вычисляем, как расставить переносы, если у нас надпись 900*600
ans = get_text(text, 900, 600)
# и наносим полученную надпись уже известным шрифтом на все картинки
for i in images:
    put_text(i, ans)
