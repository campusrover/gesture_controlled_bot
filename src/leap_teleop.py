#!/usr/bin/env python

import rospy
from leap_motion.msg import leap
from leap_motion.msg import leapros
from geometry_msgs.msg import Twist

teleop_topic = '/cmd_vel_mux/input/teleop'

low_speed = -0.5
stop_speed = 0
high_speed = 0.5
 
low_turn = -0.5
stop_turn = 0
high_turn = 0.5
 
pitch_low_range = -30
pitch_high_range = 30
 
roll_low_range = -150
roll_high_range = 150

def callback_ros(data): 
    msg = leapros()
    msg = data
     
    yaw = msg.ypr.x
    pitch = msg.ypr.y
    roll = msg.ypr.z

rospy.init_node('leap_teleop', anonymous=True) 
rospy.Subscriber("leapmotion/data", leapros, callback_ros)
pub = rospy.Publisher(teleop_topic, Twist, queue_size=1)

while not rospy.is_shutdown():

    twist = Twist()
    twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0 
    twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0

    if(pitch > pitch_low_range and pitch < pitch_low_range + 30):
        twist.linear.x = high_speed; twist.linear.y = 0; 
        twist.linear.z = 0   twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
