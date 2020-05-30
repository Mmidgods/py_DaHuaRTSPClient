#!/usr/bin/env python3

import av
import av.datasets
import sys
import time
import cv2
import numpy as np
import logging
import datetime
from multiprocessing import Pool

from dahua.GetRtspData import GetRtspData


streams = {
    'cam0': 'rtsp://admin:123456@192.168.2.101:554'
    # 'cam1': 'rtsp://admin:123456@192.168.2.104:554/cam/realmonitor?channel=1&subtype=0'
}
def save(stream):
    # name, url = stream[:2]
    url = 'rtsp://admin:123456@192.168.2.101:554'
    with GetRtspData(url)as sgg:
        for img, RTP_time, nalpayload in sgg.StartPlay():
            cv2.namedWindow('Video', cv2.WINDOW_GUI_NORMAL)
            cv2.imshow("Video", img)
            print(RTP_time)

def main():
    save(streams.items())
    # try :
    #     pool = Pool(len(streams))
    #     pool.map(save, streams.items())
    # except:

if __name__ == '__main__':
    main()
