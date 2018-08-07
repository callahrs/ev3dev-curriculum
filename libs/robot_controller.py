"""
  Library of EV3 robot functions that are useful in many different applications. For example things
  like arm_up, arm_down, driving around, or doing things with the Pixy camera.

  Add commands as needed to support the features you'd like to implement.  For organizational
  purposes try to only write methods into this library that are NOT specific to one tasks, but
  rather methods that would be useful regardless of the activity.  For example, don't make
  a connection to the remote control that sends the arm up if the ir remote control up button
  is pressed.  That's a specific input --> output task.  Maybe some other task would want to use
  the IR remote up button for something different.  Instead just make a method called arm_up that
  could be called.  That way it's a generic action that could be used in any task.
"""

import ev3dev.ev3 as ev3
import math
import time


class Snatch3r(object):

    def __int__(self):
        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.touch_sensor = ev3.TouchSensor()
        self.color_sensor = ev3.ColorSensor()
        self.ir_sensor = ev3.InfraredSensor()
        self.BeaconSeeker = ev3.BeaconSeeker()
        self.pixy = ev3.Sensor(driver_name="pixy-lego")
        assert self.pixy
        assert self.ir_sensor
        assert self.color_sensor
        assert self.arm_motor.connected
        assert self.left_motor.connected
        assert self.right_motor.connected
        assert self.touch_sensor.connected

    def drive_left_inches_forward(self, inches_to_drive, drive_speed_sp):
        self.left_motor.run_to_rel_pos(speed_sp=drive_speed_sp,
                                       position_sp=inches_to_drive * 360 / 4)
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()

    def drive_right_inches_forward(self, inches_to_drive, drive_speed_sp):
        self.right_motor.run_to_rel_pos(speed_sp=drive_speed_sp,
                                        position_sp=inches_to_drive * 360 / 4)
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()

    def drive_inches(self, inches_to_drive, drive_speed_sp):
        self.left_motor.run_to_rel_pos(speed_sp=drive_speed_sp,
                                       position_sp=inches_to_drive * 360 / 4)
        self.right_motor.run_to_rel_pos(speed_sp=drive_speed_sp,
                                        position_sp=inches_to_drive * 360 / 4)
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()

    def turn_forever(self, turn_speed):
        self.left_motor.run_forever(speed_sp=turn_speed)
        self.right_motor.run_forever(speed_sp=-turn_speed)

    def turn_degrees(self, degrees, turn_speed):
        motor_turns_deg = (440 / 90) * degrees
        self.left_motor.run_to_rel_pos(position_sp=motor_turns_deg,
                                       speed_sp=turn_speed)
        self.right_motor.run_to_rel_pos(position_sp=-motor_turns_deg,
                                        speed_sp=turn_speed)
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()

    def drive_time_forward(self, drive_time_sp, drive_speed_sp):
        self.left_motor.run_forever(speed_sp=drive_speed_sp)
        self.right_motor.run_forever(speed_sp=drive_speed_sp)
        time.sleep(drive_time_sp)
        self.left_motor.stop()
        self.right_motor.stop()
        ev3.Sound.beep().wait()

    def drive_both_forever(self, drive_speed_sp):
        self.left_motor.run_forever(speed_sp=drive_speed_sp)
        self.right_motor.run_forever(speed_sp=drive_speed_sp)

    def drive_left_forever(self, drive_speed_sp):
        self.left_motor.run_forever(speed_sp=drive_speed_sp)

    def drive_right_forever(self, drive_speed_sp):
        self.right_motor.run_forever(speed_sp=drive_speed_sp)

    def drive_both_stop(self):
        self.left_motor.stop()
        self.right_motor.stop()

    def drive_left_stop(self):
        self.left_motor.stop()

    def drive_right_stop(self):
        self.right_motor.stop()

    def arm_calibration(self):
        self.arm_motor.run_forever(speed_sp=900)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action="brake")

        arm_revolutions_for_full_range = 14.2
        self.arm_motor.run_to_rel_pos(
            position_sp=-arm_revolutions_for_full_range * 360, speed_sp=900)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()

        self.arm_motor.position = 0

    def arm_up(self):
        self.arm_motor.run_forever(speed_sp=900)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action="brake")
        ev3.Sound.beep().wait()

    def arm_down(self):
        self.arm_motor.run_to_abs_pos(position_sp=0, speed_sp=900)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()

    def loop_forever(self):
        self.running = True
        while self.running:
            time.sleep(0.1)

    def shutdown(self):
        self.left_motor.stop()
        self.right_motor.stop()
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
        print('Goodbye')
        ev3.Sound.speak('Goodbye')
        self.running = False

    def seek_beacon(self):
        forward_speed = 300
        turn_speed = 100
        while not self.touch_sensor.is_pressed:
            current_heading = self.BeaconSeeker.heading
            current_distance = self.BeaconSeeker.distance
            if current_distance == -128:
                print("IR Remote not found. Distance is -128")
                self.drive_both_stop()
            else:
                if math.fabs(current_heading) < 2:
                    print("On the right heading. Distance: ", current_distance)
                    if current_distance > 0:
                        self.drive_both_forever(forward_speed)
                    if current_distance == 0:
                        self.drive_both_stop()
                        return True
                elif math.fabs(current_heading) > 10:
                    print("Heading is too far off to fix: ", current_heading)
                elif current_heading < 0:
                    self.drive_both_stop()
                    self.turn_forever(-turn_speed)
                    time.sleep(.1)
                    self.drive_both_stop()
                    print("Adjusting heading: ", current_heading)
                elif current_heading > 0:
                    self.drive_both_stop()
                    self.turn_forever(turn_speed)
                    time.sleep(.2)
                    self.drive_both_stop()
                    print("Adjusting heading: ", current_heading)
                else:
                    print("Error in Code or No Heading")
            time.sleep(0.2)
        print("Abandon ship!")
        self.drive_both_stop()
        return False
