import sys
import os
from PIL import Image

# chars = '.:!*%$@&#SB'
chars = ',:;!=*%#$&0'
# chars = '.,-~:;=!*#$@'
# chars2 = "`^\",:;i!Il~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

image = Image.open(f'/home/heisendelta/Pictures/{sys.argv[1]}')
termSize = os.get_terminal_size()

w, h = image.size

# aspectRatio = h / w
# newWidth = termSize.columns
# newHeight = int(aspectRatio * newWidth * 0.55)
# image = image.resize((newWidth, int(newHeight))).convert('L')

aspectRatio = w / h
newHeight = termSize.lines
newWidth = int(aspectRatio * newHeight / 0.55)
image = image.resize((newWidth, int(newHeight))).convert('L')

pixels = image.getdata()

newPixels = ''.join([
    chars[pixel // 25] for pixel in pixels
])

asciiImage = [newPixels[index:index + newWidth] for index in range(0, len(newPixels), newWidth)]

os.system('clear')

print('\n'.join(asciiImage))
