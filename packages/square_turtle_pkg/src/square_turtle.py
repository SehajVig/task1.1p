#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist


class SquareTurtle:

    def __init__(self):
        rospy.init_node('square_turtle_timer_node')

        # Publisher
        self.pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)

        # Timer (calls function every 0.1 sec)
        self.timer = rospy.Timer(rospy.Duration(0.1), self.timer_callback)

        # State variables
        self.state = "move"   # "move" or "turn"
        self.start_time = rospy.Time.now().to_sec()
        self.side_count = 0

        rospy.loginfo("Drawing square using TIMER callback!")

        rospy.spin()

    def timer_callback(self, event):
        vel = Twist()

        current_time = rospy.Time.now().to_sec()
        elapsed = current_time - self.start_time

        # MOVE FORWARD
        if self.state == "move":
            vel.linear.x = 2.0
            vel.angular.z = 0.0

            if elapsed >= 2:   # move duration
                self.state = "turn"
                self.start_time = current_time

        # TURN 90 DEGREE
        elif self.state == "turn":
            vel.linear.x = 0.0
            vel.angular.z = 1.57

            if elapsed >= 1:   # turn duration
                self.state = "move"
                self.start_time = current_time
                self.side_count += 1

                # Optional: reset after full square
                if self.side_count >= 4:
                    self.side_count = 0

        self.pub.publish(vel)


if __name__ == '__main__':
    try:
        SquareTurtle()
    except rospy.ROSInterruptException:
        pass
