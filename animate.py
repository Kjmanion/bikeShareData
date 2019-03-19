# Creating a gif with Pillow to combine 30 frames created by the QGIS plugin TimeManager, since I am not on a Mac/Linux machine
from PIL import Image
import os

files = os.listdir()
images = []
print (files)
for fil in files:
    if "frame000.png" in fil:
        firstimage = Image.open(fil)
    if ".png" in fil and "000" not in fil:
        print (fil)
        image = Image.open(fil)
        images.append(image)

firstimage.save('out2.gif', save_all=True, append_images=images, duration=100, loop=0)

