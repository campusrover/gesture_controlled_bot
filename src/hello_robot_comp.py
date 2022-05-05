import os, sys, inspect, _thread, time
import re
sys.path.insert(1, os.path.abspath(".."))
from MacOS import Leap
import boto3
from credentials import Credentials
from datetime import datetime
import json



my_credentials = Credentials.Credentials()

sqs = boto3.client('sqs', region_name = 'us-east-2',
                    aws_access_key_id=my_credentials.AWS_ACCESS_KEY_ID, 
                    aws_secret_access_key=my_credentials.SECRET_ACCESS_KEY)

queue = sqs.get_queue_url(QueueName=my_credentials.lmq_name,
                            QueueOwnerAWSAccountId=my_credentials.OWNER_ID)

class LeapListener(Leap.Listener):

    def on_connect(self, controller):
        print("Connected")

    def on_frame(self, controller):
        frame = controller.frame()
        hand = frame.hands.rightmost
        position = hand.palm_position
        velocity = hand.palm_velocity
        direction = hand.direction
        hand_side = "Left hand" if hand.is_left else "Right hand or no hand detected"
        time_visible = hand.time_visible
        current_time = datetime.now()
        
        frame_output = {}
        frame_output.update({
                            "Hand Data": { 
                            "Number of hands":len(frame.hands), 
                            "Fingers Visible":len(frame.fingers),
                            "Hand Position": {"x":position.x, "y":position.y, "z":position.z},
                            "Hand Velocity": {"x":velocity.x, "y":velocity.y, "z":velocity.z},
                            "Hand Direction":{"x":direction.x, "y":direction.y, "z":direction.z},
                            "Grab Strength": hand.grab_strength,
                            "Pinch Strength": hand.pinch_strength,
                            "Left or Right": hand_side,
                            "Time Hand Visible": time_visible
                            }
                        })
        for gesture in frame.gestures():
            if gesture.type is Leap.Gesture.TYPE_CIRCLE:
                circle = Leap.CircleGesture(gesture)
                frame_output.update({"Gesture Type": "circle"})
        frame_output.update({"Frame ID": int(frame.id)})
        frame_output.update({"Current Time":current_time.strftime("%H:%M:%S")})
    
        return frame_output
    

def main():
    controller = Leap.Controller()
    listener = LeapListener()
    controller.add_listener(listener) 
    frame_output = listener.on_frame(controller)

    # Enabling Gestures
    controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE)
    controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)



    # Keep this process running until Enter is pressed
    print("Press Enter to quit...")
    try:
        while True:
            frame_output = listener.on_frame(controller)
            # 
            if(frame_output['Frame ID'] % 10 == 0):
                print(json.dumps(frame_output, indent = 4))
                print
                response = sqs.send_message(QueueUrl= queue['QueueUrl'], 
                                        MessageBody=(str(frame_output)), 
                                        MessageGroupId='testing_leap_data')
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)

if __name__ == "__main__":
    main()