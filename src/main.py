#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import time
from std_srvs.srv import Empty
x=0
y=0
z=0
yaw=0
#---------------------------------------------------------------------------
def poseCallback(pose_message):
    global x
    global y, z, yaw
    x= pose_message.x
    y= pose_message.y
    yaw = pose_message.theta
#---------------------------------------------------------------------------
def move(speed, distance):
        #declare a Twist message to send velocity commands
            velocity_message = Twist()
            #get current location 
            x0=x
            y0=y

            #assign the x coordinate of linear velocity to the speed. 
            velocity_message.linear.x = speed

            distance_moved = 0.0
            loop_rate = rospy.Rate(10) # we publish the velocity at 10 Hz (10 times a second)    
            cmd_vel_topic='/turtle1/cmd_vel'

            #create a publisher for the velocity message on the appropriate topic.
            velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)
            while True :
                    rospy.loginfo("Turtlesim moves forwards")

                    #publish the velocity message 
                    velocity_publisher.publish(velocity_message)
                    loop_rate.sleep()
                    
                    #rospy.Duration(1.0)
                    
                    distance_moved = distance_moved+abs(0.5 * math.sqrt(((x-x0) ** 2) + ((y-y0) ** 2)))
                    print  distance_moved               
                    if  not (distance_moved<distance):
                        rospy.loginfo("reached")
                        break
            
            #finally, stop the robot when the distance is moved
            velocity_message.linear.x =0
            velocity_publisher.publish(velocity_message)
#---------------------------------------------------------------------------
#--rotate--
from math import radians
def rotate():
    orig = yaw
    turn_cmd = Twist()
    turn_cmd.linear.x = 0.5
    turn_cmd.angular.z = radians(90)
    loop_rate = rospy.Rate(10) # we publish the velocity at 10 Hz (10 times a second)    
    cmd_vel_topic='/turtle1/cmd_vel'
    #create a publisher for the velocity message on the appropriate topic.
    velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)
    velocity_publisher.publish(turn_cmd)
    while yaw < orig+radians(90):
        continue
#--end rotate--
if __name__ == '__main__': # if main program
    try:
        
        rospy.init_node('turtlesim_motion_pose', anonymous=True)

        cmd_vel_topic='/turtle1/cmd_vel'
        velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)
        
        position_topic = "/turtle1/pose"
        pose_subscriber = rospy.Subscriber(position_topic, Pose, poseCallback) 

        time.sleep(2)
        print 'move: '
        move(0.5, 3.0)
        rotate()
        move(0.5, 3.0)
        rotate()
        move(0.5, 3.0)
        rotate()
        move(0.5, 3.0)
        time.sleep(5)
        print 'start reset: '
        rospy.wait_for_service('reset')
        reset_turtle = rospy.ServiceProxy('reset', Empty)
        reset_turtle()
        print 'end reset: '
        rospy.spin()
       
    except rospy.ROSInterruptException:
        rospy.loginfo("node terminated.")
