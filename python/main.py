import cv2
import time
import os, sys
import numpy as np

CAM_SIZE = 7

def stream(callback: callable):
    vid = cv2.VideoCapture(0)
    if vid.isOpened() == False:
        print("can not open camera")
        return
    print("start")

    def stepper(frame, chars):
        buffer = ""
        for line in frame:
            for pixel in line: 
                buffer += f'{chars[pixel]} '
            buffer += "\n"
        return buffer

    CHARS_V = np.array([' ' for _ in range(256)])

    def putchar(chars_v, i1, i2, char):
        chars_v[i1:i2] = char
    putchar(CHARS_V, 0, 40, ' ')
    putchar(CHARS_V, 40, 80, '.')
    putchar(CHARS_V, 80, 120, '°')
    putchar(CHARS_V, 120, 160, '*')
    putchar(CHARS_V, 160, 200, '0')
    putchar(CHARS_V, 200, 256, '#')

    BORDER = 3
    while(True):
        ret, frame = vid.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        t_size = frame.shape
        frame=cv2.resize(frame,  (t_size[1]//CAM_SIZE, t_size[0]//CAM_SIZE))
        frame = cv2.copyMakeBorder(frame, top=BORDER, bottom=BORDER, left=BORDER, right=BORDER,
            borderType=cv2.BORDER_CONSTANT,
            value=255)
        buffer = stepper(frame, CHARS_V)
        if callback(buffer) == "STOP":
            break
    
    vid.release()
    print("stop")


if __name__ == "__main__":
    stream(print)