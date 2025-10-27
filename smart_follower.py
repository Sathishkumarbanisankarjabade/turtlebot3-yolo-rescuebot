#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from apriltag_msgs.msg import AprilTagDetectionArray
from sensor_msgs.msg import LaserScan
import math

class TagCollector(Node):
    def __init__(self):
        super().__init__('tag_collector')
        
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.tag_sub = self.create_subscription(AprilTagDetectionArray, '/detections', self.tag_callback, 10)
        self.scan_sub = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        
        # --- SETTINGS ---
        self.stop_distance = 320.0     # Visual proximity (approx 0.15m)
        self.obstacle_dist = 0.45      # Obstacle avoidance threshold
        self.center_x = 320.0
        
        # --- MEMORY ---
        self.visited_tags = set()      # List of IDs we have already finished
        self.post_arrival_timer = 0    # Timer for backing up after arrival
        
        # --- SENSORS ---
        self.front_dist = 99.0
        self.left_dist = 99.0
        self.right_dist = 99.0
        self.tags_found = []

        self.get_logger().info('TAG COLLECTOR: Chase -> Visit -> Ignore -> Next!')

    def scan_callback(self, msg):
        # Zones
        front = msg.ranges[0:30] + msg.ranges[-30:]
        left = msg.ranges[30:90]
        right = msg.ranges[-90:-30]

        def get_min(r):
            v = [x for x in r if x > 0.1 and x < 10.0]
            return min(v) if len(v) > 0 else 99.0

        self.front_dist = get_min(front)
        self.left_dist = get_min(left)
        self.right_dist = get_min(right)

    def tag_callback(self, msg):
        self.tags_found = msg.detections
        self.logic_loop()

    def logic_loop(self):
        twist = Twist()

        # ---------------------------------------------------------
        # 1. POST-ARRIVAL MANEUVER (Back up & Turn away)
        # ---------------------------------------------------------
        # If we just finished a tag, we spend 30 cycles backing away
        if self.post_arrival_timer > 0:
            self.post_arrival_timer -= 1
            self.get_logger().info(f'Mission Complete! Leaving zone... ({self.post_arrival_timer})')
            twist.linear.x = -0.2  # Back up fast
            twist.angular.z = 1.0  # Turn around sharply
            self.publisher_.publish(twist)
            return

        # ---------------------------------------------------------
        # 2. FILTER TAGS (Ignore ones we already visited)
        # ---------------------------------------------------------
        # Only look at tags NOT in our memory set
        new_tags = [t for t in self.tags_found if t.id not in self.visited_tags]

        # ---------------------------------------------------------
        # 3. CHASE NEW TAGS
        # ---------------------------------------------------------
        if len(new_tags) > 0:
            # Pick largest *new* tag
            best_tag = max(new_tags, key=lambda t: math.sqrt((t.corners[1].x - t.corners[0].x)**2 + (t.corners[1].y - t.corners[0].y)**2))
            width = math.sqrt((best_tag.corners[1].x - best_tag.corners[0].x)**2 + (best_tag.corners[1].y - best_tag.corners[0].y)**2)
            
            # Are we there yet?
            if width < self.stop_distance and self.front_dist > 0.15:
                # Drive to it
                error_x = self.center_x - best_tag.centre.x
                twist.linear.x = 0.15
                twist.angular.z = 0.005 * error_x
                self.get_logger().info(f'Chasing Tag {best_tag.id}...')
            
            else:
                # WE ARRIVED!
                self.get_logger().info(f'>>> SUCCESS: Visited Tag {best_tag.id}! Adding to memory.')
                self.visited_tags.add(best_tag.id) # Mark as done
                self.post_arrival_timer = 40       # Trigger "Leave Zone" maneuver (40 cycles)
                twist.linear.x = 0.0
                twist.angular.z = 0.0

            self.publisher_.publish(twist)
            return

        # ---------------------------------------------------------
        # 4. OBSTACLE AVOIDANCE (If no new tag seen)
        # ---------------------------------------------------------
        if self.front_dist < self.obstacle_dist:
            self.get_logger().info('Obstacle ahead. Turning...')
            if self.left_dist > self.right_dist:
                twist.angular.z = 0.5
            else:
                twist.angular.z = -0.5
            twist.linear.x = 0.0
            self.publisher_.publish(twist)
            return

        # ---------------------------------------------------------
        # 5. WANDER / SEARCH
        # ---------------------------------------------------------
        self.get_logger().info(f'Searching... (Visited: {list(self.visited_tags)})')
        twist.linear.x = 0.15
        
        # Bias towards open space
        if self.left_dist > self.right_dist:
            twist.angular.z = 0.1
        else:
            twist.angular.z = -0.1

        self.publisher_.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = TagCollector()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
