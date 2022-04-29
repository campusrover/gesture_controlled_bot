#!/usr/bin/env python
from math import pi
from geometry_msgs.msg import Twist

class MiniScoutLeapTeleop:
    def __init__(self):
        self.twist = Twist()
    
    def leap_teleop(self, queue_message):
        data = queue_message
        pitch_low_range = -0.5
        pitch_high_range = 0.5
        twist = Twist()

        numHands = data['Hand Data']["Number of hands"]
        pitch = data['Hand Data']['Pitch']
    
        # check if there is a circle gesture
        if "Gesture" in data:
            gesture = data['Gesture']
            if gesture['type'] == 'circle':
                if gesture['isClockwise'] == True:
                    print('Turning right!')
                    twist.linear.x = 0
                    twist.angular.z = 0.2
                    return twist
                else:
                    print('Turning left!')
                    twist.linear.x = 0
                    twist.angular.z = -0.2
                    return twist
        # if pitch is low, move forward
        elif pitch > pitch_low_range and pitch < pitch_low_range - 0.5:
            print('Driving forward!')
            twist.linear.x = 0.5
            twist.angular.z = 0
            return twist
        # if pitch is high, move backward
        elif pitch < pitch_high_range and pitch > pitch_high_range + 0.5:
            print('Driving backward!')
            twist.linear.x = -0.5
            twist.angular.z = 0
            return twist     
        else:
            twist.linear.x = 0
            twist.angular.z = 0
            return twist