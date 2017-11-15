import os
import math
from PIL import Image

from django.conf import settings

from core.models import Alliance, Corp

w = 35
h = 35
row_size = 20

def generate_alliance_spritesheet():
    # Get the list of icons we want to generate
    icon_map = Alliance.objects.filter(active=True).all()
    icon_map = map(lambda x: x.logo.path, icon_map)

    w = 35
    h = 35
    row_size = 20
    sprite_size = (w, h)

    images = []
    for filename in icon_map:
        image = Image.open(filename)
        image = image.resize(sprite_size, resample=Image.LANCZOS)
        images.append(image)

    master_width = w * row_size
    master_height = int(math.ceil(len(images) / row_size)) * h

    master = Image.new(
        mode='RGBA',
        size=(master_width, master_height),
        color=(0,0,0, 0)
    )

    for i, image in enumerate(images):
        location = (
            (i % row_size) * w,
            int(math.floor(i / row_size)) * h
        )
        master.paste(image, location)

    path = os.path.join(settings.MEDIA_ROOT, "alliances.png")
    master.save(path, 'PNG', optimize=True)
    return path
