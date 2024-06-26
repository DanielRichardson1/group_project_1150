# Simulation of V2V Communication for Enhanced Head-on Collision Avoidance Systems

The goal of this simulation is to evaluate the efficacy of Vehicle-to-Vehicle Dedicated short-range communications in preventing head-on collisions. In order to test DSRC’s efficiency, this simulation considers the most basic scenario- head on automobile collisions. The simulation involves two cars, moving towards each other on a one-dimensional road, in order to simulate a crash-scenario. The key here is that variables such as position,  velocity, acceleration, braking force, and braking time can be changed with each run of the simulation. This allows us to test how both non-DSRC and DSRC enhanced vehicles perform under different conditions.	
	
This simulation is coded in Python, with the backbone of the simulation being a car class. The car object has 5 member variables which are position, velocity, direction, acceleration, and braking distance (As shown below). The simulation involves two of these car objects, facing each other.	
 	
The simulation runs in a real-time loop, and is constantly checking for three things: communication between the cars, car collision, and both cars being completely stopped. Communication between cars is represented by the cars braking (acceleration being set to 15 feet/second) when the cars are within the distance at which they are able to communicate (For DSRC, reliable communication length is about 300 meters in 5.9 GHz band with bandwidth of 75 MHz, whereas human perception is much more variable, but has been valued at an average of 300 ft). A car collision is represented visually in this simulation and we are shown the speed of each car at the time of crash.

Both cars being completely stopped means no crash will occur, so we are successful in preventing a crash and we are shown the distance in between the two cars’ fronts

The results of the simulation demonstrate that V2V communication can prevent head-on collisions by enabling cars to exchange information and foresee possible automobile accidents faster than a human driver can alone.
