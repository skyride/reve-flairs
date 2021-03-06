import os
import math
from PIL import Image

from django.conf import settings

w = 25
h = 25
row_size = 1

generic_alliance_logo = Image.open(os.path.join(settings.BASE_DIR, "core/generic_alliance_logo.png"))


def is_generic_alliance_logo(logo):
    histogram = Image.open(logo).histogram()
    return generic_alliance_logo.histogram() == histogram

def calc_location(i, w=w, h=h, row_size=row_size):
    return (
        (i % row_size) * w,
        int(math.floor(i / row_size)) * h
    )

def generate_spritesheet(icon_map, output_file, w=w, h=h, row_size=row_size):
    # Get the list of icons we want to generate
    icon_map = map(lambda x: x.logo.path, icon_map)
    sprite_size = (w, h)

    images = []
    for filename in icon_map:
        image = Image.open(filename)
        image = image.resize(sprite_size, resample=Image.LANCZOS)
        images.append(image)

    master_width = w * row_size
    master_height = int(math.ceil(float(len(images)) / row_size)) * h

    master = Image.new(
        mode='RGBA',
        size=(master_width, master_height),
        color=(0,0,0, 0)
    )

    for i, image in enumerate(images):
        location = calc_location(i)
        master.paste(image, location)

    path = os.path.join(settings.MEDIA_ROOT, output_file)
    master.save(path, 'PNG', optimize=True)
    return path
