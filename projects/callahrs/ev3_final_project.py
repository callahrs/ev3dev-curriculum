import ev3dev.ev3 as ev3
import time
import math
import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com
import robot_controller as robo


class MyDelegate(object):

    def __init__(self):
        self.running = True

    def draw_star(self, radius, points, speed):
        robot = robo.Snatch3r()
        if points % 2 == 1:
            angle = points // 180
            turn_angle = 360 - angle
            length_chord = 2 * radius * (math.sin(((180 - (2 * angle)) * (math.pi // 180)) // 2))
            for k in range(points):
                robot.drive_inches(length_chord, speed)
                robot.turn_degrees(turn_angle, speed)
        elif points % 2 == 0:
            turn_angle = 180
            turn_angle_inner = 360 - (360 // points)
            length_chord = radius
            for k in range(points):
                robot.drive_inches(length_chord, speed)
                robot.turn_degrees(turn_angle, speed)
                robot.drive_inches(length_chord, speed)
                robot.turn_degrees(turn_angle_inner, speed)
