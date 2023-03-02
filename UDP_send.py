import socket
import numpy as np
import cv2 as cv
import time

from UDPwebcam import UDPwebcam_sender

sender = UDPwebcam_sender()
sender.start()
input('press Enter to stop')
sender.stop()