import os
import cv2
import sys

from rich.console import Console
console = Console()

image = cv2.imread(f'/home/heisendelta/Pictures/{sys.argv[1]}', cv2.IMREAD_UNCHANGED)
imgSize = (image.shape[1], image.shape[0])
termSize = os.get_terminal_size()

os.system('clear')

print(f'Image size (unscaled): {imgSize[0]}x{imgSize[1]}')
print(f'Terminal size: {termSize.columns}x{termSize.lines}')


# Image resizing

if imgSize[0] > termSize.columns:
    hbyw = imgSize[1] / imgSize[0]
    wbyh = imgSize[0] / imgSize[1]

    # image = cv2.resize(image, (termSize.columns, round(termSize.columns * hbyw * 0.55)), interpolation = cv2.INTER_AREA) # Scale with width
    image = cv2.resize(image, (round(termSize.lines * wbyh / 0.55), termSize.lines), interpolation = cv2.INTER_AREA)       # Scale by height

    imgSize = (image.shape[1], image.shape[0])
    print(f'Image size (scaled): {imgSize[0]}x{imgSize[1]}')

str_ = ''
for i in range(min(imgSize[1], 500)):
    for j in range(min(imgSize[0], termSize.columns)):

        pix = image[i][j]
        hexCode = '#%02x%02x%02x' % (pix[2], pix[1], pix[0])

        str_ += f'[{hexCode}]0[/{hexCode}]'
    str_ += '\n'

console.print(str_)

