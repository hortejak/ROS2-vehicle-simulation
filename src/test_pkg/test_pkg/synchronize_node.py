#!usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

class SynchronizeNode(Node):

    def __init__(self,period):
        super().__init__("SynchNode")
        self.counter = 0
        self.synchronize_publisher = self.create_publisher(Int32,"/synch_tic/seconds",10)
        self.create_timer(period,self.synchronize_cb)

    def synchronize_cb(self):

        #self.get_logger().info("Tick")
        msg = Int32()
        msg.data = self.counter
        self.synchronize_publisher.publish(msg)
        self.counter += 1

    
def main():

    rclpy.init()
    node = SynchronizeNode(1.0)
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()