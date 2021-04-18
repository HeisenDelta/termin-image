import sys
import os
from dotenv import load_dotenv
from pathlib import Path
from rich.console import Console
console = Console()

from profile import ProfileImage, function_profile_api
from main import load_env_file

def function_details(det_file, env_path, mnl = True, x_offset = 0, y_offset = 0, color = 'True', factor = 1):

    PATH_, COLOR, FACTOR, ORIENT = load_env_file(env_path = env_path)

    image = ProfileImage(PATH_, float(FACTOR))
    if mnl: image_text = image.select_profile(False).split('\n')
    else:
        image_text = function_profile_api(env_path, x_offset, y_offset, False, COLOR = color, FACTOR = float(factor)).split('\n')


    # Operations

    details = []
    with open(det_file, 'r') as handle: 
        details = ['\t\t' + line_.replace('\n', '') for line_ in handle.readlines() if line_.strip()]

    if len(details) > len(image_text): details = details[:len(image_text)]          # Read only first few details if too many provided

    if len(details) <= (len(image_text) // 2) - 1: 
        details_ = []
        for detail in details: 
            details_.append(detail)
            details_.append('')
        details = details_[:len(details_) - 1]

    sps_length = (len(image_text) - len(details)) // 2

    ret_str = ''
    for j in range(sps_length): ret_str += image_text[j] + '\n'
    for i in range(sps_length, len(image_text) - sps_length):

        try: ret_str += image_text[i] + details[i - sps_length] + '\n'
        except IndexError: ret_str += image_text[i] + '\n'

    for k in range(len(image_text) - sps_length, len(image_text)): ret_str += image_text[k] + '\n'

    return ret_str

if __name__ == '__main__':
    os.system('clear')
    console.print(function_details(det_file = 'details.txt', env_path = 'PARAM.env'))
