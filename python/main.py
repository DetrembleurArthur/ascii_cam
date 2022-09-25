import cv2
import time
import os, sys
import numpy as np

def stream(callback: callable):
    vid = cv2.VideoCapture(0)
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
    putchar(CHARS_V, 0, 60, ' ')
    putchar(CHARS_V, 60, 120, '.')
    putchar(CHARS_V, 120, 200, '*')
    putchar(CHARS_V, 200, 256, '#')

    BORDER = 3
    while(True):
        ret, frame = vid.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        t_size = frame.shape
        frame=cv2.resize(frame,  (t_size[1]//10, t_size[0]//10))
        frame = cv2.copyMakeBorder(frame, top=BORDER, bottom=BORDER, left=BORDER, right=BORDER,
            borderType=cv2.BORDER_CONSTANT,
            value=255)
        buffer = stepper(frame, CHARS_V)
        callback(buffer)
    
    vid.release()
