#!/usr/bin/env python

import boto3
import json
from teleop import MiniScoutLeapTeleop
from teleop import MiniScoutAlexaTeleop
from sqs import sqs_connector
import rospy
from credentials import Credentials
from geometry_msgs.msg import Twist

# scan = rospy.Subscriber('/scan', LaserScan, scan_cb)
cmd_vel = rospy.Publisher('cmd_vel', Twist, queue_size=1)
twist = Twist()
rospy.init_node('mini_scout')
rate = rospy.Rate(10)

alexa = MiniScoutAlexaTeleop.MiniScoutAlexaTeleop()
leap = MiniScoutLeapTeleop.MiniScoutLeapTeleop()
stop_teleop = Twist()
queue_connector = sqs_connector.SQSConnector()

# queue_connector.purge_sqs_queue()
# print("Purged Queue")

while not rospy.is_shutdown():
    message = queue_connector.get_sqs_message()
    if message["Motion Input"] == "Alexa":
        while message["Intent"] != AMAZON.StopIntent and queue_connector.getAlexa != False:
            teleop = alexa.motion(message)
            cmd_vel.publish(teleop)
            message = alexa.getAlexa()
        print("alexa exit")
    elif message["Motion Input"] == "Leap Controller":
        teleop = leap.leap_teleop(message)
        rate.sleep(1)
        cmd_vel.publish(teleop)
        print("leap")
    rate.sleep()

# queue_connector.purge_sqs_queue()
# print("Purged Queue")