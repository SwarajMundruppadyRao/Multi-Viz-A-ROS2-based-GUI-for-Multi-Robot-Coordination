# Project Plan: Multi-Robot Coordination GUI Using Qt, ROS2, and Gazebo (3 Weeks)

## Project Overview
This project aims to develop a Graphical User Interface (GUI) using Qt that integrates with ROS2 and Gazebo for monitoring and controlling TurtleBot 3 robots in simulation. The focus will be on visualizing key topics like odometry, LiDAR scans, and camera feed, while also providing a **teleoperation (telop)** feature to manually control the robots using buttons in the GUI. Additionally, the GUI will have a kill switch for emergency robot shutdown. Given the 3-week timeline, the project will focus on essential functionality for multi-robot coordination in simulation.

## Key Features
1. **Odometry Visualization**:
   - Display real-time odometry data for each TurtleBot (position, orientation, velocity).
   - Visualize robot movement on a 2D map.

2. **LiDAR Scan (Laser Scan) Visualization**:
   - Display real-time LiDAR scan data from TurtleBot 3.
   - Visualize detected obstacles and surroundings.

3. **Camera Feed**:
   - Stream the camera feed from the TurtleBot’s onboard camera.
   - Display real-time video in the GUI.

4. **Kill Switch**:
   - Implement a kill switch to stop individual or all robots in an emergency.
   - Display the status (active/inactive) of each robot.

5. **Teleoperation (Telop) Control**:
   - Add buttons to the GUI to manually control the robots.
     - Forward, Backward, Turn Left, Turn Right, Stop.
   - Each button will send movement commands to the TurtleBot via ROS2 topics (e.g., `/cmd_vel` for velocity control).
   - Display the current status of the robot (e.g., moving forward, stopped).

6. **Multi-Robot Monitoring**:
   - Support real-time data visualization for multiple TurtleBot 3 robots in simulation.
   - Display essential data (odometry, LiDAR, camera) for each robot.

## How Teleoperation (Telop) Works (Layman’s Terms)

1. **Manual Control**: We will add simple control buttons to the GUI, like "Forward," "Backward," "Turn Left," "Turn Right," and "Stop." 
   - When a button is pressed, the GUI will send a signal (called a ROS2 message) to the TurtleBot, telling it to move in that direction.
   - This works through the `/cmd_vel` topic, which handles movement commands for the robot.

2. **Real-Time Response**: The robot will move according to the button presses. For example:
   - Pressing "Forward" sends a command to the robot to move forward.
   - Pressing "Turn Left" rotates the robot in place to the left.
   - The "Stop" button immediately stops the robot’s motion.
   
3. **Multiple Robots**: The GUI will include buttons for each robot if multiple TurtleBots are being controlled at once.

## Team Roles and Responsibilities
1. **Team Lead**:
   - Coordinate tasks and ensure the project meets the 3-week deadline.
   - Oversee the integration of ROS2 topics with the GUI and simulation.

2. **GUI Developer**:
   - Design and implement the Qt-based interface for odometry, LiDAR, camera, and teleoperation control.
   - Ensure the kill switch and teleoperation (telop) feature is integrated and operational.

3. **ROS2 Integration Specialist**:
   - Develop ROS2 nodes to subscribe to topics like `/odom`, `/scan`, and `/camera/rgb/image_raw`.
   - Implement teleoperation by publishing movement commands to the `/cmd_vel` topic based on button presses.

4. **Simulation Engineer**:
   - Set up and configure TurtleBot 3 in the Gazebo simulation.
   - Ensure the simulation environment provides accurate data for the GUI.

5. **System Tester**:
   - Test the end-to-end functionality of the GUI with the Gazebo simulation.
   - Debug any integration issues between ROS2, Gazebo, and the GUI.

## Development Timeline

### Week 1: Setup and Core Functionality
- **Requirements**: Identify key topics (odometry, LiDAR, camera, teleoperation) to be visualized.
- **Environment Setup**: Set up ROS2, Qt, and Gazebo with TurtleBot 3 in simulation.
- **GUI Design**: Create a basic interface layout for odometry, LiDAR, camera, and teleoperation controls.
- **ROS2 Nodes**: Develop basic ROS2 nodes to subscribe to `/odom`, `/scan`, `/camera/rgb/image_raw` and to publish to `/cmd_vel` for teleoperation.

### Week 2: Core Feature Integration
- **Odometry Visualization**: Implement real-time odometry data visualization in the GUI.
- **LiDAR Scan Visualization**: Display real-time LiDAR scan data and obstacle detection.
- **Camera Feed**: Stream and display the TurtleBot’s camera feed in the GUI.
- **Teleoperation (Telop)**: Implement button-based manual control (Forward, Backward, Turn Left, Turn Right, Stop) for the robots.
- **Multi-Robot Setup**: Test the GUI with multiple TurtleBot 3 robots in Gazebo.

### Week 3: Final Testing, Optimization, and Documentation
- **Testing**: Conduct thorough end-to-end testing with the Gazebo simulation.
- **Kill Switch**: Implement and test the kill switch for emergency stop functionality.
- **GUI Optimization**: Ensure the GUI runs smoothly and handles multiple robots.
- **Documentation**: Write clear instructions and documentation for the system.

## Challenges and Considerations
- **Real-Time Communication**: Ensure low-latency data visualization for odometry, LiDAR, and camera topics, and real-time teleoperation response.
- **Multi-Robot Coordination**: Make sure the GUI can handle and display data from multiple robots in the simulation environment, with independent controls for each.
- **Teleoperation Safety**: Ensure that teleoperation commands are safely handled and stop commands take priority in emergencies.

## Tools and Technologies
- **Qt**: For building the cross-platform GUI.
- **ROS2**: For handling communication between the simulation and the GUI.
- **Gazebo**: For simulating TurtleBot 3 robots and generating data for visualization.

## Collaborators

- **Aryan Mishra**  
- **Gautam Sreenarayanan Nair** - [GitHub Profile](https://github.com/gautamsrn)  
- **Sai Jagadeesh Muralikrishnan** - [GitHub Profile](https://github.com/cravotics)  
- **Suhas Nagaraj** - [GitHub Profile](https://github.com/suhasnagaraj99)  
- **Swaraj Mundruppady Rao** - [GitHub Profile](https://github.com/SwarajMundruppadyRao)  

