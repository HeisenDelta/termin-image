import cv2
import os
import sys
import time
from PIL import Image
from rich.console import Console
from numba import jit
console = Console()

try: 
    from ..library.main import TerminalImage

except (ModuleNotFoundError, ImportError):

    lib = os.path.dirname(os.getcwd()) + '/library'
    sys.path.insert(1, lib)

    from main import TerminalImage

video_ = cv2.VideoCapture('/home/heisendelta/Videos/dont_judge_me.mp4')
term_size = (os.get_terminal_size().columns, os.get_terminal_size().lines)
fps = 20

@jit(nopython = True)                                   # Function for getting the dimensions
def get_dim(factor, img_size, width):  

    hbyw = img_size[1] / img_size[0]
    wbyh = img_size[0] / img_size[1]

    if width: return (int(term_size[0] * factor), round(term_size[0] * hbyw * 0.55 * factor))
    else: return (round(term_size[1] * wbyh * factor / 0.55), int(term_size[1] * factor))


def render_image_color(image, orientation = ['HEIGHT', 'WIDTH'], factor = 1.0):

    imgSize = (image.shape[1], image.shape[0])

    if orientation == 'WIDTH':
        image = cv2.resize( image, get_dim(factor, imgSize, True), interpolation = cv2.INTER_AREA )         # Scale with width
    elif orientation == 'HEIGHT':
        image = cv2.resize( image, get_dim(factor, imgSize, False), interpolation = cv2.INTER_AREA )        # Scale by height

    imgSize = (image.shape[1], image.shape[0])

    str_ = ''
    for i in range(min(imgSize[1], 500)):
        for j in range(min(imgSize[0], term_size[0])):

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
    frame_rate = 1 / fps
    success = get_frame(sec)

    while success:

        try:
            sec += round(frame_rate, 2)
            start_time = time.time()

            success = get_frame(sec)

            with open('times.txt', 'a') as handle: handle.writelines(str(time.time() - start_time) + '\n')

        except KeyboardInterrupt: break
