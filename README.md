# RoboVision
## Object Tracking Using Computer Vision

This project involves the creation of a robot that navigates in the world and follows designated objects.
The computing platform used for this project is Raspberry Pi 3B. The robot model is made with 3D printed components. The other key components used in the project include:

* A USB camera
* Arduino NANO
* 4x TT D65 motor with 48:1 gear
* TA 6586 5A - 3-14VDC controller module
* 2x Power Bank 5V
* Connecting cables

## Project Overview

![](/assets/robot.jpg)

## Connection Schema

![](/assets/schema.png)

The program is written in Python. The GPIO pins of the Raspberry Pi are not used in the project. We control the motor controller with an Arduino microcontroller connected to the Raspberry Pi via a USB cable.
This enables easy control of the robot from a computer. The camera is connected to the Raspberry Pi using the USB interface. The power for the motors and their controller is supplied by one of the two used power banks. 
The Raspberry Pi, powering the Arduino and the camera via a USB connector, is powered by a separate Power Bank to ensure stable voltage for the microcomputer.

Communication between the Arduino and Raspberry Pi is one-sided and is realized using the Serial interface and the serial library for Python.
The form of the message sent by the Raspberry Pi is as follows: f'{left:.3f};{right:.3f}\n' where left and right are float values in the range <-1, 1> corresponding to the speed and direction of the corresponding track.

## Web Control Panel

![](/assets/webpanel.png)

The remote control panel with real-time camera preview allows us to view the target and take control of the robot and steer it using the keyboard. The REMOTE button is also an indicator of the current mode of operation of the robot: remote controlled/automatic [follow]. The panel also allows you to view information about the number of frames processed per second:

* fps camera - number of frames processed by the object tracking algorithm
* fps web - number of frames sent to the control panel

The server is implemented using the fastAPI and uvicorn libraries. The panel is available at raspberrypi.local:5000.

## Image Processing

The Open CV library is used for image processing and determining the position of the object. The tracking of object positions is based on the tracking of "blot" colors in the camera view.
The object is where we observe the largest cluster of desired color pixels. In a similar way, we determine the width of the object.
The project assumes a constant target size which allows us to estimate the approximate distance of the robot from the object.

## Contributors

This project was brought to life thanks to the combined efforts of:

* [Bartosz Słowik](https://github.com/Bartosz-Slowik) - Took charge of the 3D printing processes and the physical design of the robot.
* [Adrian Szlag](https://github.com/AdrianSzlag) - Led the development and programming efforts.

Project was made using slightly changed 3d-printing design from: https://www.thingiverse.com/thing:652851

We both thank the wider Open Source Community and everyone else who has indirectly contributed to this project. 
Your contributions to the libraries and tools we've used have made this project possible and have enriched its feature set significantly.

### Thank You, Happy Hacking!
