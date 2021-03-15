from main import TerminalImage
import sys
import os
from rich.console import Console
console = Console()

image = TerminalImage(f'/home/heisendelta/Pictures/{sys.argv[1]}')
os.system('clear')

# Comparison between images
def comparison(image_):
    color_image = image_.color(details = False, orientation = 'HEIGHT').split('\n')
    grayscale_image = image_.grayscale(orientation = 'HEIGHT').split('\n')

    for i in range(min(len(color_image), len(grayscale_image))):
        console.print(color_image[i], grayscale_image[i])

