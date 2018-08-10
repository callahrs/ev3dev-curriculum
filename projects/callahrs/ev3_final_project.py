import time
import math
import mqtt_remote_method_calls as com
import robot_controller as robo
import ev3dev.ev3 as ev3


class MyDelegate(object):

    def __init__(self):
        self.running = True
        self.mqtt_client = None
        self.count_done = 0

    def loop_forever(self):
        btn = ev3.Button()
        self.running = True
        while not btn.backspace and self.running:
            # Do nothing while waiting for commands
            time.sleep(0.01)
        self.mqtt_client.close()
        # Copied from robot.shutdown
        print("Goodbye")
        ev3.Sound.speak("Goodbye").wait()

    def draw_star(self, radius, points, speed):
        robot = robo.Snatch3r()
        if points % 2 == 0:
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
                self.mqtt_client.send_message("lines_done", [self.count_done])
                time.sleep(.2)
            self.count_done = 0
        else:
            angle = 180 // points
            print(angle)
            length_chord = 2 * radius * (math.sin(((180 - (2 * angle)) // 2)))
            print(length_chord)
            for k in range(points):
                robot.drive_inches_star(length_chord, speed)
                ev3.Sound.beep().wait()
                robot.turn_degrees((-1 * angle), speed)
                ev3.Sound.beep().wait()
                time.sleep(.2)
                self.count_done = self.count_done + 1
                self.mqtt_client.send_message("lines_done", [self.count_done])
            self.count_done = 0


def main():
    my_delegate = MyDelegate()
    mqtt_client = com.MqttClient(my_delegate)
    my_delegate.mqtt_client = mqtt_client
    mqtt_client.connect_to_pc()
    robot = robo.Snatch3r()
    robot.arm_calibration()
    my_delegate.loop_forever()


main()
