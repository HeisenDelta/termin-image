<h1>Termin Image</h1>

<div>
    <img src="https://img.shields.io/github/issues/HeisenDelta/termin-image" style="float:left;">
    <img src="https://img.shields.io/github/license/HeisenDelta/termin-image" style="float:left; margin-left: 10%;">
</div>

<h2>Description</h2>

<div>
    <div style="float: left; width: 50%;"><img src="images/git1.png"></div>
    <div style="float: left; width: 50%;"><img src="images/git2.png"></div>
</div><br>

<p>Termin Image is an easy python library to render 2D images in the terminal in color and in grayscale.</p>
<p>Note: Color images will only work in the Linux, Mac and new Windows Terminal,</p>

<h2>Libraries</h2>

<p>Termin Image is built using Python 3x and all the external libraries listed below are required to render the images</p>
<ul>
    <li><a href="https://opencv.org/">OpenCV</a></li>
    <li><a href="https://python-pillow.org/">Pillow</a></li>
    <li><a href="https://pypi.org/project/rich/">Rich</a></li>
</ul>

<h2>Usage</h2>

<p>To use the library, first clone into the repository</p>
<pre>
git clone https://github.com/HeisenDelta/termin-image.git
</pre>

<p>Import the Image class and create a new image.</p>
<pre>
from library.main import TerminalImage
from rich.console import Console
console = Console()

image = TerminalImage('PATH')
</pre>

<p>From here, you can print grayscale images ...</p>
<pre>
console.print(image.grayscale(orientation = 'HEIGHT'))
</pre>

<p>Or images in color.</p>
<pre>
console.print(image.color(orientation = 'HEIGHT', details = False))
</pre>

<p>You can even change the character used to print the images (for colored images)</p>
<pre>
image.char_ = '%'
</pre>

<p>Or you can change the background of the image (for colored images)</p>
<pre>
image.backc_ = '#000000'
</pre>
