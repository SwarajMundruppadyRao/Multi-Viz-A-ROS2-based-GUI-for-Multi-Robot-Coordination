import sys
import os
import rclpy
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QComboBox, QProgressBar,
                             QHBoxLayout, QSplitter, QFrame, QLineEdit, QPushButton, QGridLayout, QInputDialog, QTextEdit)
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QPixmap, QFont, QIcon, QImage
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan, Image
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge

class RobotMonitorUI(QWidget):
    def __init__(self):
        super().__init__()
        self.namespace = 'waffle_1'  # Default robot namespace

        # List of robot names
        self.robot_names = ["waffle_1", "waffle_2", "waffle_3", "waffle_4"]
        self.robot_batteries = {}

        # Initialize ROS node
        rclpy.init()
        self.node = rclpy.create_node('robot_monitor_ui')
        self.bridge = CvBridge()

        # Initialize the UI layout
        self.initUI()

        # Initialize ROS topics
        self.initialize_ros_topics()

        # Start the ROS timer
        self.start_ros_timer()

    def initUI(self):
        # Load icons (adjust the paths as necessary)
        self.icon_up = QIcon('up-arrow.png')
        self.icon_down = QIcon('down-arrow.png')
        self.icon_left = QIcon('left-arrow.png')
        self.icon_right = QIcon('right-arrow.png')
        self.icon_stop = QIcon('stop.png')

        # Main layout
        main_layout = QVBoxLayout(self)

        # Apply a beige gradient background
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #f5f5dc, stop: 0.5 #e3d5b5, stop: 1 #d2b48c
                );
                font-family: Arial;
                color: #000000;
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
                text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
                color: #000000;
            }
            QPushButton {
                background-color: #8b4513;
                color: #ffffff;
                font-size: 14px;
                font-weight: bold;
                border: 2px solid #ffffff;
                border-radius: 10px;
                padding: 10px 20px;
                box-shadow: 3px 3px 5px rgba(0, 0, 0, 0.3);
            }
            QPushButton:pressed {
                background-color: #5a2e0f;
                box-shadow: inset 2px 2px 5px rgba(0, 0, 0, 0.3);
            }
            QProgressBar {
                text-align: center;
                font-size: 12px;
                border: 1px solid #3d3d3d;
                border-radius: 5px;
                color: #000000;
            }
            QLineEdit, QTextEdit {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.5);
                color: #000000;
                padding: 5px;
                border-radius: 5px;
            }
            QComboBox {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.5);
                color: #000000;
                padding: 5px;
                border-radius: 5px;
            }
            QProgressBar::chunk {
                background-color: #8b4513;
            }
        """)

        # Create a vertical layout for the header
        header_layout = QVBoxLayout()

        # Create the "Multiviz" logo as a header
        title_label = QLabel("MULTIVIZ")
        title_label.setFont(QFont("Helvetica", 36, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            color: #8b4513;
            text-shadow: 4px 4px 6px #000000;
            letter-spacing: 2px;
        """)

        # Add the title label to the header layout
        header_layout.addWidget(title_label)

        # Create a horizontal layout for robot batteries
        robot_battery_layout = QHBoxLayout()
        for robot_name in self.robot_names:
            robot_battery_container = QVBoxLayout()
            robot_battery_label = QLabel(robot_name)
            robot_battery_label.setAlignment(Qt.AlignCenter)
            robot_battery_label.setFont(QFont("Arial", 12, QFont.Bold))
            robot_battery_bar = QProgressBar()
            robot_battery_bar.setRange(0, 100)
            robot_battery_bar.setValue(100)
            robot_battery_bar.setTextVisible(True)
            robot_battery_bar.setFixedWidth(100)
            # Store the battery bar in self.robot_batteries[robot_name] for updating later
            self.robot_batteries[robot_name] = robot_battery_bar
            # Add label and bar to container
            robot_battery_container.addWidget(robot_battery_label)
            robot_battery_container.addWidget(robot_battery_bar)
            # Add container to robot_battery_layout
            robot_battery_layout.addLayout(robot_battery_container)
        # Add robot battery layout to header layout
        header_layout.addLayout(robot_battery_layout)

        # Create the kill switch button
        self.kill_switch_button = QPushButton('Kill Switch')
        self.kill_switch_button.setFont(QFont("Arial", 20, QFont.Bold))
        self.kill_switch_button.setStyleSheet("""
            QPushButton {
                background-color: #8b0000;
                color: #ffffff;
                border: 2px solid #ffffff;
                border-radius: 15px;
                padding: 10px 20px;
                text-align: center;
                text-shadow: 2px 2px 4px #000;
            }
            QPushButton:pressed {
                background-color: #5a0000;
            }
        """)

        # Connect the button to the kill_switch method
        self.kill_switch_button.clicked.connect(self.kill_switch)

        # Add the kill switch button to the header layout
        header_layout.addWidget(self.kill_switch_button)

        # Add the header layout to the main layout
        main_layout.addLayout(header_layout)

        # Robot selection layout
        robot_selection_layout = QHBoxLayout()
        robot_label = QLabel("Select Robot:", self)
        robot_label.setFont(QFont("Arial", 12, QFont.Bold))
        robot_selection_layout.addWidget(robot_label)
        self.robot_dropdown = QComboBox(self)
        self.robot_dropdown.addItems(self.robot_names)
        self.robot_dropdown.currentTextChanged.connect(self.on_robot_selected)
        robot_selection_layout.addWidget(self.robot_dropdown)
        main_layout.addLayout(robot_selection_layout)

        # Data layout (contains the splitter)
        data_layout = QHBoxLayout()

        # Left pane for robot controls and info
        left_frame = QFrame(self)
        left_layout = QVBoxLayout(left_frame)

        headline_font = QFont("Arial", 12, QFont.Bold)

        # Command Velocity
        cmd_vel_label = QLabel("Command Velocity (cmd_vel):", self)
        cmd_vel_label.setFont(headline_font)
        left_layout.addWidget(cmd_vel_label)
        self.cmd_vel_value = QLineEdit(self)
        self.cmd_vel_value.setReadOnly(True)
        left_layout.addWidget(self.cmd_vel_value)

        # Odometry
        odom_label = QLabel("Odometry (odom):", self)
        odom_label.setFont(headline_font)
        left_layout.addWidget(odom_label)
        self.odom_value = QLineEdit(self)
        self.odom_value.setReadOnly(True)
        left_layout.addWidget(self.odom_value)

        # Teleoperation controls
        teleop_label = QLabel("Teleop Controls:", self)
        teleop_label.setFont(headline_font)
        left_layout.addWidget(teleop_label)
        teleop_grid = QGridLayout()

        # Teleop buttons
        self.btn_up = QPushButton('', self)
        self.btn_down = QPushButton('', self)
        self.btn_left = QPushButton('', self)
        self.btn_right = QPushButton('', self)
        self.btn_stop = QPushButton('', self)

        # Set the icons
        self.btn_up.setIcon(self.icon_up)
        self.btn_down.setIcon(self.icon_down)
        self.btn_left.setIcon(self.icon_left)
        self.btn_right.setIcon(self.icon_right)
        self.btn_stop.setIcon(self.icon_stop)

        # Set the icon sizes
        icon_size = 32
        self.btn_up.setIconSize(QSize(icon_size, icon_size))
        self.btn_down.setIconSize(QSize(icon_size, icon_size))
        self.btn_left.setIconSize(QSize(icon_size, icon_size))
        self.btn_right.setIconSize(QSize(icon_size, icon_size))
        self.btn_stop.setIconSize(QSize(icon_size, icon_size))

        # Connect buttons to movement functions
        self.btn_up.clicked.connect(self.move_forward)
        self.btn_down.clicked.connect(self.move_backward)
        self.btn_left.clicked.connect(self.turn_left)
        self.btn_right.clicked.connect(self.turn_right)
        self.btn_stop.clicked.connect(self.stop_robot)

        # Add buttons to grid layout
        teleop_grid.addWidget(self.btn_up, 0, 1)
        teleop_grid.addWidget(self.btn_left, 1, 0)
        teleop_grid.addWidget(self.btn_stop, 1, 1)
        teleop_grid.addWidget(self.btn_right, 1, 2)
        teleop_grid.addWidget(self.btn_down, 2, 1)

        left_layout.addLayout(teleop_grid)

        # Logs section
        logs_label = QLabel("Logs:", self)
        logs_label.setFont(headline_font)
        left_layout.addWidget(logs_label)
        self.logs_text_edit = QTextEdit(self)
        self.logs_text_edit.setReadOnly(True)
        left_layout.addWidget(self.logs_text_edit)

        # Waypoints
        waypoint_label = QLabel("Set Waypoints:", self)
        waypoint_label.setFont(headline_font)
        left_layout.addWidget(waypoint_label)

        self.btn_set_waypoint = QPushButton('Set Waypoint', self)
        self.btn_set_waypoint.clicked.connect(self.set_waypoint)
        left_layout.addWidget(self.btn_set_waypoint)

        left_layout.addStretch()  # Add stretch to fill space

        # Right pane for visual data
        right_frame = QFrame(self)
        right_layout = QVBoxLayout(right_frame)

        # Map View (Placeholder)
        map_label = QLabel("Map View (Simulated):", self)
        map_label.setFont(headline_font)
        right_layout.addWidget(map_label)
        self.map_view = QLabel(self)
        self.map_view.setPixmap(QPixmap(640, 240))
        self.map_view.setScaledContents(True)  # Make pixmap scale with label size
        right_layout.addWidget(self.map_view)

        # Image View (Camera)
        image_label = QLabel("Camera View:", self)
        image_label.setFont(headline_font)
        right_layout.addWidget(image_label)
        self.image_view = QLabel(self)
        self.image_view.setPixmap(QPixmap(640, 240))
        self.image_view.setScaledContents(True)
        right_layout.addWidget(self.image_view)

        # Laser scan data
        laser_label = QLabel("Laser Scan Data:", self)
        laser_label.setFont(headline_font)
        right_layout.addWidget(laser_label)
        self.laser_value = QLineEdit(self)
        self.laser_value.setReadOnly(True)
        right_layout.addWidget(self.laser_value)

        right_layout.addStretch()  # Add stretch to fill space

        # Create a splitter
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_frame)
        splitter.addWidget(right_frame)
        # Set stretch factors to control resizing behavior
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)

        # Add the splitter to the data layout
        data_layout.addWidget(splitter)
        main_layout.addLayout(data_layout)

        # Set window properties
        self.setLayout(main_layout)
        self.setWindowTitle('Multiviz - Robot Monitor and Control Interface')
        self.setGeometry(100, 100, 1280, 720)

        # Timer to update the battery level (simulated)
        self.battery_timer = QTimer()
        self.battery_timer.timeout.connect(self.update_battery)
        self.battery_timer.start(1000)  # Update every second

    def initialize_ros_topics(self):
        # Close existing subscriptions and publishers if they exist
        try:
            self.node.destroy_subscription(self.odom_sub)
            self.node.destroy_subscription(self.scan_sub)
            self.node.destroy_subscription(self.image_sub)
            self.node.destroy_publisher(self.cmd_vel_pub)
        except AttributeError:
            pass  # Subscriptions don't exist yet

        # Odometry subscriber
        self.odom_sub = self.node.create_subscription(
            Odometry,
            f'/{self.namespace}/odom',
            self.odom_callback,
            10)

        # Laser scan subscriber
        self.scan_sub = self.node.create_subscription(
            LaserScan,
            f'/{self.namespace}/scan',
            self.scan_callback,
            10)

        # Image subscriber
        self.image_sub = self.node.create_subscription(
            Image,
            f'/{self.namespace}/camera/image_raw',
            self.image_callback,
            10)

        # Cmd_vel publisher
        self.cmd_vel_pub = self.node.create_publisher(
            Twist,
            f'/{self.namespace}/cmd_vel',
            10)

    def start_ros_timer(self):
        # Timer to periodically call rclpy.spin_once
        self.ros_timer = QTimer()
        self.ros_timer.timeout.connect(self.spin_ros)
        self.ros_timer.start(50)  # Call every 50 milliseconds

    def spin_ros(self):
        # Process ROS events
        rclpy.spin_once(self.node, timeout_sec=0)

    # ROS Callbacks
    def odom_callback(self, msg):
        position = msg.pose.pose.position
        orientation = msg.pose.pose.orientation
        text = f"Position: x={position.x:.2f}, y={position.y:.2f}, z={position.z:.2f}\n" \
               f"Orientation: x={orientation.x:.2f}, y={orientation.y:.2f}, z={orientation.z:.2f}, w={orientation.w:.2f}"
        self.update_odom_ui(text)

    def scan_callback(self, msg):
        ranges = msg.ranges
        if len(ranges) >= 3:
            text = f"Distances: {ranges[0]:.2f}, {ranges[1]:.2f}, {ranges[2]:.2f}..."
        else:
            text = "Laser data unavailable"
        self.update_laser_ui(text)

    def image_callback(self, msg):
        # Convert ROS Image message to QPixmap
        pixmap = self.ros_image_to_qpixmap(msg)
        if pixmap:
            self.image_view.setPixmap(pixmap)

    def ros_image_to_qpixmap(self, msg):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
            height, width, channel = cv_image.shape
            bytes_per_line = 3 * width
            q_image = QImage(cv_image.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
            pixmap = QPixmap.fromImage(q_image)
            return pixmap
        except Exception as e:
            self.node.get_logger().error(f"Failed to convert image: {e}")
            return None

    # Methods to handle commands from GUI
    def publish_cmd_vel(self, linear, angular):
        twist = Twist()
        twist.linear.x = linear
        twist.angular.z = angular
        self.cmd_vel_pub.publish(twist)
        text = f"Linear: {linear}, Angular: {angular}"
        self.update_cmd_vel_ui(text)
        # Log the command
        self.logs_text_edit.append(f"{self.namespace} cmd_vel: {text}")

    def stop_robot(self):
        twist = Twist()
        self.cmd_vel_pub.publish(twist)
        self.update_cmd_vel_ui("Stopped")
        # Log the command
        self.logs_text_edit.append(f"{self.namespace} stopped")

    def kill_switch(self):
        self.node.get_logger().info("Kill switch activated!")
        self.stop_robot()
        try:
            self.node.destroy_publisher(self.cmd_vel_pub)
        except AttributeError:
            pass
        self.update_cmd_vel_ui("Robot stopped (Kill switch activated)")
        self.logs_text_edit.append("Kill switch activated!")

    def change_namespace(self, namespace):
        self.namespace = namespace
        self.initialize_ros_topics()
        self.logs_text_edit.append(f"Switched to {namespace}")

    def update_battery(self):
        # Simulate battery drain for all robots
        for robot_name in self.robot_names:
            battery_bar = self.robot_batteries[robot_name]
            current_value = battery_bar.value()
            new_value = max(0, current_value - 1)
            battery_bar.setValue(new_value)
            # Change battery bar color based on level
            if new_value < 30:
                battery_bar.setStyleSheet("""
                    QProgressBar::chunk {
                        background-color: red;
                    }
                """)
            else:
                battery_bar.setStyleSheet("""
                    QProgressBar::chunk {
                        background-color: green;
                    }
                """)

    def on_robot_selected(self, robot_name):
        self.change_namespace(robot_name)

    def move_forward(self):
        self.publish_cmd_vel(0.2, 0.0)
        self.logs_text_edit.append(f"{self.namespace} moving forward")

    def move_backward(self):
        self.publish_cmd_vel(-0.2, 0.0)
        self.logs_text_edit.append(f"{self.namespace} moving backward")

    def turn_left(self):
        self.publish_cmd_vel(0.0, 0.5)
        self.logs_text_edit.append(f"{self.namespace} turning left")

    def turn_right(self):
        self.publish_cmd_vel(0.0, -0.5)
        self.logs_text_edit.append(f"{self.namespace} turning right")

    def set_waypoint(self):
        waypoint, ok = QInputDialog.getText(self, 'Set Waypoint', 'Enter waypoint coordinates (x, y):')
        if ok:
            print(f"Waypoint set to: {waypoint}")
            self.cmd_vel_value.setText(f"Moving to waypoint: {waypoint}")
            self.logs_text_edit.append(f"{self.namespace} moving to waypoint: {waypoint}")
            # Implement waypoint navigation logic here

    # Slots to update UI
    def update_odom_ui(self, text):
        self.odom_value.setText(text)

    def update_laser_ui(self, text):
        self.laser_value.setText(text)

    def update_cmd_vel_ui(self, text):
        self.cmd_vel_value.setText(text)

    def closeEvent(self, event):
        # Clean up ROS resources
        self.node.destroy_node()
        rclpy.shutdown()
        event.accept()

def main(args=None):
    app = QApplication(sys.argv)
    ex = RobotMonitorUI()
    ex.show()

    ret = app.exec_()

    # Clean up
    sys.exit(ret)

if __name__ == '__main__':
    main()
