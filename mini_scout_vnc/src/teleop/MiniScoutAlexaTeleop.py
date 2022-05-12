from geometry_msgs.msg import Twist

class MiniScoutAlexaTeleop:
    def __init__(self):
        self.twist = Twist()
    
    
    def motion(self, msg):
            twist = Twist()
            if msg["Intent"] == "MoveForward":
                twist.linear.x = 0.1
                twist.angular.z = 0
                # print("Moving Forward")
                return twist
            elif msg["Intent"] == "MoveBackward":
                twist.linear.x = -0.05
                twist.angular.z = 0
                # print("Moving Backwards")
                return twist
            elif msg["Intent"] == "Move":
                twist.linear.x = -0.1
                twist.angular.z = 0
                print("Moving")
                return twist
            elif msg["Intent"] == "RotateLeft":
                twist.linear.x = 0
                twist.angular.z = 0.4
                # print("Rotate Left")
                return twist
            elif msg["Intent"] == "RotateRight":
                twist.linear.x = 0
                twist.angular.z = -0.4
                # print("Rotate Right")
                return twist
            elif msg["Intent"] == "AMAZON.CancelIntent":
                twist.linear.x = 0
                twist.angular.z = 0
                # print("Stopping")
                return twist
            elif msg["Intent"] == "AMAZON.StopIntent":
                twist.linear.x = 0
                twist.angular.z = 0
                # print("Stopping")
                return twist
            else:
                twist.linear.x = 0
                twist.angular.z = 0
                return twist