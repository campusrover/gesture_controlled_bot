#!/usr/bin/env python

import boto3
import json
from teleop import MiniScoutAlexaTelep
from teleop import MiniScoutLeapTelep
from sqs import sqs_connector
import rospy
import time
from credentials import Credentials
from geometry_msgs.msg import Twist

rospy.init_node('mini_scout')
rate = rospy.Rate(10)

cmd_vel = rospy.Publisher('cmd_vel', Twist, queue_size=1)
twist = Twist()
# alexa and leap teleop teleop
alexa = MiniScoutAlexaTelep.MiniScoutAlexaTeleop()
leap = MiniScoutLeapTeleop.MiniScoutLeapTeleop()

# teleop message to stop the robot
stop_teleop = Twist()
stop_teleop.linear.x = 0
stop_teleop.angular.z = 0
cmd_vel.publish(stop_teleop)

# booleans for which queue will be in use
follow_alexa = False
follow_leap = True

# queue connection
queue_connector = sqs_connector.SQSConnector()

queue_connector.purge_sqs_queue("alexa")
print("purged alexa queue")
queue_connector.purge_sqs_queue("leap")
print("purged leap queue")

def main():
    # if message in alexa queue, check has_message until cancel or stop message recieved
    # if message in leap queue but listening to alexa, listen to alexa until cancel or stop
    # if listening to leap and message in leap queue, listen to leap queue
    # if listening to leap and message from alexa, stop robot, listen to alexa message until cancel or stop message
    
    while not rospy.is_shutdown():   
        # checking twice to ensure message has not been deleted
        if queue_connector.has_message('alexa'):
            if queue_connector.has_message('alexa'):
                # retreive message
                new_msg = queue_connector.get_sqs_message('alexa')
                # store it in a variable
                msg = new_msg
                # if message intent is to stop, stop robot and exit
                if msg['Intent'] == 'AMAZON.StopIntent':
                    cmd_vel.publish(alexa.motion(msg))
                    follow_alexa = False
                    print("Stopping Movement and Exiting")
                    time.sleep(2)
                else: 
                    follow_alexa = True
                
                # if following alexa, run a while loop that checks for new messages as the robot is moving
                if follow_alexa == True:
                    cmd_vel.publish(stop_teleop)
                    time.sleep(2)
                    print("Queue has msg: " + str(queue_connector.has_message('alexa')))
                    while not queue_connector.has_message('alexa'):
                        cmd_vel.publish(alexa.motion(msg))
                        print("Published command") 
        elif queue_connector.has_message('leap') and not queue_connector.has_message('alexa'):
            # if there is a message in the alexa queue, exit
            if queue_connector.has_message('alexa'):
                follow_leap = False
            else:
                follow_leap = True
            # check leap queue, then proceed similarly to alexa
            if follow_leap == True:
                if queue_connector.has_message('leap'):
                    new_msg = queue_connector.get_sqs_message('leap')
                    msg = new_msg
                    if queue_connector.has_message('alexa'):
                        cmd_vel.publish(stop_teleop)
                        follow_alexa = True
                        print("Stopping Movement and Exiting Leap")
                    else: 
                        cmd_vel.publish(stop_teleop)
                        time.sleep(2)
                        while not queue_connector.has_message('leap'):
                            cmd_vel.publish(leap.motion(msg))
                            print("Published command")
        # a final conditional in the case that both queues were empty
        else:
            if queue_connector.has_message('alexa'):
                follow_alexa = True
                follow_leap = False
            elif queue_connector.has_message('leap'):
                follow_leap = True
        rate.sleep()

    rospy.spin()

if __name__ == '__main__':
    main()