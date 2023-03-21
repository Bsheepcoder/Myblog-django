# -*- coding:utf-8 -*-
"""
作者：71041
日期：2023年03月05日
"""
from PIL import Image, ImageDraw, ImageFont
import random
import string


def check_code(width=120, height=30, char_length=5, font_file='./userprofile/utils/Monaco-1.ttf', font_size=28):
    # 创建图片
    img = Image.new(mode='RGB', size=(width, height), color=(193, 193, 193))
    draw = ImageDraw.Draw(img, mode='RGB')
    font = ImageFont.truetype(font_file, font_size)
    color = ['blue', 'black', 'red', 'yellow', 'green']
    # 生成随机数字
    randomChar = ''.join(random.sample(string.ascii_letters + string.digits, char_length))
    # 画字字符
    betweenWidth = 10
    number = int(len(randomChar))
    count = 0
    for i in randomChar:
        count = count % number
        c = random.choice(color)
        draw.text((10 + (betweenWidth + 10) * count, -2), i, c, font=font)
        count += 1

    # 画干扰点
    charList = ['~', '-', '`', '^', '+', '-', '=']
    font = ImageFont.truetype(font_file, 14)
    for x in range(10):
        for y in range(2):
            c = random.choice(color)
            char = random.choice(charList)
            draw.text((15 * x, 15 * y), char, c, font=font)

    return img, randomChar


check_code()
