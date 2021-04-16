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

video_ = cv2.VideoCapture('/home/heisendelta/Videos/dont_judge_me.mp4')


def render_image_color(image, orientation = ['HEIGHT', 'WIDTH'], factor = 1.0):

    start_time = time.time()

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


def get_frame(sec):

    video_.set(cv2.CAP_PROP_POS_MSEC, sec * 1000)
    has_frames, image = video_.read()

    if has_frames:

        os.system('clear')
        frame_image = render_image_color(image, orientation = 'WIDTH')
        console.print(frame_image)

    return has_frames

if __name__ == '__main__':

    sec = 10
    frame_rate = 1 / 20
    count = 1

    success = get_frame(sec)

    while success:

        try:
            count += 1
            sec += frame_rate
            sec = round(sec, 2)
            success = get_frame(sec)

        except KeyboardInterrupt: break
