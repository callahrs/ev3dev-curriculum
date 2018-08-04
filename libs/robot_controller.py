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
    """Commands for the Snatch3r robot that might be useful in many different programs."""

    def drive_left_inches_forward(self, inches_to_drive, drive_speed_sp):
        left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        left_motor.run_to_rel_pos(speed_sp=drive_speed_sp,
                                  position_sp=inches_to_drive * 360 / 4)
        left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()

    def drive_right_inches_forward(self, inches_to_drive, drive_speed_sp):
        right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        right_motor.run_to_rel_pos(speed_sp=drive_speed_sp,
                                   position_sp=inches_to_drive * 360 / 4)
        right_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()

    def drive_inches(self, inches_to_drive, drive_speed_sp):
        left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        left_motor.run_to_rel_pos(speed_sp=drive_speed_sp,
                                  position_sp=inches_to_drive * 360 / 4)
        right_motor.run_to_rel_pos(speed_sp=drive_speed_sp,
                                   position_sp=inches_to_drive * 360 / 4)
        left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        right_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()

    def turn_degrees(self, degrees, turn_speed):
        left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        motor_turns_deg = (440 / 90) * degrees
        left_motor.run_to_rel_pos(position_sp=motor_turns_deg,
                                  speed_sp=turn_speed)
        right_motor.run_to_rel_pos(position_sp=-motor_turns_deg,
                                   speed_sp=turn_speed)
        left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        right_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()

    def drive_time_forward(self, drive_time_sp, drive_speed_sp):
        left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        left_motor.run_forever(speed_sp=drive_speed_sp)
        right_motor.run_forever(speed_sp=drive_speed_sp)
        time.sleep(drive_time_sp)
        left_motor.stop()
        right_motor.stop()
        ev3.Sound.beep().wait()
