import time
import math
import mqtt_remote_method_calls as com
import robot_controller as robo
import ev3dev.ev3 as ev3


class MyDelegate(object):

    def __init__(self):
        self.running = True
        self.count_done = 0

    def draw_star(self, radius, points, speed):
        robot = robo.Snatch3r()
        if points % 2 == 1:
            angle = points // 180
            print(angle)
            length_chord = 2 * radius * (math.sin(((180 - (2 * angle)) * (math.pi // 180)) // 2))
            print(angle)
            for k in range(points):
                robot.drive_inches_star(length_chord, speed)
                ev3.Sound.beep().wait()
                robot.turn_degrees((-1 * angle), speed)
                ev3.Sound.beep().wait()
                time.sleep(.2)
                self.count_done = self.count_done + 1
            self.running = False
        elif points % 2 == 0:
            turn_angle = 180
            turn_angle_inner = (360 // points)
            length_chord = radius
            for k in range(points):
                robot.drive_inches_star(length_chord, speed)
                ev3.Sound.beep().wait()
                robot.turn_degrees(turn_angle_inner, speed)
                ev3.Sound.beep().wait()
                robot.drive_inches_star(length_chord, speed)
                ev3.Sound.beep().wait()
                robot.turn_degrees(turn_angle, speed)
                ev3.Sound.beep().wait()
                self.count_done = self.count_done + 1
                time.sleep(.2)
            self.running = False


def main():
    my_delegate = MyDelegate()
    mqtt_client = com.MqttClient(my_delegate)
    my_delegate.mqtt_client = mqtt_client
    mqtt_client.connect_to_pc()
    robot = robo.Snatch3r()
    robot.arm_calibration()
    my_delegate.running = True
    while my_delegate.running is True:
        print("Sending " + str(my_delegate.count_done))
        mqtt_client.send_message("lines_done", [my_delegate.count_done])
        time.sleep(0.1)


main()
