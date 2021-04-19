# Termin Image

![Issues](https://img.shields.io/github/issues/HeisenDelta/termin-image)
![License](https://img.shields.io/github/license/HeisenDelta/termin-image)

##  Description

Termin Image is an easy python library to render 2D images in the terminal in color and in grayscale.
Note: Color images will only work in the Linux, Mac and new Windows Terminal.

##  Libraries

Termin Image is built using Python 3x and all the external libraries listed below are required to render the images
* [OpenCV](https://opencv.org/)
* [Pillow](https://python-pillow.org/)
* [Rich](https://pypi.org/project/rich/)
* [Dotenv](https://pypi.org/project/python-dotenv/)
* [Flask](https://flask.palletsprojects.com/en/1.1.x/)
* [Numba](http://numba.pydata.org/) (Experimental

## Usage

To use the library, first clone into the repository
```shell
git clone https://github.com/HeisenDelta/termin-image.git
```

From here, you can import the Image class and create a new image.
```python
from library.main import TerminalImage

image = TerminalImage('PATH_TO_YOUR_IMAGE')
```

You can print grayscale images ...
```python
print(image.grayscale(orientation = 'HEIGHT'))
```
![alt_text_grayscale](images/git2.png "Grayscale image example")

Or images in color.
```python
from rich.console import Console
console = Console()

console.print(image.color(orientation = 'HEIGHT', details = False))
```
![alt_text_color](images/git1.png "Color image example")

You can even change the character used to print the images (for colored images)
```python
image.char_ = '%'
```

Or you can change the background character of the image (for colored images)
```python
image.backc_ = '#000000'
```

## Environment Variables

The environment variables define the image path, color, orientation, image name (optional) and scale factor (optional).
The path to the image file can be specified while running the python code from the terminal. (It is stored as a pathlib.Path class)
```shell
python3 main.py path_to_your_env_file
```

The format of the env file should be in this format. (Note: An example is given in the library folder)
```shell
PATH_ = path_to_your_image
ORIENTATION = WIDTH
COLOR = True
IMG_NAME = name_of_your_image
FACTOR = 1
```

* **PATH** - (required) specifies the path of the image directory.
* **ORIENTATION** - (required) 'WIDTH' or 'HEIGHT' specifies if the image scales to terminal width or height.
* **COLOR** - (required) Boolean value for if the image is colored or not
* **IMG_NAME** - Not required if PATH specifies the img name as well. Otherwise this will be appended to PATH
* **FACTOR** - Resizes the image width the scale factor (defaults to 1.0)

## API
As of now, api/app.py is Flask file that acts as a REST API for localhost. The syntax is listed below:

```shell
# Loads basic terminal image rendering (main.py)

http://127.0.0.1:5000/main/env?env_path={}
http://127.0.0.1:5000/main/mnl?img_path={}&color={}&factor={}&orient={}


# Loads profile image rendering (profile.py)

http://127.0.0.1:5000/profile/env?env_path={}
http://127.0.0.1:5000/profile/mnl?img_path={}&x={}&y={}&color={}&factor={}
```

| Parameter | Value                                                                                                   |
| --------- | ------------------------------------------------------------------------------------------------------- |
| env_path  | (class str) The path to your .env file                                                                  |
| img_path  | (class str) The path to your image file                                                                 |
| color     | (class bool) True for colored images, false for grayscale images                                        |
| factor    | (class float) The factor by which the image is scaled                                                   |
| orient    | ('HEIGHT', 'WIDTH') 'HEIGHT' for if the image is scaled by terminal height or 'WIDTH' by terminal width |
| x         | (class unsigned int) The x_offset by which the image is shifted to the right in the profile frame       |
| y         | (class unsigned int) The y_offset by which the image is shifted down in the profile frame               |
