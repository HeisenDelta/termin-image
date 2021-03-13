import os
import cv2

from rich.console import Console
console = Console()

image = cv2.imread('/home/heisendelta/Pictures/img3.jpeg')
termSize = os.get_terminal_size()

print(f'Image size: {image.shape[0]}x{image.shape[1]}')
print(f'Terminal size: {termSize.columns}x{termSize.lines}')

str_ = ''

for i in range(min(image.shape[0], 500)):
    for j in range(min(image.shape[1], termSize.columns)):

        pix = image[i][j]
        hexCode = '#%02x%02x%02x' % (pix[2], pix[1], pix[0])

        str_ += f'[{hexCode}]O[/{hexCode}]'
    str_ += '\n'

os.system('clear')
console.print(str_)

