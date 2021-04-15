import cv2
import os
import sys
import time
from PIL import Image
from rich.console import Console
console = Console()

try: 
    from ..library.main import TerminalImage

except (ModuleNotFoundError, ImportError):

    lib = os.path.dirname(os.getcwd()) + '/library'
    sys.path.insert(1, lib)

    from main import TerminalImage

vidcap = cv2.VideoCapture('/home/heisendelta/Videos/dont_judge_me.mp4')


def render_image_color(image, orientation = ['HEIGHT', 'WIDTH'], factor = 1.0):
    imgSize = (image.shape[1], image.shape[0])
    termSize = os.get_terminal_size()

    # Image resizing

    hbyw = imgSize[1] / imgSize[0]
    wbyh = imgSize[0] / imgSize[1]

    if orientation == 'WIDTH':
        image = cv2.resize(
            image, (int(termSize.columns * factor), round(termSize.columns * hbyw * 0.55 * factor)), 
            interpolation = cv2.INTER_AREA)   # Scale with width
    elif orientation == 'HEIGHT':
        image = cv2.resize(
            image, (round(termSize.lines * wbyh * factor / 0.55), int(termSize.lines * factor)),
            interpolation = cv2.INTER_AREA)       # Scale by height

    imgSize = (image.shape[1], image.shape[0])

    str_ = ''
    for i in range(min(imgSize[1], 500)):
        for j in range(min(imgSize[0], termSize.columns)):

            pix = image[i][j]
            hexCode = '#%02x%02x%02x' % (pix[2], pix[1], pix[0])
            
            str_ += f'[{hexCode}]0[/{hexCode}]'

        str_ += '\n'

    return str_


def render_image_grayscale(img, orientation = ['HEIGHT', 'WIDTH'], factor = 1.0):

    image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    chars = ',:;!=*%#$&0'
    termSize = os.get_terminal_size()

    w, h = image.size

    if orientation == 'WIDTH':
        aspect_ratio = h / w
        new_width = int(termSize.columns * factor)
        new_height = int(aspect_ratio * new_width * 0.55)
        image = image.resize((new_width, new_height)).convert('L')

    elif orientation == 'HEIGHT':
        aspect_ratio = w / h
        new_height = int(termSize.lines * factor)
        new_width = int(aspect_ratio * new_height / 0.55)
        image = image.resize((new_width, new_height)).convert('L')

    pixels = image.getdata()

    newPixels = ''.join([ chars[pixel // 25] for pixel in pixels ])

    asciiImage = [ newPixels[index:index + new_width] for index in range(0, len(newPixels), new_width) ]

    return '\n'.join(asciiImage)


def get_frame(sec):
    vidcap.set(cv2.CAP_PROP_POS_MSEC, sec * 1000)
    hasFrames, image = vidcap.read()
    if hasFrames:

        os.system('clear')
        print(render_image_grayscale(image, orientation = 'WIDTH'))

        # cv2.imwrite('image' + str(count) + '.jpg', image)
        # lib = os.path.dirname(os.getcwd()) + '/video/'

        # image_object = TerminalImage(lib + 'image' + str(count) + '.jpg')
        # console.print(image_object.color(details = False, factor = 1.0, orientation = 'WIDTH'))

        # time.sleep(1 / 20)

        # os.system('clear')
        # os.system('rm ' + 'image' + str(count) + '.jpg')

    return hasFrames

sec = 0
frame_rate = 1 / 20
count = 1
success = get_frame(sec)
while success:
    count += 1
    sec += frame_rate
    sec = round(sec, 2)
    success = get_frame(sec)
