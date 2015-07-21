# MongooseOS

MongooseOS is a tool in order to let developers write arduino application in python independetly from the IDE/Text editor choosen. For now, it is available only on MacOS

# Get started

## Installation

Download the latest release or clone it from Github using the command:

`git clone https://github.com/hdlj/MongooseOS.git`

## Requirements

MongooseOS needs Arduino IDE, Python 3.4 in order to work

#### Arduino IDE 
Arduino IDE can be found on https://www.arduino.cc/en/main/software

#### Python 3.4 
Python 3.4 can be found on https://www.python.org/download/releases/3.4.0/


## Setup the tool

On Mac OS X:

* Open Application>Utilities>Terminal.app. To setup MongooseOS, you need your Arduino board name (here Arduino Uno).
* Go to MongooseOS directory
* Run this command line:

`$python3 setup.py uno`

A template folder named "BlinkLed_uno" has been created. This folder doesn't have to stay in MongooseOS. However, every arduino application folder has to contain at least the Makefile created by MongooseOS, "MOSFoundation.py" and source files for the application.

* Run this command line in order to setup the simulator:

```
$ cd BlinkLed_uno
$ make MOSSimulator-setup
```

## First example: blink a led

* First, open the Makefile contained in BlinkLed_uno folder and edit it with:

`USB_PORT = /dev/tty.usbmodem1421`

You can find your arduino board port by running this command line:

`$ls /dev/tty.*`

* Go to BlinkLed_uno folder with Terminal

* To upload to Arduino board, run this command line:

`$make upload`

* To upload to Arduino board and store the logs from the board, run this command line:

`$make upload-store-log`

you can exit the screen mode with `CTRL+A+K` then `Y`


## Writing a MongooseOS application

The application needs to implement two functions and import MOSFoundation file:

` from MOSFoundation import * `

` setup `  In this function, all setup operations are done

` loop `   This function is repeat infinitely




#### For loop 

A for loop allows code to be executed a certain number of times. In this example, a counter is implemented 100 times 
``` 
counter = 0
for i in range(100):
    counter = counter + 1 
```
#### If loop

An if loop allows code to be executed only if the boolean condition is satisfied

```
value = 1
if value == 1 :
    value = 0
elif value = 2 :
    value = 1
else : 
    value = 2
```

#### While loop

A while loop allows code to be executed repeatly until a condition is statified

```
counter = 0

while counter < 100:
    counter = counter +1

```

#### function definition

Functions are defined by: 

```
def addition( a : int , b : int) -> int :
    return a + b

```

The type of each function's argument has to be precised and also the return type

#### Supported types

You don't need to specify the type of each variable except functions' arguments and functions' return type. When your code is parsed by MongooseOS, the type of each local variable and global variable will be defined.

MongooseOS supports integers (int), floats (float), strings (str) 


## Hardware API

#### Default led

A led is connected to the port 13 on Arduino Uno. This led is named the default led in MongooseOS.

Available functions: 

`   MOSLedSetup()  ` Setup the default led

`   MOSLedOn()     ` Turn on the default led

`   MOSLedOff()    ` Turn off the default led


#### Digital port

Arduino Uno has 14 ports (0 to 13). The port 13 is already connected to the default led.

Available functions: 

`   MOSDigitalSetup(2)  ` Setup the port 2

`   MOSDigitalOn(2)     ` Turn on the port 2

`   MOSDigitalOff(2)    ` Turn off the port 2


#### Serial communication

You can communicate via the serial port. If you want to see the serial port on your terminal and store the logs in you project folder, use:

` $make upload-store-log `

In order to print a string on the serial port, you can use: 

` print ("hello world") ` like in Python

You can also concatenate two strings :

` print( "hello " + "world" ) `


#### Delay

You can let the CPU waits n milliseconds with the delay function :

` delay(1000) ` CPU will wait 1000 milliseconds (i.e. 1 second)


## MOSSimulator

MongooseOS provides a simple simulator in order to test your code without an Arduino board

* Open Terminal application and go to your project folder
* Run this if it is the first time you use it in your project: 
`$ make MOSSimulator-setup`
* Run this to launch the simulator: `$ make MOSSimulator-run`





