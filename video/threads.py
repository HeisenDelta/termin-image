from datetime import datetime
from threading import Thread
import time
import argparse
import cv2
import os

from frames import render_image_color
from rich.console import Console
console = Console()

frame_rate = 30


class CountsPerSec:

    """ Class that tracks the number of occurrences ("counts") of an
    arbitrary event and returns the frequency in occurrences
    (counts) per second. The caller must increment the count.
    """

    def __init__(self):
        self._start_time = None
        self._num_occurrences = 0

    def start(self):
        self._start_time = datetime.now()
        return self

    def increment(self): self._num_occurrences += 1

    def countsPerSec(self):
        elapsed_time = (datetime.now() - self._start_time).total_seconds()
        return self._num_occurrences / elapsed_time


class VideoGet:

    """ Class that continuously gets frames from a VideoCapture object
    with a dedicated thread.
    """

    def __init__(self, src = 0):
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False

    def start(self):    
        Thread(target = self.get, args = (), daemon = True).start()
        return self

    def get(self):
        while not self.stopped:
            if not self.grabbed: self.stop()
            else: (self.grabbed, self.frame) = self.stream.read()

    def stop(self): self.stopped = True


class VideoShow:

    """ Class that continuously shows a frame using a dedicated thread. """

    def __init__(self, frame = None):
        self.frame = frame
        self.stopped = False
    
    def start(self):
        Thread(target = self.show, args = ()).start()
        return self

    def show(self):
        while not self.stopped:

            # cv2.imshow("Video", self.frame)

            console.print(render_image_color(self.frame, orientation = 'WIDTH'))
            time.sleep(1 / frame_rate)

            if cv2.waitKey(1) == ord("q"): self.stopped = True
            # if KeyboardInterrupt: self.stopped = True

    def stop(self): self.stopped = True


def put_iterations_per_sec(frame, iterations_per_sec):

    """ Add iterations per second text to lower-left corner of a frame. """

    cv2.putText(frame, "{:.0f} iterations/sec".format(iterations_per_sec), (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255))
    return frame


def thread_video_show(source = 0):

    """ Dedicated thread for showing video frames with VideoShow object.
    Main thread grabs video frames.
    """

    cap = cv2.VideoCapture(source)
    (grabbed, frame) = cap.read()
    video_shower = VideoShow(frame).start()
    cps = CountsPerSec().start()

    while True:
        (grabbed, frame) = cap.read()
        if not grabbed or video_shower.stopped:
            video_shower.stop()
            break

        frame = put_iterations_per_sec(frame, cps.countsPerSec())
        video_shower.frame = frame
        cps.increment()


def thread_both(source = 0):

    """ Dedicated thread for grabbing video frames with VideoGet object.
    Dedicated thread for showing video frames with VideoShow object.
    Main thread serves only to pass frames between VideoGet and
    VideoShow objects/threads.
    """

    video_getter = VideoGet(source).start()
    video_shower = VideoShow(video_getter.frame).start()
    cps = CountsPerSec().start()

    while True:
        if video_getter.stopped or video_shower.stopped:
            video_shower.stop()
            video_getter.stop()
            break

        frame = video_getter.frame
        # frame = put_iterations_per_sec(frame, cps.countsPerSec())
        video_shower.frame = frame
        cps.increment()

def no_threading(source = 0):

    """ Grab and show video frames without multithreading. """

    cap = cv2.VideoCapture(source)
    cps = CountsPerSec().start()

    while True:
        (grabbed, frame) = cap.read()
        if not grabbed or cv2.waitKey(1) == ord("q"): break

        # frame = put_iterations_per_sec(frame, cps.countsPerSec())
        # cv2.imshow("Video", frame)

        os.system('clear')
        console.print(render_image_color(frame, orientation = 'WIDTH'))

        cps.increment()

thread_both(source = '/home/heisendelta/Videos/dont_judge_me.mp4')
# no_threading(source = '/home/heisendelta/Videos/dont_judge_me.mp4')
