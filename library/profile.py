from main import TerminalImage
import sys
import os
import time

from rich.prompt import Prompt
from rich.console import Console
console = Console()

class ProfileImage():

    def __init__(self, path, factor = 1, char = None):
        self.image_ = TerminalImage(path)
        if char: self.image_.char_ = char

        self.gray_image_ = self.image_.grayscale(orientation = 'HEIGHT', factor = factor).split('\n')
        self.color_image_ = self.image_.color(orientation = 'HEIGHT', details = False, factor = factor).split('\n')
        
        self.iwidth_ = len(self.gray_image_[0])
        self.iheight_ = len(self.gray_image_)

    # Comparison between images
    def comparison(self):
        for i in range(min(len(self.color_image_), len(self.gray_image_))):
            console.print(self.color_image_[i], self.gray_image_[i])

    # Draws a circle for the profile maker
    def draw_circle(self, radius, thickness = 0.4, hollow = False, xpos = 0, ypos = 0, grayscale = True):
        r_in, r_out = radius - thickness, radius + thickness
        str_, strt = '', 0
        y = radius
        while y >= - radius:
            x = - radius
            while x < r_out:
                value = (x ** 2) + (y ** 2)
                if hollow: condition = value >= (r_in ** 2) and value <= (r_out ** 2)
                else: condition = value <= (r_out ** 2)
                
                if condition and grayscale: str_ += self.gray_image_[(strt // 41) + ypos][(strt % 41) + xpos]
                elif condition: 
                    new_color_image = []
                    for c_image in self.color_image_:
                        new_color_image.append([c_image[i: i + 20] for i in range(0, len(c_image), 20)])              # Split into substrings of length 20

                    str_ += new_color_image[(strt // 41) + ypos][(strt % 41) + xpos]

                else: str_ += ' '

                strt += 1
                x += 0.5
            str_ += '\n'
            y -= 1
        return str_

    def draw_profile(self, pos, g_):
        os.system('clear')
        
        if g_: print(self.draw_circle(10, xpos = pos[0], ypos = pos[1]))
        else: console.print(self.draw_circle(10, xpos = pos[0], ypos = pos[1], grayscale = False))

    def select_profile(self, g_):

        cur_pos = [0, 0]                # x coordinate and y coordinate
        prev_pos = [0, 0]

        while True:
            if cur_pos != prev_pos: self.draw_profile(cur_pos, g_)
            prev_pos[0] = cur_pos[0]
            prev_pos[1] = cur_pos[1]

            command = Prompt.ask('[bold](Profile)[/bold]').split()
            if len(command) != 2: print('Invalid command')
            else: 
                if command[0] == 'RSHIFT':
                    if int(command[1]) < 1: print('Invalid number')
                    else: 
                        if cur_pos[0] + int(command[1]) > self.iwidth_ - 41: print('Too high')
                        else: cur_pos[0] += int(command[1])
                elif command[0] == 'LSHIFT':
                    if int(command[1]) < 1: print('Invalid number')
                    else: 
                        if cur_pos[0] - int(command[1]) < 0: print('Too high')
                        else: cur_pos[0] -= int(command[1])
                elif command[0] == 'DSHIFT':
                    if int(command[1]) < 1: print('Invalid number')
                    else:
                        if cur_pos[1] + int(command[1]) > self.iheight_ - 41: print('Too high')
                        else: cur_pos[1] += int(command[1])
                elif command[0] == 'USHIFT':
                    if int(command[1]) < 1: print('Invalid number')
                    else:
                        if cur_pos[1] - int(command[1]) < 0: print('Too high')
                        else: cur_pos[1] -= int(command[1])
                # elif command[0] == 'WRITE':
                    # with open('profile.txt', 'w') as write_file:
                        # write_file.write(self.draw_circle(10, xpos = cur_pos[0], ypos = cur_pos[1]))
                        # write_file.close()
                elif command[0] == 'QUIT': 
                    return self.draw_circle(10, xpos = cur_pos[0], ypos = cur_pos[1], grayscale = g_)
                    break
                else: print('Unrecognized Comman d')

            time.sleep(0.3)

if __name__ == '__main__':

    try:
        try: image = ProfileImage(f'/home/heisendelta/Pictures/{sys.argv[1]}', sys.argv[3])
        except IndexError: image = ProfileImage(f'/home/heisendelta/Pictures/{sys.argv[1]}')

        if sys.argv[2] == 'G': print(image.select_profile(True))
        elif sys.argv[2] == 'C': print(image.select_profile(False))
        else: exit()

    except IndexError: exit()
