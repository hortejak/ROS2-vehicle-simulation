#!usr/bin/env python3
import rclpy
from rclpy.node import Node

from interfaces.msg import KinematicState, KinematicCommand

class AccelerationPControlNode(Node):

    def __init__(self):
        super().__init__("AccelerationPControlNode")
        self.v_ref = 10
        self.P = 10
        self.command_publisher = self.create_publisher(KinematicCommand,"/command/kinematic",10)
        self.create_subscription(KinematicState,'/state/kinematic',self.control_cb,10)

    def control_cb(self,msg:KinematicState):

        dv = self.v_ref - msg.v
        msg = KinematicCommand()
        msg.a = dv*self.P
        self.command_publisher.publish(msg)


    
def main():

    rclpy.init()
    node = AccelerationPControlNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()