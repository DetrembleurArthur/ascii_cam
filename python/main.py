import cv2
import time
import os, sys
import numpy as np


ratio = 0.1


def frame_to_ascii(frame, chars, output_dimensions):
    buffer = ""
    width, height = output_dimensions[0], output_dimensions[1]
    height -= 2 #les lignes de prompt
    actual_width = len(frame[0]) * 2 #un pixel = 2 chars
    actual_height = len(frame)
    ratio_x = width / actual_width
    ratio_y = height / actual_height
    #print(ratio_x, ratio_y)
    acc_height = 1
    for line in frame:
        line_temp_count = 0
        line_temp_count += int(ratio_y)
        acc_height += ratio_y - int(ratio_y)
        if acc_height >= 1:
            line_temp_count += 1
            acc_height -= 1
        if line_temp_count > 0:
            buff_line = ""
            acc_width = 0
            for pixel in line:
                char = f'{chars[pixel]} '
                acc_width += ratio_x - int(ratio_x)
                buff_line += char * int(ratio_x)
                if acc_width >= 1:
                    buff_line += char
                    acc_width -= 1
            buff_line += "\n"
            buffer += buff_line * line_temp_count
    return buffer

def process_to_ascii(vid, CHARS_V, output_dimensions, BORDER, ratio):
    ret, frame = vid.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    t_size = frame.shape
    frame=cv2.resize(frame,  (int(t_size[1]*ratio), int(t_size[0]*ratio)))
    frame = cv2.copyMakeBorder(frame, top=BORDER, bottom=BORDER, left=BORDER, right=BORDER,
        borderType=cv2.BORDER_CONSTANT,
        value=255)
    return frame_to_ascii(frame, CHARS_V, output_dimensions)

def stream(callback: callable, once=False):
    vid = cv2.VideoCapture(0)
    if vid.isOpened() == False:
        print("can not open camera")
        return
    print("start")
#134 78 286 89 2.13 1.14

    CHARS_V = np.array([' ' for _ in range(256)])

    def putchar(chars_v, i1, i2, char):
        chars_v[i1:i2] = char
    putchar(CHARS_V, 0, 40, ' ')
    putchar(CHARS_V, 80, 160, '.')
    putchar(CHARS_V, 160, 200, '+')
    putchar(CHARS_V, 200, 256, '#')

    BORDER = 2
    if not once:
        while True:
            buffer = process_to_ascii(vid, CHARS_V, os.get_terminal_size(), BORDER, ratio)
            if callback(buffer) == "STOP":
                break
    else:
        import time
        time.sleep(1.5)
        callback(process_to_ascii(vid, CHARS_V, os.get_terminal_size(), BORDER, ratio))
    
    vid.release()
    print("stop")


def terminal_cam(buffer):
    print(f"\033[0;0H{buffer}")

from datetime import datetime
def file_storage_cam(buffer):
    with open(f"{datetime.now()}.txt", "wt") as file:
        file.write(buffer)

if __name__ == "__main__":
    #stream(terminal_cam)
    stream(file_storage_cam, True)

