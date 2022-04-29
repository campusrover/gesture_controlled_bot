#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
import boto3
import Credentials
import json
import re
import ast
#################
# cmd_vel setup #
#################
cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
rospy.init_node('vel_node')
move = Twist()
rate = rospy.Rate(10)

global my_credentials 
my_credentials = Credentials.Credentials()

global sqs 
sqs = boto3.client('sqs', region_name = 'us-east-2',
                        aws_access_key_id=my_credentials.AWS_ACCESS_KEY_ID, 
                        aws_secret_access_key=my_credentials.SECRET_ACCESS_KEY)

sqs.purge_queue(QueueUrl=my_credentials.LMQ_URL)
print("Purged Queue")

#################
# SQS Connector #
#################
def sqs_connector():

    queue = sqs.get_queue_url(QueueName=my_credentials.LMQ_NAME,
                                QueueOwnerAWSAccountId=my_credentials.OWNER_ID)

    global queue_message

    #print("Press Enter to quit...")
    recieve_response = sqs.receive_message(
                    QueueUrl=my_credentials.LMQ_URL,
                    AttributeNames=[
                        'All',
                    ],
                    MessageAttributeNames=[
                        'All',
                    ],
                    MaxNumberOfMessages=1,
                    VisibilityTimeout=15,
                    WaitTimeSeconds=1
                )

    # Converting string message from queue to dictionary
    queue_message = recieve_response['Messages'][0]['Body']
    json_converter = re.compile('(?<!\\\\)\'')
    queue_message = json_converter.sub('\"', queue_message)
    queue_message = ast.literal_eval(queue_message)
    
    # Deleting queue message
    reciept_handle = recieve_response['Messages'][0]['ReceiptHandle']
    sqs.delete_message(QueueUrl=my_credentials.LMQ_URL,
                    ReceiptHandle= reciept_handle)

    return queue_message
      

while not rospy.is_shutdown():
    data = sqs_connector()
    curr_hands = data['Hand Data']["Number of hands"]
    print(data)
    print
    if curr_hands == 1:
        print("One Hand Visible, moving forward")
        move.linear.x = 0.1
        move.angular.z = 0
        cmd_vel_pub.publish(move)
    elif curr_hands == 2:
        print("One Hand Visible, rotating")
        move.angular.z = 0.5
        move.linear.x = 0
        cmd_vel_pub.publish(move)
    elif curr_hands == 0:
        print("No Hand Visible, stopping movement")
        move.linear.x = 0
        move.angular.z = 0
        cmd_vel_pub.publish(move)



    rate.sleep()