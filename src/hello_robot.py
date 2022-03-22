import os, sys, inspect, _thread, time
import re
sys.path.insert(1, os.path.abspath(".."))
import Leap
import boto3

sqs = boto3.client('sqs', region_name = 'us-east-2',
                    aws_access_key_id="AKIA3QP7SNLSF45B2CF2", 
                    aws_secret_access_key="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")

queue = sqs.get_queue_url(QueueName='LeapMotionQueue.fifo',
                            QueueOwnerAWSAccountId='791346834148')

class SampleListener(Leap.Listener):

    def on_connect(self, controller):
        print("Connected")

    def on_frame(self, controller):
        global frame
        frame = controller.frame()
        print("Frame id: %d, timestamp: %d, hands: %d, fingers: %d" % (
            frame.id, frame.timestamp, len(frame.hands), len(frame.fingers)))
        return frame

    # TODO: Write this method
    def gesture_changed(self,cur_frame):
        if len(frame.fingers) != len(cur_frame.fingers):
            return True
        elif len(frame.hands) != len(cur_frame.hands):
            return True
        else:
            return False
    

def main():
    controller = Leap.Controller()
    listener = SampleListener()

    controller.add_listener(listener) 
    frame = listener.on_frame(controller)
    # Keep this process running until Enter is pressed
    print("Press Enter to quit...")
    try:
        sys.stdin.readline()
        while True:
            # leap_data = ("Frame id: %d, timestamp: %d, hands: %d, fingers: %d" % (
            # frame.id, frame.timestamp, len(frame.hands), len(frame.fingers)))
            response = sqs.send_message(QueueUrl= queue['QueueUrl'], 
                                        MessageBody= frame, 
                                        MessageGroupId='testing_leap_data')
            print("Message send response : {} ".format(response))
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)

if __name__ == "__main__":
    main()