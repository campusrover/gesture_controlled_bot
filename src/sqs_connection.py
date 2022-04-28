#!/usr/bin/env python

import boto3
import Credentials
import json

#import rospy

def sqs_connector():
    my_credentials = Credentials.Credentials()

    sqs = boto3.client('sqs', region_name = 'us-east-2',
                        aws_access_key_id=my_credentials.AWS_ACCESS_KEY_ID, 
                        aws_secret_access_key=my_credentials.SECRET_ACCESS_KEY)

    queue = sqs.get_queue_url(QueueName=my_credentials.LMQ_NAME,
                                QueueOwnerAWSAccountId=my_credentials.OWNER_ID)

    global queue_message

    #print("Press Enter to quit...")
    try:        
        while True:
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
                            WaitTimeSeconds=20
                        )

            recieve_response = json.dumps(recieve_response, indent = 4)
            recieve_response = json.loads(recieve_response)
            queue_message = json.dumps(recieve_response['Messages'][0]['Body'], indent = 4)
            queue_message = json.loads(queue_message)
            print(queue_message)
            
            reciept_handle = recieve_response['Messages'][0]['ReceiptHandle']
            sqs.delete_message(QueueUrl=my_credentials.LMQ_URL,
                            ReceiptHandle= reciept_handle)

    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    sqs_connector()
