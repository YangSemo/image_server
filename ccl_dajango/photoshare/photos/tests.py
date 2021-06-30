from django.test import TestCase

import os
from thumb_gen.worker import Generator

folder = 'C:/Users/SAMSUNG/CCLab_git/image_server/ccl_dajango/photoshare/static/images'
for video in os.listdir(folder):
    if video.endswith('.mp4') or video.endswith('.mkv'):
        app = Generator(os.path.join(folder, video),output_path=folder ,custom_text=False, font_size=25)
        app.run()