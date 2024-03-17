#!usr/bin/env python3
import rclpy
from rclpy.node import Node
import numpy as np

from interfaces.msg import KinematicState, KinematicCommand

class KinematicsBicycleNode(Node):

    def __init__(self):
        super().__init__("KinematicsBicycleNode")

        #constants
        self.lf = 2.791/2
        self.lr = 2.791/2
        self.a_max = 2.8935
        self.a_min = -3

        self.t = 0.1

        #states
        self.x = 0
        self.y = 0
        self.v = 0
        self.psi = 0

        #inputs
        self.a = 0
        self.df = 0
        self.dr = 0

        #simulation
        self.create_timer(self.t,self.update_states)
        self.state_publisher = self.create_publisher(KinematicState,'/state/kinematic',10)
        self.create_subscription(KinematicCommand,'/command/kinematic',self.command_cb,10)

    def command_cb(self,msg: KinematicCommand):

        self.a = np.clip(msg.a,self.a_min,self.a_max)
        self.df = msg.d

    def sideslip_angle(self,df,dr):

        argument = (self.lf*np.tan(dr) + self.lr*np.tan(df)) / (self.lf + self.lr)
        return np.arctan(argument)
    
    def update_states(self):

        beta = self.sideslip_angle(self.df,self.dr)

        dx = self.v*np.cos(self.psi+beta)
        dy = self.v*np.sin(self.psi+beta)
        dv = self.a
        dpsi = self.v*np.cos(beta)*np.tan(self.df)/(self.lf+self.lr)

        self.x = self.x + dx*self.t
        self.y = self.y + dy*self.t
        self.v = self.v + dv*self.t
        self.psi = self.psi + dpsi*self.t

        msg = KinematicState()
        msg.x = self.x
        msg.y = self.y
        msg.v = self.v
        msg.psi = self.psi

        self.state_publisher.publish(msg)
    
def main():

    rclpy.init()
    node = KinematicsBicycleNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()