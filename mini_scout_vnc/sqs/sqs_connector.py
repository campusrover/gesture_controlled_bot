#!/usr/bin/env python
import boto3
from credentials import Credentials
import json
import re
import ast

class SQSConnector():
    global my_credentials
    my_credentials = Credentials.Credentials()

    global sqs
    sqs = boto3.client('sqs', region_name = 'us-east-2',
                            aws_access_key_id=my_credentials.AWS_ACCESS_KEY_ID, 
                            aws_secret_access_key=my_credentials.SECRET_ACCESS_KEY)
    
    def get_sqs_message(self):

        queue = sqs.get_queue_url(QueueName=my_credentials.LMQ_NAME,
                                    QueueOwnerAWSAccountId=my_credentials.OWNER_ID)

        global queue_message

        recieve_response = sqs.receive_message(
                        QueueUrl=my_credentials.LMQ_URL,
                        AttributeNames=[
                            'All',
                        ],
                        MessageAttributeNames=[
                            'All',
                        ],
                        MaxNumberOfMessages=1,
                        # VisibilityTimeout=15,
                        # WaitTimeSeconds=20
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

    def get_alexa(self):
        message = get_sqs_message()
        if(message["Motion Input"] == "Alexa"):
            return message
        elif(message["Motion Input"] == "Leap Motion" and message['Hand Data']["Number of hands"] > 0):
            return False

    def purge_sqs_queue(self):
        sqs.purge_queue(QueueUrl=my_credentials.LMQ_URL)