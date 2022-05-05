#!/usr/bin/env python

import boto3
import json
from teleop import MiniScoutLeapTeleop
from teleop import MiniScoutAlexaTeleop
from sqs import sqs_connector
import rospy
import time
from credentials import Credentials
from geometry_msgs.msg import Twist

rospy.init_node('mini_scout')
rate = rospy.Rate(10)

cmd_vel = rospy.Publisher('cmd_vel', Twist, queue_size=1)
twist = Twist()

alexa = MiniScoutAlexaTeleop.MiniScoutAlexaTeleop()
leap = MiniScoutLeapTeleop.MiniScoutLeapTeleop()
stop_teleop = Twist()


stop_teleop.linear.x = 0
stop_teleop.angular.z = 0
cmd_vel.publish(stop_teleop)

follow_alexa = False
follow_leap = True

queue_connector = sqs_connector.SQSConnector()

queue_connector.purge_sqs_queue("alexa")
print("purged alexa queue")
queue_connector.purge_sqs_queue("leap")
print("purged leap queue")
# could add in timestamp so you don't purge more than once a minute



def follow_alexa(follow):
    while follow:
            print("waiting for alexa commands")
            if queue_connector.has_message('alexa'):
                time.sleep(0.5)
                msg = queue_connector.get_sqs_message('alexa')
                if msg['Intent'] == 'AMAZON.StopIntent':
                    cmd_vel.publish(alexa.motion(msg))
                    follow_alexa = False
                    print("Stopping Movement and Exiting")
                    return
                else:
                    cmd_vel.publish(stop_teleop)
                    while not queue_connector.has_message('alexa'):
                        cmd_vel.publish(alexa.motion(msg))
                        print("Published command")
    return

def follow_leap():
    while queue_connector.has_message('leap') or not queue_connector.has_message('alexa'):
        if queue_connector.has_message('leap'):
            msg = queue_connector.get_sqs_message('leap')
            cmd_vel.publish(leap.motion(msg))
    return

def main():
    # if message in alexa queue, check has_message until cancel or stop message recieved
    # 
    # if message in leap queue but listening to alexa, listen to alexa until cancel or stop
    # if listening to leap and message in leap queue, listen to leap queue
    # if listening to leap and message from alexa, stop robot, listen to alexa message until cancel or stop message
    while not rospy.is_shutdown():   
        if queue_connector.has_message('alexa'):
            if queue_connector.has_message('alexa'):
                # print('trying to get message')
                new_msg = queue_connector.get_sqs_message('alexa')
                msg = new_msg
                print("got message" + str(msg))
                if msg['Intent'] == 'AMAZON.StopIntent':
                    cmd_vel.publish(alexa.motion(msg))
                    follow_alexa = False
                    print("Stopping Movement and Exiting")
                    time.sleep(2)

                else: 
                    follow_alexa = True
                
                if follow_alexa == True:
                    cmd_vel.publish(stop_teleop)
                    time.sleep(2)
                    print("queue has msg: " + str(queue_connector.has_message('alexa')))
                    while not queue_connector.has_message('alexa'):
                        cmd_vel.publish(alexa.motion(msg))
                        print("Published command") 
            # if follow_alexa == True:
            #     print('follow alexa ' + str(follow_alexa))
            #     if queue_connector.has_message('alexa'):
            #         # print('trying to get message')
            #         new_msg = queue_connector.get_sqs_message('alexa')
            #         msg = new_msg
            #         # print("got message" + str(msg))
            #         if msg['Intent'] == 'AMAZON.StopIntent':
            #             cmd_vel.publish(alexa.motion(msg))
            #             time.sleep(1)
            #             follow_alexa = False
            #             print("Stopping Movement and Exiting")
            #         else:
            #             follow_alexa = True 
            #             cmd_vel.publish(stop_teleop)
            #             time.sleep(1)
            #             print(queue_connector.has_message('alexa'))
            #             while not queue_connector.has_message('alexa'):
            #                 cmd_vel.publish(alexa.motion(msg))
            #                 print("Published command")
        elif queue_connector.has_message('leap') and not queue_connector.has_message('alexa'):
            # new_msg = queue_connector.get_sqs_message('leap')
            # msg = new_msg
            # cmd_vel.publish(stop_teleop)
            # time.sleep(2.5)
            # print(queue_connector.has_message('leap'))
            # while not queue_connector.has_message('leap') or not queue_connector.has_message('alexa'):
            #     cmd_vel.publish(leap.motion(msg))
            #     print("Published command")
            # cmd_vel.publish(stop_teleop)
            if queue_connector.has_message('alexa'):
                follow_leap = False
            else:
                follow_leap = True

            if follow_leap == True:
                print('follow leap ' + str(follow_leap))
                if queue_connector.has_message('leap'):
                    # print('trying to get message')
                    new_msg = queue_connector.get_sqs_message('leap')
                    msg = new_msg
                    print("got message" + str(msg))
                    if queue_connector.has_message('alexa'):
                        cmd_vel.publish(stop_teleop)
                        follow_alexa = True
                        print("Stopping Movement and Exiting Leap")
                    else: 
                        cmd_vel.publish(stop_teleop)
                        print(queue_connector.has_message('leap'))
                        time.sleep(2)
                        while not queue_connector.has_message('leap'):
                            cmd_vel.publish(leap.motion(msg))
                            print("Published command")
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