import ev3dev.ev3 as ev3
import time
import math
import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com


class MyDelegate(object):

    def __init__(self):
        self.running = True
