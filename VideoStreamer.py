import cv2
from threading import Thread


class VideoProcessor:
    """
    Combined class to continuously get frames from a VideoCapture object and show them.
    """

    def __init__(self, src, window_name, process_callback=None):
        self.src = src
        self.stream = cv2.VideoCapture(src)
        self.stopped = False
        self.frame = None
        self.prev_frame = None
        self.process_callback = process_callback
        self.window_name = window_name

    def start(self):
        Thread(target=self.get_frames, args=()).start()
        Thread(target=self.show_frames, args=()).start()

    def get_frames(self):
        while not self.stopped:
            (grabbed, frame) = self.stream.read()
            if not grabbed:
                self.stop()
                # Attempt to reconnect to the stream
                self.stream = cv2.VideoCapture(self.src)
            else:
                # Store the current frame as prev_frame before updating frame
                prev_frame = self.frame
                self.frame = frame
                if prev_frame is not None:
                    self.prev_frame = prev_frame

    def show_frames(self):
        while not self.stopped:
            if self.frame is not None:
                if self.process_callback:
                    frame = self.process_callback(self.frame, self.prev_frame)
                else:
                    frame = self.frame
                cv2.imshow(self.window_name, frame)
                if cv2.waitKey(1) == ord("q"):
                    self.stopped = True

    def stop(self):
        self.stopped = True
