# Mini Scouter
Personal gesture and Alexa controlled robot
Nazari Tuyo and Helen Lin

### mini_scouter

## Project Description
#### Most minimal version of the project, in a real ROS package
- Node that moves the robot forward and detects obstacles using lidar data
- A node that follows a stop/go command from the leap hand motion device

#### Write a one page description of your project. Include:
#### What is your final project, what do you want to demo on showcase day?
#### What do you hope / expect to learn in doing this?
#### How would you like it to be evaluated?
- Put your project as a repository in our Campus Rover Github organization and supply the URL here (?)

### What is your final project, what do you want to demo on showcase day?
Our final project is a seeing-eye dog robot that would follow a person around (possibly based on color to easily identify which object to follow) and identify obstacles near the person using Lidar and/or a camera. The current plan is to have the robot call out the obstacles to the user as it’s moving. In addition, we will include a hand gesture feature using the LEAP motion controller. We’ll be using the hand gestures to control the robot’s movement when it’s in the “hand motion control mode”

LEAP will accurately detect a hand, a fist as long as it’s not completely closed, holding up certain fingers. Specifically, some things we want the robot to recognize; for example, do we want to make it able to cross roads, detect stairs/ledges

Some possible hand gestures:
- Holding up a certain amount of fingers to do different actions
- One finger for left, two for right, five for stop, etc.
Enunciation:
- Obstacles of course, possibly doorways or openings that someone can enter, stairs, moving obstacles (?)
- When it is switching between “hand gesture mode” and “auto” mode


### What do you hope / expect to learn in doing this?

We hope to become more familiar with working with LIDAR and camera data since a lot of our project will be looking at scans and figuring out what they mean. Additionally, we will be using a LEAP motion sensor to detect hand motions. We expect to get fairly familiar with the LEAP ROS package and translating LEAP data to be used in our programs. Finally, we hope to get a better understanding of how a robot interacts with the environment/real world and any challenges that may come with that. 


### How would you like it to be evaluated?
-  The accuracy in which the robot can detect obstacles
- Hand motion to action conversion as well as hand motion to LEAP node interpretation

Our project hopes to provide a guide dog robot of sorts so an important evaluation point is that the robot is able to detect obstacles and be able to report those obstacles to the user. Additionally, the use of the LEAP motion sensor with hand gestures is another significant part of our project. 

##### Helen: I would like our project to be evaluated based on the accuracy of the information we are taking from the motion sensor and applying to the program. I would like our project to be evaluated on how well the robot executes an action based on the hand motion displayed. 

##### Nazari: I’d like to be evaluated on our approach towards resolving the issues that come up when trying to utilize the LEAP controller. Something that I feel is often overlooked during the implementation process for projects are the problems that come up along the way, and when they’re not tracked, it’s difficult to recall them. I think the a way I'd like to to be evaluated is through a written log.
