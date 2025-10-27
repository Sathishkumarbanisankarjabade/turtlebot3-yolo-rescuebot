import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import time
import os
from ultralytics import YOLO

# Libraries to listen to robot position
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener

class YoloNode(Node):
    def __init__(self):
        super().__init__('qr_scanner_node')
        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.listener_callback,
            10)
        self.br = CvBridge()
        
        # Load your model
        self.model = YOLO('/home/bani/tb3_ws/src/my_yolo_system/my_yolo_system/qr_best.pt')

        # Setup position listener
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        self.last_save_time = 0.0

        # ====================================================
        # NEW: DEFINE THE SPECIFIC FOLDER
        # This creates a folder named 'mission_evidence' in your Home
        # ====================================================
        home_path = os.path.expanduser("~")
        self.evidence_dir = os.path.join(home_path, "mission_evidence")
        
        # Create the folder if it doesn't exist
        if not os.path.exists(self.evidence_dir):
            os.makedirs(self.evidence_dir)
            self.get_logger().info(f"📂 Created new evidence folder at: {self.evidence_dir}")
        else:
            self.get_logger().info(f"📂 Saving data to existing folder: {self.evidence_dir}")

    def listener_callback(self, msg):
        frame = self.br.imgmsg_to_cv2(msg, "bgr8")
        results = self.model(frame)
        
        current_time = time.time()

        for result in results:
            for box in result.boxes:
                confidence = box.conf[0]
                
                # Only proceed if confident AND 5 seconds have passed
                if confidence > 0.6 and (current_time - self.last_save_time) > 5.0:
                    
                    # 1. Get Location
                    x_str, y_str = "0.00", "0.00"
                    try:
                        trans = self.tf_buffer.lookup_transform('map', 'base_footprint', rclpy.time.Time())
                        x_val = trans.transform.translation.x
                        y_val = trans.transform.translation.y
                        x_str = f"{x_val:.2f}"
                        y_str = f"{y_val:.2f}"
                    except TransformException:
                        pass 

                    location_text = f"X: {x_str}, Y: {y_str}"

                    # 2. LOG TO TERMINAL
                    self.get_logger().info(f"📸 SAVING EVIDENCE: QR found at [{location_text}]")

                    # 3. SAVE TO TEXT FILE (Inside the specific folder)
                    report_path = os.path.join(self.evidence_dir, "mission_report.txt")
                    with open(report_path, "a") as f:
                        f.write(f"CONFIRMED: QR Code found at {location_text} | Time: {time.ctime()}\n")

                    # 4. SAVE PHOTO EVIDENCE (Inside the specific folder)
                    filename = f"evidence_x{x_str}_y{y_str}.jpg"
                    full_image_path = os.path.join(self.evidence_dir, filename)
                    cv2.imwrite(full_image_path, frame)
                    
                    self.last_save_time = current_time

                    # Draw on screen
                    cv2.putText(frame, f"SAVED: {filename}", (10, 50), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        cv2.imshow("Scanner View", frame)
        cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)
    node = YoloNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
