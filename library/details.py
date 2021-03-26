import sys
import os
from profile import ProfileImage
from rich.console import Console
console = Console()

image = ProfileImage(f'/home/heisendelta/Pictures/{sys.argv[1]}')
image_text = image.select_profile(False).split('\n')

# Operations
oper = [
    '', '', '\t\tName: HeisenDelta', '',
    '\t\tAge: Unknown', '',
    '\t\tBirthplace: Vienna, Austria', '',
    '\t\tProficiencies: Python, Javascript, C++', ''
]
os.system('clear')

console.print(image_text[0])
for i in range(1, len(image_text) - 1):
    try: console.print(image_text[i] + oper[i - 1])
    except IndexError: console.print(image_text[i])
console.print(image_text[len(image_text) - 1])
