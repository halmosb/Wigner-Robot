# Wigner-Robot

The goal of this project to establish a remote connection to the Keyestudio Raspberry Pi 4B Robot Car. The camera and the sensors of the robot are going to be sent to a server with a fast hardware and preferably with high performance GPU capacity. In the server the data are processed, and a decision is made for the next action. This is sent to the robot, where the action is performed.

To achieve this goal, a two-sided communication is needed between the server and the robot. To minimize latency, we use the UDP protocol, with different sentinels to be able to determine package loss.
