# Pulse Robot Automation


## Try Me
https://pescalette.github.io/pulse/src/index.html

## Installation
- Clone the repository to have access to the sample world

**Dependencies:**
- Download [Webots](https://cyberbotics.com/#download) to begin. (Make sure to add it to path)
- Download the python requirements:
```bash
$  pip  install  -r  requirements.txt
```

**Usage:**
Start by dragging in an initialization block and create a routine by dragging in more blocks to be run on the selected arm.
To begin using the created routine download the created python file into `pulse/webots/controllers/ARM_NAME/ARM_NAME.py`. Naming is important here, double check the arm selected in your init block is what you use to replace `ARM_NAME` with (The default arm is named `BlockArm`. Ensure that the name you select within the initialization block matches.). Open `ARM_NAME.wbt` in webots and run the controller script to run the created routine.

## Project Description  
Pulse is a project aimed at simplifying robot arm automation and enhancing human-machine interfaces (HMIs) through an open-source, block-based programming language. The mission is to make robot arm programming accessible to developers of all skill levels, enabling precise control for various industrial applications.

**Motivation:**
Robot automation is becoming increasingly important in industries such as manufacturing, healthcare, and logistics. However, programming robot arms can be complex and daunting. Pulse aims to bridge this gap by providing an intuitive interface that abstracts the complexities of robot arm control while offering advanced features for experts.

**Project Goals:**
- Develop a user-friendly, block-based interface for programming robot arms.
- Implement high-level abstractions for kinematic control, motion planning, feedback control, hardware interfacing, safety checking, and real-time execution.
- Provide tools for creating customizable HMIs to monitor and control robot arms.
- Ensure the language is open-source and accessible to the robotics community.

## Parsing, Interpretation, and Compilation

Pulse relates to the topics of parsing, interpretation, and compilation in several ways. The language employs a block-based interface, which requires parsing user inputs to generate executable code. The interpretation phase involves translating these blocks into high-level instructions for robot arm control, motion planning, and safety checks. Finally, compilation involves generating the necessary code to execute on the robot arm's hardware.

**Author:**
Parker Escalette
