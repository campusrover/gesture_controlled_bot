from geometry_msgs.msg import Twist

class MiniScoutAlexaTeleop:
    def __init__(self):
        self.twist = Twist()
    def motion(self,msg):
        twist = Twist()
        if msg["Intent"] == "MoveForward":
            twist.linear.x = 1
            twist.angular.z = 0
            return twist
        elif msg["Intent"] == "MoveBackward":
            twist.linear.x = -1
            twist.angular.z = 0
            return twist
        elif msg["Intent"] == "RotateLeft":
            twist.linear.x = 0
            twist.angular.z = -1
            return twist
        elif msg["Intent"] == "RotateRight":
            twist.linear.x = 0
            twist.angular.z = 1
            return twist
        elif msg["Intent"] == "AMAZON.StopIntent":
            twist.linear.x = 0
            twist.angular.z = 0
            return twist