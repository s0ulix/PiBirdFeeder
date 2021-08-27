# PiBirdFeeder
This is a driver code for a bird feeder housing which consist a pi, a camera and motion sesnsor 
so it takes a picture whenever motion detected and find out which species it is with the help of machine learning.

The ml model can be set to run on cloud as an api for which code is given.

There are 2 main files one which work with cloud api other one which does everything locally.

This was tested on the RaspberryPi 4 with 4 gb ram

Need to install tf version 2.4.x

keras compatible with specific tf

scikit learn

All other packages are built in the pi os
