#!/usr/bin/env python3
import time
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
import rclpy

def main():
    rclpy.init()
    navigator = BasicNavigator()

    print("⏳ Waiting for Navigation...")
    navigator.waitUntilNav2Active()
    print("✅ System Ready! Starting SAFE 360° MISSION.")

    # =========================================
    # SAFE ROUTE (Away from walls)
    # =========================================
    goals = [
        # 1. Room 1 (Left) - Safe Spot
        [-1.5, -1.0, 0.0],
        
        # 2. Room 1 (Left) - Upper Safe Spot
        [-1.5, 1.0, 1.57],

        # 3. Center Hallway
        [0.0, 0.0, 0.0],

        # 4. Room 2 (Right) - Safe Spot
        [1.5, -1.0, 0.0],

        # 5. Room 2 (Right) - Upper Safe Spot
        [1.5, 1.0, 1.57],
        
        # 6. Finish at Home
        [0.0, 0.0, 0.0]
    ]

    for i, goal in enumerate(goals):
        x, y, w = goal
        print(f"🚀 Driving to Checkpoint {i+1} (x={x}, y={y})...")

        # --- 1. Go to the Spot ---
        goal_pose = PoseStamped()
        goal_pose.header.frame_id = 'map'
        goal_pose.header.stamp = navigator.get_clock().now().to_msg()
        goal_pose.pose.position.x = float(x)
        goal_pose.pose.position.y = float(y)
        goal_pose.pose.orientation.w = float(w)
        navigator.goToPose(goal_pose)

        while not navigator.isTaskComplete():
            pass

        # --- 2. THE 360 SPIN ---
        if navigator.getResult() == TaskResult.SUCCEEDED:
            print(f"✅ Arrived at {i+1}. SPINNINNG for QR Codes...")
            # Spin 6.28 radians (Full Circle)
            navigator.spin(spin_dist=6.28, time_allowance=15)
            
            while not navigator.isTaskComplete():
                pass
            print("👀 Spin Complete!")
        else:
            print(f"⚠️ Skipped Checkpoint {i+1} (Still too close to wall?)")

    print("🏁 Mission Complete!")
    rclpy.shutdown()

if __name__ == '__main__':
    main()
