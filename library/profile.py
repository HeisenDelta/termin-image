from main import TerminalImage
import sys
import os
import time

from rich.prompt import Prompt
from rich.console import Console
console = Console()

image = TerminalImage(f'/home/heisendelta/Pictures/{sys.argv[1]}')

grayscale_image = image.grayscale(orientation = 'HEIGHT').split('\n')
color_image = image.color(orientation = 'HEIGHT', details = False).split('\n')
image_width = len(grayscale_image[0])
image_height = len(grayscale_image)

# Comparison between images
def comparison(image_):
    color_image = image_.color(orientation = 'HEIGHT', details = False).split('\n')
    grayscale_image = image_.grayscale(orientation = 'HEIGHT').split('\n')

    for i in range(min(len(color_image), len(grayscale_image))):
        console.print(color_image[i], grayscale_image[i])

# Draws a circle for the profile maker
def draw_circle(radius, thickness = 0.4, hollow = False, xpos = 0, ypos = 0, grayscale = True):
    r_in, r_out = radius - thickness, radius + thickness
    str_, strt = '', 0
    y = radius
    while y >= - radius:
        x = - radius
        while x < r_out:
            value = (x ** 2) + (y ** 2)
            if hollow: condition = value >= (r_in ** 2) and value <= (r_out ** 2)
            else: condition = value <= (r_out ** 2)
            
            if condition and grayscale: str_ += grayscale_image[(strt // 41) + ypos][(strt % 41) + xpos]
            elif condition: 
                new_color_image = []
                for c_image in color_image:
                    new_color_image.append([c_image[i: i + 20] for i in range(0, len(c_image), 20)])              # Split into substrings of length 20

                str_ += new_color_image[(strt // 41) + ypos][(strt % 41) + xpos]

            else: str_ += ' '

            strt += 1
            x += 0.5
        str_ += '\n'
        y -= 1
    return str_

def draw_profile(pos, g_):
    os.system('clear')
    
    if g_: print(draw_circle(10, xpos = pos[0], ypos = pos[1]))
    else: console.print(draw_circle(10, xpos = pos[0], ypos = pos[1], grayscale = False))

cur_pos = [0, 0]                # x coordinate and y coordinate
prev_pos = [0, 0]

if sys.argv[2] == 'G': g_ = True
elif sys.argv[2] == 'C': g_ = False
else: exit()

while True:
    if cur_pos != prev_pos: draw_profile(cur_pos, g_)
    prev_pos[0] = cur_pos[0]
    prev_pos[1] = cur_pos[1]

    command = Prompt.ask('[bold](Profile)[/bold]').split()
    if len(command) != 2: print('Invalid command')
    else: 
        if command[0] == 'RSHIFT':
            if int(command[1]) < 1: print('Invalid number')
            else: 
                if cur_pos[0] + int(command[1]) > image_width - 41: print('Too high')
                else: cur_pos[0] += int(command[1])
        elif command[0] == 'LSHIFT':
            if int(command[1]) < 1: print('Invalid number')
            else: 
                if cur_pos[0] - int(command[1]) < 0: print('Too high')
                else: cur_pos[0] -= int(command[1])
        elif command[0] == 'DSHIFT':
            if int(command[1]) < 1: print('Invalid number')
            else:
                if cur_pos[1] + int(command[1]) > image_height - 41: print('Too high')
                else: cur_pos[1] += int(command[1])
        elif command[0] == 'USHIFT':
            if int(command[1]) < 1: print('Invalid number')
            else:
                if cur_pos[1] - int(command[1]) < 0: print('Too high')
                else: cur_pos[1] -= int(command[1])
        elif command[0] == 'WRITE':
            with open('profile.txt', 'w') as write_file:
                write_file.write(draw_circle(10, xpos = cur_pos[0], ypos = cur_pos[1]))
                write_file.close()
        elif command[0] == 'QUIT': break
        else: print('Unrecognized Command')

    time.sleep(0.3)
