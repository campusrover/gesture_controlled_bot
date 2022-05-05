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
    
    def get_sqs_message(self, queue_req):
        queue_name = ''
        queue_url = ''
        if queue_req == "alexa":
            queue_name = my_credentials.VCQ_NAME
            queue_url = my_credentials.VCQ_URL
        elif queue_req == "leap":
            queue_name = my_credentials.LMQ_NAME
            queue_url = my_credentials.LMQ_URL

        queue = sqs.get_queue_url(QueueName=queue_name,
                                    QueueOwnerAWSAccountId=my_credentials.OWNER_ID)

        global queue_message

        recieve_response = sqs.receive_message(
                        QueueUrl=queue_url,
                        AttributeNames=[
                            'All',
                        ],
                        MessageAttributeNames=[
                            'All',
                        ],
                        MaxNumberOfMessages=1,
                        VisibilityTimeout=15,
                        WaitTimeSeconds=20
                    )        
        # Converting string message from queue to dictionary
        queue_message = recieve_response['Messages'][0]['Body']
        json_converter = re.compile('(?<!\\\\)\'')
        queue_message = json_converter.sub('\"', queue_message)
        queue_message = ast.literal_eval(queue_message)
        
        # Deleting queue message
        reciept_handle = recieve_response['Messages'][0]['ReceiptHandle']
        sqs.delete_message(QueueUrl=queue_url,
                        ReceiptHandle= reciept_handle)

        return queue_message

    def has_message(self, queue_req):
        queue_url = ''
        if queue_req == "alexa":
            queue_url = my_credentials.VCQ_URL
        elif queue_req == "leap":
            queue_url = my_credentials.LMQ_URL

        queue_response = sqs.get_queue_attributes(
                QueueUrl=queue_url,
                AttributeNames=['ApproximateNumberOfMessages'])
        num_of_messages = int(queue_response['Attributes']['ApproximateNumberOfMessages'])
        if (num_of_messages > 0):
            print(queue_req + " queue has been checked and has " + (queue_response['Attributes']['ApproximateNumberOfMessages']) + " messages")
            return True
        else:
            print(queue_req + " queue has been checked and has " + (queue_response['Attributes']['ApproximateNumberOfMessages']) + " messages")
            return False
    
    def purge_sqs_queue(self, queue_req):
        queue_url = ''
        if queue_req == "alexa":
            queue_url = my_credentials.VCQ_URL
        elif queue_req == "leap":
            queue_url = my_credentials.LMQ_URL
        sqs.purge_queue(QueueUrl=queue_url)