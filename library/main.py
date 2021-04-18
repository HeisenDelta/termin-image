import os
import cv2
import sys
from PIL import Image
from rich.console import Console
from dotenv import load_dotenv
from pathlib import Path
console = Console()

class TerminalImage():

    def __init__(self, path):
        if not path: raise NameError('Path not defined')
        self.path_ = path
        self.char_ = '0'
        self.backc_ = None

        self.color_ = None
        self.grayscale_ = None

    def grayscale(self, chars_ = ',:;!=*%#$&0', factor = 1, orientation = ['WIDTH', 'HEIGHT']):

        # chars = '.:!*%$@&#SB'
        # chars = '.,-~:;=!*#$@ '
        # chars2 = "`^\",:;i!Il~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

        if len(chars_) != 11: chars = ',:;!=*%#$&0'
        else: chars = chars_

        try: 
            image = Image.open(self.path_)

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

            # os.system('clear')

            if '\n'.join(asciiImage): self.grayscale_ = '\n'.join(asciiImage)
    
        except FileNotFoundError: print(f'File [{self.path_}] not found')

        return self.grayscale_

    def color(self, details = True, factor = 1.0, orientation = ['WIDTH', 'HEIGHT']):

        image = cv2.imread(self.path_, cv2.IMREAD_UNCHANGED)
        imgSize = (image.shape[1], image.shape[0])
        termSize = os.get_terminal_size()

        # os.system('clear')

        if details:
            print(f'Image size (unscaled): {imgSize[0]}x{imgSize[1]}')
            print(f'Terminal size: {termSize.columns}x{termSize.lines}')

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
        if details: print(f'Image size (scaled): {imgSize[0]}x{imgSize[1]}')

        str_ = ''
        for i in range(min(imgSize[1], 500)):
            for j in range(min(imgSize[0], termSize.columns)):

                pix = image[i][j]
                hexCode = '#%02x%02x%02x' % (pix[2], pix[1], pix[0])
                
                if self.backc_: str_ += f'[{hexCode} on {self.backc_}]{self.char_}[/{hexCode} on {self.backc_}]'
                else: str_ += f'[{hexCode}]{self.char_}[/{hexCode}]'

            str_ += '\n'

        self.color_ = str_
        return self.color_

def load_env_file(env_path):
    load_dotenv(dotenv_path = Path(env_path))
    PATH_ = os.getenv('PATH_')
    IMG_NAME = os.getenv('IMG_NAME')
    COLOR = os.getenv('COLOR')
    FACTOR = os.getenv('FACTOR')
    ORIENT_ = os.getenv('ORIENTATION')

    if not PATH_ and not IMG_NAME: raise FileNotFoundError('Path is not defined')
    if IMG_NAME: PATH_ += IMG_NAME
    
    return PATH_, COLOR, float(FACTOR), ORIENT_

def function_main(env_path):
    PATH_, COLOR, FACTOR, ORIENT = load_env_file(env_path = env_path)
    imag = TerminalImage(PATH_)

    if COLOR == 'True': return imag.color(orientation = ORIENT.upper(), details = False, factor = FACTOR)
    else: return imag.grayscale(orientation = ORIENT.upper(), factor = FACTOR)

def function_main_api(PATH_, COLOR, FACTOR, ORIENT):
    imag = TerminalImage(PATH_)

    if COLOR == 'True': return imag.color(orientation = ORIENT.upper(), details = False, factor = FACTOR)
    else: return imag.grayscale(orientation = ORIENT.upper(), factor = FACTOR)

if __name__ == '__main__':

    os.system('clear')
    console.print(function_main(env_path = sys.argv[1]))
