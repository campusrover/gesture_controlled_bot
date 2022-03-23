import boto3
import Credentials

my_credentials = Credentials.Credentials()

sqs = boto3.client('sqs', region_name = 'us-east-2',
                    aws_access_key_id=my_credentials.AWS_ACCESS_KEY_ID, 
                    aws_secret_access_key=my_credentials.SECRET_ACCESS_KEY)

queue = sqs.get_queue_url(QueueName=my_credentials.LMQ_NAME,
                            QueueOwnerAWSAccountId=my_credentials.OWNER_ID)

def main():
    print("Press Enter to quit...")
    try:
        while True:
            response = sqs.receive_message(
                            QueueUrl=my_credentials.LMQ_URL,
                            AttributeNames=[
                                'All',
                            ],
                            MessageAttributeNames=[
                                'All',
                            ],
                            MaxNumberOfMessages=10,
                            VisibilityTimeout=30,
                            WaitTimeSeconds=10,
                            ReceiveRequestAttemptId='testing'
                        )
            print("Message recieve response : {} ".format(response))
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()