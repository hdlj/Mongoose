# Mongoose

Mongoose is a real-time operating system based on a preemptive round robin scheduling with a microkernel architecture. It works on Arduino Uno board with ATMega328p and 2KB of RAM. Multiple applications (up to 3) can run concurrently on the board. Each application is considered as a process with its own stack. They have equal priorities. The quantum (time slice), for the round robin scheduling policy, is 2 ms offering a balance between the scheduler overhead and the impact of the number of processes.

Time constraints are expressed as delays in applications. These delays have a bounded time error, which is related to the kernel period (quantum). However, a long atomic operation can increase this error. In addition, for long delay, this error becomes unrelated to the kernel period when the scheduler anticipates its overhead (optimized time constraints).
Mongoose provides an abstraction for hardware events through the event handler process. An application can register a listener to each type of events. The responsive time depends on event’s type, the corresponding listener and applications’ behaviour . Events cannot preempted each other and can be lost because of long computational listeners.

Additionally, Mongoose lets applications communicate with each other through channels. Each channel is one-to-one and cannot be used in two directions. Synchronisation between applications is done with a reader/writer concept. A reader cannot read a value, which has been already read. In the same way, a writer cannot override an unread value. Channel access does not lead to starvation or deadlock thanks to the scheduler fairness. Nonetheless, starvation and deadlock can happen because of the synchronisation mecha- nism.

Drivers for serial communication, digital devices, analog devices have been developed in this project. They offer basic features. Nonetheless, we try to have a clear and consistent hardware API.
Applications can be written in C, in C++ or with a subset of Python. A development environment has been developed in this project. Python applications are translated to C thanks to the parser developed in this project. Developers can develop applications with any text editor or IDE. Uploading operating is done with a makefile. Clear APIs and the possibility of Python make this operating system more developer friendly.

Mongoose has a small memory footprint: 0.5 of RAM and 6KB of ROM. In addition, time constraints are respected with an error, which can be predicted. Finally, the scheduler provides a predictive behaviour. Therefore, Mongoose respects requirements, quoted in chapter 3, of a real-time operating system and the objectives presented in chapter 1. Nonetheless, Mongoose does not manage Internet protocols.

# Get started

## Installation

Download the latest release or clone it from Github using the command:

`git clone https://github.com/hdlj/Mongoose.git`

## Requirements

MongooseOS needs Arduino IDE, Python 3.4.

#### Arduino IDE 
Arduino IDE can be found on https://www.arduino.cc/en/main/software

#### Python 3.4 
Python 3.4 can be found on https://www.python.org/download/releases/3.4.0/


## Setup

On Mac OS X:

* Open Application>Utilities>Terminal.app. To setup Mongoose, you need your Arduino board name (here Arduino Uno).
* Go to Mongoose directory
* Run this command line:

`$python3 setup.py uno`

A template folder named "Project_uno" has been created. This folder doesn't have to stay in Mongoose. However, every arduino application folder has to contain at least the Makefile created, "MOSConfig.py", "MOSInterfaceC.py" and source files (C, C++ and Python) for the application.


Also 5 examples (Arduino Uno) are now ready to run. 

###Example 0  

App1:

        -> Blink a LED on digital port 4 every second


###Example 1  

App1:

        -> Blink a LED on digital port 4 every second
    
App2:

     -> Blink a LED on digital port 3 every 100 ms

### Example 2

App1:

     -> Blink a LED on digital port 4 every second


App2: 

     -> Take samples on analog port 0 every second
     -> If a button is pressed on digital port 2, blink a LED on digital port 2 4 times (period 500 ms)

### Example 3

App1:

     -> Take samples on analog port 1 every 100 ms
     -> Send result on channel 1 and read channel 3
     
     
App2: 

     -> Take samples on analog port 2 every 100 ms
     -> Send result on channel 2 and read channel 1
     
     
App3:

     -> Take samples on analog port 3 every 100 ms 
     -> Send result on channel 3 and read channel 2

### Example 4

App1:

     -> Blink a LED on digital port 4 every second


App2: 

     -> Take samples on analog port 0 every second
     -> Send result on channel 0
     -> If a button is pressed on digital port 2, blink a LED on digital port 2 4 times (period 500 ms)


App3: 

     -> Read channel 0  five times successively
     -> Compute an atomic operation with results
     -> Read again channel 0


### Run an example

* First, open the Makefile contained in Example0 folder and edit it with (it can be different with you computer):

`USB_PORT = /dev/tty.usbmodem1421`

or 

`USB_PORT = /dev/tty.usbmodem1411`

If they do not corrspond to you computer USB port, you can find your board port by running this command line:

`$ls /dev/tty.*`

* Go to Example 1 folder with Terminal

```
$ cd Example0
```
* To upload to the board, run this command line:

`$make upload`

* To upload to Arduino board and store the logs from the board, run this command line:

`$make upload-store-log`

you can exit the screen mode with `CTRL+A+K` then `Y`. The logs will be contained in the current directory


# Writing an application for Mongoose: MOSPython

Applications can be written in C, C++ or Python.



#### Overview

Firstly, MOSPython will create a source directory in the working directory if it is not already done. Then, MOSPython will search all python files present in the working directory then it will translate them in C. Secondly, MOSConfig file will be used for configuring Mongoose. This file contains each application start function and what stack size each application needs. Then, all C and C++ files and Mongoose will be compiled in machine code. Finally, all machine code will be linked together in an Intel hex file and uploaded to the board. Each step is executed in the Makefile. With this approach, developers can use every text editors or IDE which supports Python 3.4.

#### MOSFoundation


Python applications will be translated in C. They need to import MOSFoundation file in order to have access to drivers functions and Mongoose public functions :

