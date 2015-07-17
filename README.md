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




