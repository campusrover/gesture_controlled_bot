#!/usr/bin/env python
from math import pi
from geometry_msgs.msg import Twist

class MiniScoutLeapTeleop:
    def __init__(self):
        self.twist = Twist()

    def motion(self, queue_message):
        data = queue_message
        motion_mapping = {'Move forward': [0.5,0], 'Move backward': [-0.5,0],
            'Turn right': [0,0.5], 'Turn left': [0,-0.5], 'Stop': [0,0]}
        vel = motion_mapping[data['Motion']]
        self.twist.linear.x = vel[0]
        self.twist.angular.z = vel[1]
        return self.twist







