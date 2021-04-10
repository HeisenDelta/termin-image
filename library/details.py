import sys
import os
from dotenv import load_dotenv
from pathlib import Path
from profile import ProfileImage
from rich.console import Console
console = Console()

load_dotenv(dotenv_path = Path(sys.argv[1]))
PATH_ = os.getenv('PATH_')
IMG_NAME = os.getenv('IMG_NAME')
FACTOR = os.getenv('FACTOR')

if not PATH_ and not IMG_NAME: raise FileNotFoundError('Path is not defined')
if IMG_NAME: PATH_ += IMG_NAME

image = ProfileImage(PATH_, float(FACTOR))
image_text = image.select_profile(False).split('\n')

# Operations

details = []
with open('details.txt', 'r') as handle: 
    details = ['\t\t' + line_.replace('\n', '') for line_ in handle.readlines()]

os.system('clear')

if len(details) > len(image_text): exit()                                                       # Currently exits if details exceed image text

if len(details) <= (len(image_text) // 2) - 1: 
    details_ = []
    for detail in details: 
        details_.append(detail)
        details_.append('')
    details = details_[:len(details_) - 1]

# Doesn't quite work ...  remember to fix later

sps_length = (len(image_text) - len(details)) // 2
for j in range(sps_length): console.print(image_text[j])

for i in range(sps_length, len(image_text) - sps_length):

    try: console.print(image_text[i] + details[i - sps_length])
    except IndexError: console.print(image_text[i])

for k in range(len(image_text) - sps_length, len(image_text)): console.print(image_text[k])
