# Wifi-Ray-Tracing-Simulation

The goal of this project is to calculate the power received by a receiver connected to a Wifi station inside a building. The program makes it possible to visualize this captured power in a 2-dimensional representation of the building, as well as to determine the coverage area of the Wifi base station.

To this end, the interior of the building has been discretized and the program (developed in Python) sums for each point the contributions of all the electromagnetic waves passing through it. Only the direct rays, transmitted or reflected by the walls were taken into account. Diffraction has been neglected.

The first part of the report 'Project_ray_tracing.pdf' will present the theoretical models used to describe the physical phenomena present in this problem. The second part will give explanations on the algorithms used. Finally, results will be presented and discussed in the last part.

Here below is an example of the simulation for a specific building.

<img src="https://github.com/Alban999/WiFi-Ray-Tracing-Simulation/assets/74149424/a12b91b7-dbf0-4aea-a399-075d9932055f"> <img src="https://github.com/Alban999/WiFi-Ray-Tracing-Simulation/assets/74149424/6f3cdd39-2cba-406a-ace2-a7c4d3aa7b77">




​
