#!/usr/bin/python2.7

import sys, os
sys.path.insert(1, os.path.abspath(".."))

import boto3
from credentials import Credentials
from MacOSLeap import Leap
from datetime import datetime
import time

my_credentials = Credentials.Credentials()

sqs = boto3.client('sqs', region_name = 'us-east-2',
                    aws_access_key_id=my_credentials.AWS_ACCESS_KEY_ID, 
                    aws_secret_access_key=my_credentials.SECRET_ACCESS_KEY)

queue = sqs.get_queue_url(QueueName=my_credentials.LMQ_NAME,
                            QueueOwnerAWSAccountId=my_credentials.OWNER_ID)

class LeapListener(Leap.Listener):

    def __init__(self):
        super(LeapListener, self).__init__()
        self.currMotion = 'Stop'

    def on_connect(self, controller):
        print("Connected")

    def on_frame(self, controller):

        frame = controller.frame()
        hand = frame.hands.rightmost
        position = hand.palm_position
        velocity = hand.palm_velocity
        direction = hand.direction
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
                            "Pitch": hand.direction.pitch,
                            "Time Hand Visible": time_visible
                            }
                        })
        for gesture in frame.gestures():
            if gesture.type is Leap.Gesture.TYPE_SWIPE:
                frame_output.update({"Gesture": {"type": "swipe"}})
            elif gesture.type is Leap.Gesture.TYPE_CIRCLE:
                circle = Leap.CircleGesture(gesture)
                isClockwise = False
                if (circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2):
                    isClockwise = True
                else:
                    isClockwise = False
                frame_output.update({"Gesture": {"type": "circle", "isClockwise": isClockwise}})

        frame_output.update({"Frame ID": int(frame.id)})
        frame_output.update({"Current Time": current_time.strftime("%H:%M:%S")})

        self.getMotion(frame_output)
        sqs_message = {'Time': frame_output['Current Time'], "Motion Input": "Leap", "Motion": self.currMotion}
    
        return sqs_message
        
    def getMotion(self, frame):
    
        pitch = frame['Hand Data']['Pitch']
        time_in_frame = frame['Hand Data']['Time Hand Visible']
        #print(pitch)
        #print(frame['Hand Data']['Grab Strength'])
        if time_in_frame > 2:
            # check if is a gesture
            if 'Gesture' in frame:
                #if frame['Gesture']['type'] == 'swipe':
                    #self.currMotion = 'Swipe'
                if frame['Gesture']['type'] == 'circle':
                    # circle is clockwise
                    if frame['Gesture']['isClockwise']:
                        self.currMotion = 'Turn right'
                    # circle is counterclockwise
                    else:
                        self.currMotion = 'Turn left'
            # if pitch is low, move forward
            elif pitch < 1 and pitch > 0.4:
                self.currMotion = 'Move forward'
            # if pitch is high, move backward
            elif pitch < -0.5:
                self.currMotion = 'Move backward'
            # grab strength is 1 (hand is fist), stop all movement
            elif frame['Hand Data']['Grab Strength'] > 0.75:
                self.currMotion = 'Stop'
        
    

def main():
    # Creates new Leap Controller
    controller = Leap.Controller()
    # Creates new Leap Listener
    listener = LeapListener()
    # Adds the listener to the controller
    controller.add_listener(listener)
    newMotion = listener.on_frame(controller)

    # Enabling Gestures
    controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE)
    controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)
    pastMotion = listener.currMotion

    #logging.basicConfig(filename='logs/sqs_response.log',level=logging.DEBUG)

    # Keep this process running until Enter is pressed
    print("Receiving Data From Leap Motion Controller")
    try:
        while True:
            queue_response = sqs.get_queue_attributes(QueueUrl = my_credentials.LMQ_URL,
                AttributeNames=['ApproximateNumberOfMessages'])
            num_of_messages = int(queue_response['Attributes']['ApproximateNumberOfMessages'])
            currMotion = listener.on_frame(controller)
                        # if num_of_messages == 0 and currMotion['Motion'] != pastMotion:
            if currMotion['Motion'] != pastMotion:
                print('past motion: %s'%pastMotion)
                # update motion if different from past motion
                pastMotion = currMotion['Motion']
                print('new motion: %s'%currMotion)
                # print(json.dumps(frame_output, indent = 4))
                # print
                response = sqs.send_message(QueueUrl= queue['QueueUrl'], 
                                            MessageBody=(str(currMotion)), 
                                            MessageGroupId='testing_leap_data')
                #logging.info(currMotion)
                time.sleep(2)
    except KeyboardInterrupt:
        pass
    finally:
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()