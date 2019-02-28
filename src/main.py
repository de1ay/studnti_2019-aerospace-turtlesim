#!/usr/bin/env python
import rospy
import time
import math
from math import radians
from turtlesim.msg import Pose
from std_srvs.srv import Empty
from geometry_msgs.msg import Twist


x = 0
y = 0
z = 0
angle = 0

def poseCallback(pose_message):
  global x
  global y, z, angle
  x= pose_message.x
  y= pose_message.y
  angle = pose_message.theta
    
def move():
  print "x: " + str(x) + "; y: " + str(y)

  x0 = x
  y0 = y

  velocity_message = Twist()
  velocity_message.linear.x = 0.5
  distance = 0.0

  loop_rate = rospy.Rate(10)   
  cmd_vel_topic='/turtle1/cmd_vel'

  velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)
  
  while distance < 3.0:
          velocity_publisher.publish(velocity_message)
          distance = math.sqrt(((x-x0) ** 2) + ((y-y0) ** 2))

  velocity_message.linear.x = 0
  velocity_publisher.publish(velocity_message)


def rotate():
  ANGLE_90 = radians(90)

  turn_cmd = Twist()
  turn_cmd.angular.z = 0.5

  loop_rate = rospy.Rate(10)   
  cmd_vel_topic='/turtle1/cmd_vel'

  rotation_velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)
  rotation_velocity_publisher.publish(turn_cmd)

  if angle == 0:
    while angle < ANGLE_90:
      rotation_velocity_publisher.publish(turn_cmd)
  elif angle > 1.5 and angle < 1.6:
    while angle > 0:
      rotation_velocity_publisher.publish(turn_cmd)
  elif angle > 3.1 or angle < -3.1:
    while angle < -ANGLE_90:
      rotation_velocity_publisher.publish(turn_cmd)
  else:
    while angle < 0:
      rotation_velocity_publisher.publish(turn_cmd)

  turn_cmd.angular.z = 0
  rotation_velocity_publisher.publish(turn_cmd)

if __name__ == '__main__': 
  rospy.init_node('turtlesim_motion_pose', anonymous=True)

  cmd_vel_topic='/turtle1/cmd_vel'
  velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)
  
  position_topic = "/turtle1/pose"
  pose_subscriber = rospy.Subscriber(position_topic, Pose, poseCallback) 

  time.sleep(2)
  move()
  rotate()
  move()
  rotate()
  move()
  rotate()
  move()
  rotate()
  print "x: " + str(x) + "; y: " + str(y)

  exit(0)
