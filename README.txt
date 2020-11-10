# Information

Readme.txt file for MSD P21422 created 10/27/2020
Author(s): Jennika Haining (jmh1592), Josh Noble (jtn6092)
Purpose: to monitor and control the environment for the Black Soldier Fly Smart Shed
	on the RIT campus.

Files:
	main.py   : outputs environmental data to a CSV file for analysis
	relay.py  : controls electrical relay that manage vent, humidifier, and heater
	sensor.py : collects environmental data from sensors

## Usage

To run the program from the shell, navigate to the folder containing main.py
and use the following command:

```
	python3.5 main.py (-v[erbose])
```

-v flag is an optional argument to determine if the program prints to the 
shell or not. If -v is set, program should print something like:

```
	Current Date: 10/27/20 12:25:48PM
	Indoor readings:
 	Temperature: 21.87*C [71.33*F]
	Relative Humidity: 37.1%
	Dew Point: 5.89*C

	Outdoor readings:
 	Temperature: 21.74*C [71.09*F]
	Relative Humidity: 35.21%
	Dew Point: 5.12*C
```


If the program is running in the background and you need to kill it, first obtain the
list of currently running processes by running the following command

```
	ps aux | grep python3.5
```
A list of currently running python processes should appear. You can determine which is
the program by the filepath listed in the processes.
Find the PID, which is the number in the second column, and run the following command

```
	sudo kill <PID>
```

Run the 'ps aux' command again to confirm the program is killed

## License
