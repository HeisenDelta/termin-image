import os
import cv2
import sys
from PIL import Image
from rich.console import Console
console = Console()

class TerminalImage():

    def __init__(self, path):
        if path == None: raise NameError('Path not defined')
        self.path_ = path
        self.char_ = '0'
        self.backc_ = None

        self.color_ = None
        self.grayscale_ = None

    def grayscale(self, chars_ = ',:;!=*%#$&0', orientation = ['WIDTH', 'HEIGHT']):

        # chars = '.:!*%$@&#SB'

        if len(chars_) != 11: chars = ',:;!=*%#$&0'
        else: chars = chars_
        # chars = '.,-~:;=!*#$@'
        # chars2 = "`^\",:;i!Il~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

        try: 
            image = Image.open(self.path_)

            termSize = os.get_terminal_size()

            w, h = image.size

            if orientation == 'WIDTH':
                aspectRatio = h / w
                newWidth = termSize.columns
                newHeight = int(aspectRatio * newWidth * 0.55)
                image = image.resize((newWidth, int(newHeight))).convert('L')

            elif orientation == 'HEIGHT':
                aspectRatio = w / h
                newHeight = termSize.lines
                newWidth = int(aspectRatio * newHeight / 0.55)
                image = image.resize((newWidth, int(newHeight))).convert('L')

            pixels = image.getdata()

            newPixels = ''.join([
                chars[pixel // 25] for pixel in pixels
            ])

            asciiImage = [newPixels[index:index + newWidth] for index in range(0, len(newPixels), newWidth)]

            # os.system('clear')

            if '\n'.join(asciiImage): self.grayscale_ = '\n'.join(asciiImage)
            return '\n'.join(asciiImage)
    
        except FileNotFoundError: print(f'No file found with path: {self.path_}')


    def color(self, details = True, orientation = ['WIDTH', 'HEIGHT']):

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
            image = cv2.resize(image, (termSize.columns, round(termSize.columns * hbyw * 0.55)), interpolation = cv2.INTER_AREA)   # Scale with width
        elif orientation == 'HEIGHT':
            image = cv2.resize(image, (round(termSize.lines * wbyh / 0.55), termSize.lines), interpolation = cv2.INTER_AREA)       # Scale by height

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

        if str_: self.color_ = str_
        return str_


if __name__ == '__main__':

    # Defaults to Pictures directory of Linux
    imag = TerminalImage('/home/heisendelta/Pictures/' + sys.argv[1])
    
    os.system('clear')
    imag.char_ = '0'

    if sys.argv[2] == 'G': 
        if imag.grayscale(orientation = 'HEIGHT'): console.print(imag.grayscale(orientation = 'HEIGHT'))
    elif sys.argv[2] == 'C': 
        if imag.color(orientation = 'HEIGHT', details = False): 
            console.print(imag.color(orientation = 'HEIGHT', details = False))
