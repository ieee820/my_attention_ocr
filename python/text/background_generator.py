import cv2
import math
import os
import random
import numpy as np
import sys, os
from PIL import Image, ImageFont, ImageDraw, ImageFilter

class BackgroundGenerator(object):
    @classmethod
    def gaussian_noise(cls, height, width):
        """
            Create a background with Gaussian noise (to mimic paper)
        """

        # We create an all white image
        image = np.ones((height, width)) * 255

        # We add gaussian noise
        cv2.randn(image, 235, 10)

        return Image.fromarray(image).convert('L')

    @classmethod
    def plain_white(cls, height, width):
        """
            Create a plain white background
        """

        return Image.new("L", (width, height), 255)

    @classmethod
    def quasicrystal(cls, height, width):
        """
            Create a background with quasicrystal (https://en.wikipedia.org/wiki/Quasicrystal)
        """

        image = Image.new("L", (width, height))
        pixels = image.load()

        frequency = random.random() * 30 + 20 # frequency
        phase = random.random() * 2 * math.pi # phase
        rotation_count = random.randint(10, 20) # of rotations

        for kw in range(width):
            y = float(kw) / (width - 1) * 4 * math.pi - 2 * math.pi
            for kh in range(height):
                x = float(kh) / (height - 1) * 4 * math.pi - 2 * math.pi
                z = 0.0
                for i in range(rotation_count):
                    r = math.hypot(x, y)
                    a = math.atan2(y, x) + i * math.pi * 2.0 / rotation_count
                    z += math.cos(r * math.sin(a) * frequency + phase)
                c = int(255 - round(255 * z / rotation_count))
                pixels[kw, kh] = c # grayscale
        return image

    @classmethod
    def picture(cls, height, width, bg_dir="../resource/bgimg/images"):
        """
            Create a background with a picture
        """
        if not os.path.exists(bg_dir):
            parentdir = os.path.dirname(os.path.abspath(__file__))
            bg_dir = os.path.join(parentdir, bg_dir)

        # print(bg_dir)
        pictures = os.listdir(bg_dir)
        #
        # print("-------------")
        # print(pictures)

        if len(pictures) > 0:
            image_file = os.path.join(bg_dir, random.choice(pictures))
            picture = Image.open(image_file)

            if picture.size[0] < width:
                picture = picture.resize([width, int(picture.size[1] * (width / picture.size[0]))], Image.ANTIALIAS)
            elif picture.size[1] < height:
                picture.thumbnail([int(picture.size[0] * (height / picture.size[1])), height], Image.ANTIALIAS)

            if (picture.size[0] == width):
                x = 0
            else:
                x = random.randint(0, picture.size[0] - width)
            if (picture.size[1] == height):
                y = 0
            else:
                if picture.size[1] > height:
                    y = random.randint(0, picture.size[1] - height)
                else:
                    y = random.randint(0,  height - picture.size[1])

            return picture.crop(
                (
                    x,
                    y,
                    x + width,
                    y + height,
                )
            )
        else:
            raise Exception('No images where found in the pictures folder!')