# Mini Scouter
Personal gesture and Alexa controlled robot

## Team
- Nazari Tuyo nazarituyo@brandeis.edu
- Helen Lin helenlin@brandeis.edu

## Project Introduction
Our final project is a mini scouter robot that can be controlled through hand gestures and voice commands. The robot uses a Leap Motion Controller to detect hand gestures and an Alexa to detect voice commands from the user. It then makes actions depedning on the commands it receives from either the Alexa (which takes priority; gestures are paused if a voice command is detected) or the Leap Motion Controller.

## Project Objective
If humans can’t enter an area because of unforeseen danger, what could be used instead? We created MiniScouter to combat this problem. The goal of our project was to create a robot that can be used to navigate or “scout” out spaces with directions coming from the Leap Gesture Controller or voice commands supported by Alexa. The robot takes in commands through hand gestures or voice, and interprets them. Once interpreted, the robot preforms the action requested.

## Setup (g**uide on how to use the code)**

1. **Clone the Mini Scout repository (Be sure to switch to the correct branch based on your system)**
    1. [https://github.com/campusrover/mini_scouter](https://github.com/campusrover/mini_scouter.git)
2. **Install the Leap Motion Tracking SDK**
    1. Mac (V2): [https://developer-archive.leapmotion.com/v2](https://developer-archive.leapmotion.com/v2)
    2. Windows (Orion, SDK included): [https://developer.leapmotion.com/tracking-software-download](https://developer.leapmotion.com/tracking-software-download)
    
    ### **Mac OS Installation**
    
    1. Note: The MacOS software does not currently work with macOS Monterey, but there is a hack included below that does allow it to work
        
        [https://developer.leapmotion.com/tracking-software-download](https://developer.leapmotion.com/tracking-software-download)
        
    2. Once installed, open the Leap Motion application to ensure correct installation. 
        
        ![Imgur](https://i.imgur.com/WfrcbmN.png)
        
        A window will pop up with controller settings, and make sure the leap motion icon is present at the top of your screen.
        
    3. Plug your leap motion controller into your controller via a USB port.
        
        ![Imgur](https://i.imgur.com/7aKaFAL.png)
        
    4. From the icon dropdown menu, select visualizer. 
        
         ![Imgur](https://i.imgur.com/ZKnLImE.png)
        
        The window below should appear.
      
	 ![Imgur](https://i.imgur.com/XW60vjn.png)
        
    5. Note: If your MacOS software is an older version than Monterey, skip this step. Your visualizer should display the controller’s cameras on it’s own. 
        
        Restart your computer, leaving your Leap controller plugged in. Do not quit the Leap Application. (so it will open once computer is restarted)
        
    6. Once restarted, the computer will try to configure your controller. After that is complete, the cameras and any identifiable hand movement you make over the controller should appear.
    
    ### Windows Installation
    
    1. Note: the Leap Motion Controller V2 is not compatible with a certain update of Windows 10 so you’ll have to use the Orion version of the Leap software
    2. With V2, you can go into Program Files and either replace some of the .exe files or manually change some of the .exe files with a Hex editor
    3. However, this method still caused some problems on Windows (Visualizer could see hands but code could not detect any hand data) so it is recommended that Orion is used
        1. Orion is slightly worse than V2 at detecting hand motions (based off of comparing the accuracy of hand detection through the visualizer
    4. Orion is fairly simple to set up; once you install the file, you just run through the installation steps after opening the installation file
        1. Make sure to check off “Install SDK” when running through the installation steps
    5. After the installation is completed, open “UltraLeap Tracking Visualizer” on your computer to open the visualizer and make sure the Leap Motion Controller is connected
        
        The window below should look like this when holding your hands over the Leap Motion Controller:
        
        ![Imgur](https://i.imgur.com/0ZKc77a.png)
        

1. **AWS Setup**
    1. Create a AWS Account (if you have one already, skip this step)
    2. Create an SQS Queue in AWS
        1. Search for “Simple Queue Service”
        2. Click “Create Queue”
            
            ![Imgur](https://i.imgur.com/DMiuRRN.png)
            
        3. Give your queue a name, and select ‘FIFO’ as the type.
            
            ![Imgur](https://i.imgur.com/cPeZ0bl.png)
            
        4. Change “Content-based deduplication” so that its on. There is no need to change any of the other settings under “Configuration”
            
            ![Imgur](https://i.imgur.com/6NzGSSg.png)
            
        5. Click “Create Queue”. No further settings need to be changed for now.
            
            **This is the type of queue you will use for passing messages between your robot, the leap controller, alexa and any additional features you decide to incorporate from the project.**
            
        6.  **Creating your Access Policy**
            1. Click “Edit”
            2. Under “Access Policy”, select advanced, and then select “Policy Generator”
                
                ![Imgur](https://i.imgur.com/zlaPKAu.png)
                
            3.  This will take you to the AWS Policy Generator. The Access Policy you create will give your Leap software, Alexa Skill and robot access to the queue.
            4.  Add your account ID number, which can be found under your username back on the SQS page, and your queue ARN, which can also be found on the SQS page.
                
                ![Imgur](https://i.imgur.com/bOlwSAs.png)
                
                1. Select “Add Statement”, and then “Generate Policy” at the bottom. Copy this and paste it into the Access Policy box in your queue (should be in editing mode).
        7. Repeat step 1-5 once more, naming the queue separately for Alexa.
    3. Create an AWS access Key (Start at “****Managing access keys (console)”****)
        
        [https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html)
        
        Save the details of your AWS access key somewhere safe.
        
    4. Installing AWS CLI, boto3
        1. Follow the steps at the link below:
            
            [https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
            
        2. Once completed, downgrade your pip version with:
            
            `sudo easy_install pip==20.3.4`
            
            (this is needed since the LEAP portion of the project can only run on python2.7)
            
        3.  Run the following commands
            1. `pip install boto3`
            2. `pip freeze`
            3. check that `boto3` is actually there!
            4. `python -m pip install --user boto3`
2. **Adding your credentials to the project package**
    1. In your code editor, open the cloned gesture bot package
    2. navigate to the “credentials” folder
    3. using your saved **AWS Access Key** info, edit the fields 
        - Your “`OWNER_ID`” can be found in the top right hand corner of your aws console
        - “`lmq_name`” is the name of your queue + “`.fifo`”
            
             i.e. `leapmotionqueue.fifo`
            
    4. change the name of `Add_Credentials.py` to `Credentials.py`
    5. You will need to do this step with each credentials file in each package
        
        **IMPORTANT**
        
        UNDER NO CONDITION should this file be uploaded to github or anywhere else online, so after making your changes, run `nano .git/info/exclude` and add `Credentials.py`
        
        Please make sure that it is excluded by running `git status` and then making sure it’s listed under `Untracked files`
        
3. **Running the script**
    
    **Before running this script, please make sure you have Python2.7 installed and ready for use**
    
    1. navigate to the ‘`scripts`' folder and run ‘`python2.7 hello_robot_comp.py`'
    2. If everything is installed correctly you should see some output from the controller!
    3. to run the teleop script, run ‘`LeapGestureToSQS.py`’ while your controller is plugged in and set up!
4. **Using the Alexa Skill**
    1. This step is a bit more difficult. 
    2. Go to the Alexa Developer Console
        
        [https://developer.amazon.com/alexa/console/ask](https://developer.amazon.com/alexa/console/ask)
        
    3. Click “Create Skill”
        
        ![Imgur](https://i.imgur.com/FFQkJfT.png)
        
    4. Give your skill a **name**. Select **Custom Skill**. Select ‘Alexa-Hosted Python’ for the host.
    5. Once that builds, go to the ‘Code’ tab on the skill. Select **‘Import Code’,** and import the “VoiceControlAlexaSkill.zip” file from the repository, under the folder “**Alexa”**
        
        ![Imgur](https://i.imgur.com/AdfMqCo.png)
        
    6. Import all files.
    7. In Credentials.py, fill in your credentials, ensuring you have the correct name for your queue. 
        
        “`vcq_name`” is the name of your queue + “`.fifo`”
        
    8. Click ‘Deploy’
    9. Once Finished, navigate to the ‘Build’ tab. Open the `intents.txt` file from the repository’s ‘Skill’ folder (under the Alexa folder), and it’s time to build our intents. 
    10. Under invocation, give your skill a name. This is what you will say to activate it. We recommend **mini scout**! Be sure to save!
    11. Under intents, click ‘Add Intent’ and create the following 5 intents:
        1. Move
        2. MoveForward
        3. MoveBackward
        4. RotateLeft
        5. RotateRight
        
        ![Imgur](https://i.imgur.com/9s5j8tS.png)
        
    12. Edit each intent so that they have the same or similar “Utterances” as seen in the `intents.txt` file. Don’t forget to save!
    13. Your skill should be good to go! Test it in the Test tab with some of the commands, like “ask **mini scout** to move right”
5. **Using MiniScout in ROS**
    1. Clone the branch entitled vnc into your ROS environment
    2. install boto3 using similar steps as the ones above
    3. run `catkin_make`
    4. give execution permission to the file `MiniScoutMain.py`
    5. change each `Add_Credentials.py` file so that your AWS credentials are correct, and change the name of each file to `Credentials.py`
6. running hello robot!
    1. run the hello_robot_comp.py script on your computer
    2. run the hello_robot_vnc.py script on your robot

---

## Implementation
### Local
- A connection is set up between the Leap Motion Controller and the computer via Leap’s Software in a local script
- AWS boto3 is used to connect to our SQS and push messages containing controller data to the queue in this script for VNC access
- Alexa and a lambda function are set up in our AWS account

### VNC
- Takes in messages from both queues (Leap and Alexa)
- Interprets messages based on motion input
- Publishes results and starts robot movement 
- 
##### Helen: I would like our project to be evaluated based on the accuracy of the information we are taking from the motion sensor and applying to the program. I would like our project to be evaluated on how well the robot executes an action based on the hand motion displayed. 

##### Nazari: I’d like to be evaluated on our approach towards resolving the issues that come up when trying to utilize the LEAP controller. Something that I feel is often overlooked during the implementation process for projects are the problems that come up along the way, and when they’re not tracked, it’s difficult to recall them. I think the a way I'd like to to be evaluated is through a written log.