` import MOSFoundation `

C/C++ applications need to import MOSFoundation file in order to have access to drivers functions and Mongoose public functions :

` #include <MOSFoundation.h> `


#### Supported types

You don't need to specify the type of each variable except functions' arguments and functions' return type. When your code is parsed by MOSPython, the type of each local variable and global variable will be defined.

Mongoose supports integers (int), floats (float), strings (str), lists (list) and booleans (bool). List can only stores at most 5 integers (int)


## Hardware API

#### Default led

A led is connected to the port 13 on Arduino Uno. This led is named the default led in MongooseOS.

Available functions: 

`   HOSLedSetup()  ` Setup the default led

`   HOSLedOn()     ` Turn on the default led

`   MOSLedOff()    ` Turn off the default led


#### Digital port

Arduino Uno has 14 ports (0 to 13). The port 13 is already connected to the default led.

Available functions: 

`   HOSDigitalSetup(2)             ` Set the port 2 as an output

`   HOSDigitalOn(2)                ` Turn on the port 2

`   HOSDigitalOff(2)               ` Turn off the port 2

`   HOSDigitalListen(2, listener)  ` Digital port 2 is then set as an input. The listener is executed when a FALLING signal edge, such as a pressed button, is detected on the digital port 2


#### Serial communication

You can communicate via the serial port. If you want to see the serial port on your terminal and store the logs in you project folder, use:

` $make upload-store-log `

In order to print a string on the serial port, you can use: 

` print("hello world") ` like in Python

or you can use: 

` HOSSafePrint("hello world")`   Print a string without be interrupted by Mongoose

` HOSSafePrintInt(300)       `   Print an integer without be interrupted by Mongoose

####  Analog

You can take sample on an analog port

` HOSAnalogSetup()   `   Set up the analog driver

` HOSAnalogRead(2)   `   Read an anolog pin value.

## Mongoose API

#### Atomic operation

An application can execute an atomic operation. This block of code will not be interrupted by Mongoose until it is finished:

` MOSAtomicEnter() ` Start an atomic operation

` MOSAtomicExit()  ` Stop an atomic operation

#### Delay/Sleep

You can let an application wait n milliseconds with :

` delay(1000)     `    the corresponding application will be stopped and then rescheduled after n millisecond

` MOSSleep(1000)  `    the corresponding application will be stopped and then rescheduled after n millisecond

Another application will then scheduled. If no application can be exectued (they are all in sleep mode), the CPU will go in idle mode

#### Events 

Mongoose run an event handler process. Each time an event happens on a digital pin, this event is executed by this process.
An application can push an event to this process. This handler has a FIFO queue storing all events to execute. However this queue has a limited capacity. If the capacity limit is reached, the following events are rejected until there is a free position at the end of the queue.

` MOSEventReceived(listener) ` push listener function to the event handler process

#### Error

You can stop all application by sending an error to Mongoose. The error message will be printed and Mongoose will go in idle mode. All applications will be stopped definitely.

`MOSError("error message") ` Send an error to Mongoose

#### Inter process communication

Applications can communicate with other applications via channels there is 6 channels. Each channel has to have an application writer and an application reader:

`MOSSendMessage(data,0)   ` write "data" on channel 0

`MOSReadChannel(0)        ` read channel 0

The report in the repository explains how this communication mechanism work


#Futur Work

Mongoose still needs to be more developed. In this section, we will suggest a list of future work.


#### Mongoose and internet

One of the objectives of internet of things is to let devices connect to the internet. In fact, Mongoose does not integrate any internet protocols. It would be a main improvement for this operating system. This capability should not decrease Mongoose performances and be able to work with constrained resources. With internet, Mongoose could be able to download new applications or software updates which could make it more flexible.

#### Mongoose and energy consumption

Energy consumption is also a key feature for internet of things. There is no energy saving mechanism. Thanks to such mechanism, Mongoose would be able to monitor energy consumption of the whole system. Based on this analysis, Mongoose would be able to ask a peripheral device or a process to reduce its power consumption.

#### Multitasking

Mongoose is already able to run applications concurrently. These applications, as pro- cesses, have separated stacks. A priority policy added to the scheduler may be an inter- esting improvement in order to reduce the time constraint error.

Moreover, each application has one thread of execution. Introducing multithreading possibilities within an application would allow Mongoose to support more complex appli- cations. Also, shared stack between threads could be interesting in order to avoid memory space losses.

Application may crash during execution. Mongoose is not able to detect and stop a crashed application. It could be an interesting start point to make Mongoose more robust. In addition, Mongoose could load and unload application at run-time. It may offer the possibility to have more applications available on a board without launching all of them when Mongoose starts. Downloaded applications from the internet could be launched when they need to start.

#### Development environment

A development environment has been created in this project. It could be interesting to integrate this environment in the most used IDE on all main operating system (Linux, Mac OS X and Windows).

Only a subset of Python is available for developing applications. Improving the parser capabilities may let python application having more features. For instance, only basic types are supported. Developer may be able to use their own types and more advanced python features.

#### Memory Management

Mongoose uses for now only static allocation for the memory. Introducing a dynamic memory management may be interesting. Indeed, it could prevent memory space losses due to memory fragmentation.
Moreover, it could be interesting to let Mongoose and applications work with different memory (EEPROM, flash, RAM, SD card,...).

#### Cross platform
We have worked with ATMega328p for Mongoose development. So, for now, it is only compatible with boards based on this microcontroller. Nonetheless, Mongoose should be available on a large range of hardware. It will be interesting to port this operating system to all IoT platform. It will increase applications’ capabilities. In fact, each platform has different hardware and different features.

