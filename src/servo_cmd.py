#!/usr/bin/env python
import rospy
import time
import math
from math import radians
from std_msgs.msg import Int32

if __name__ == '__main__': 
  rospy.init_node('servo_cmd_node', anonymous=True)

  servo_cmd_topic='/servo_cmd'
  angle_publisher = rospy.Publisher(servo_cmd_topic, Int32, queue_size=10)
  angle_publisher.publish(30)

  while True:
    angle = int(input())
    if angle == -1:
      break
    angle_publisher.publish(angle)

  exit(0)
