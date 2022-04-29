# Mini Scouter
Personal gesture and Alexa controlled robot

## Team
- Nazari Tuyo nazarituyo@brandeis.edu
- Helen Lin helenlin@brandeis.edu

## Project Introduction
Our final project is a mini scouter robot that can be controlled through hand gestures and voice commands. The robot uses a Leap Motion Controller to detect hand gestures and an Alexa to detect voice commands from the user. It then makes actions depedning on the commands it receives from either the Alexa (which takes priority; gestures are paused if a voice command is detected) or the Leap Motion Controller.

## Project Objective
The goal of our project was to create a robot that can be used by law enforcement or the military to navigate through before a human does. The robot will be able to take in commands through hand gestures or voice as a way to “scout out” an area.

## Implementation
### Local
- A connection is set up between the Leap Motion Controller and the computer via Leap’s Software in a local script
- AWS boto3 is used to connect to our SQS and push messages containing controller data to the queue in this script for VNC access
#### Challenges

### VNC






### What do you hope / expect to learn in doing this?

We hope to become more familiar with working with LIDAR and camera data since a lot of our project will be looking at scans and figuring out what they mean. Additionally, we will be using a LEAP motion sensor to detect hand motions. We expect to get fairly familiar with the LEAP ROS package and translating LEAP data to be used in our programs. Finally, we hope to get a better understanding of how a robot interacts with the environment/real world and any challenges that may come with that. 


### How would you like it to be evaluated?
- Accuracy with which the robot moves based off of the hand motion it detects
- Can detect obstacles around it and report them to the user
- Hand motion to action conversion as well as hand motion to LEAP node interpretation

##### Helen: I would like our project to be evaluated based on the accuracy of the information we are taking from the motion sensor and applying to the program. I would like our project to be evaluated on how well the robot executes an action based on the hand motion displayed. 

##### Nazari: I’d like to be evaluated on our approach towards resolving the issues that come up when trying to utilize the LEAP controller. Something that I feel is often overlooked during the implementation process for projects are the problems that come up along the way, and when they’re not tracked, it’s difficult to recall them. I think the a way I'd like to to be evaluated is through a written log.
