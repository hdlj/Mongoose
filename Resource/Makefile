
#This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.#
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>


#===============  SETUP   ==============
ARDUINO_PORT = /dev/tty.usbmodem1421
ARDUINO_DIR  = /Applications/Arduino.app/Contents/Resources/Java
AVR_TOOLS_DIR =$(ARDUINO_DIR)/hardware/tools/avr
AVRDUDE_CONF    = $(AVR_TOOLS_DIR)/etc/avrdude.conf

#============== Current Time ==========
CURRENT_TIME=`date +'%y.%m.%d-%H:%M:%S'`


#===============  BOARD PARAMETERS   ==============
BOARDS_TXT:=$(ARDUINO_DIR)/hardware/arduino/avr/boards.txt

BOARD:=uno
# get the MCU value from the $(BOARD).build.mcu variable. For the atmega328 board this is atmega328p
ARDUINO_MCU:=$(shell sed -n -e "s/$(BOARD).build.mcu=\(.*\)/\1/p" $(BOARDS_TXT))
# get the F_CPU value from the $(BOARD).build.f_cpu variable. For the atmega328 board this is 16000000
ARDUINO_F_CPU:=$(shell sed -n -e "s/$(BOARD).build.f_cpu=\(.*\)/\1/p" $(BOARDS_TXT))
# get the AVRDUDE_UPLOAD_RATE value from the $(BOARD).upload.speed variable. For the atmega328 board this is 57600
ARDUINO_SERIAL_PORT_SPEED:=$(shell sed -n -e "s/$(BOARD).upload.speed=\(.*\)/\1/p" $(BOARDS_TXT))
# get the AVRDUDE_PROGRAMMER value from the $(BOARD).upload.protocol variable. For the atmega328 board this is stk500
PROGRAMMER:=$(shell sed -n -e "s/$(BOARD).upload.protocol=\(.*\)/\1/p" $(BOARDS_TXT))


ifndef MOSLib
$(error MOSLib is not set)
endif

ifndef ARDUINO_MCU
$(error ARDUINO_MCU is not set)
endif
ifndef ARDUINO_F_CPU
$(error ARDUINO_MCU is not set)
endif
ifndef ARDUINO_SERIAL_PORT_SPEED
$(error ARDUINO_MCU is not set)
endif
ifndef PROGRAMMER
$(error PROGRAMMER is not set)
endif

#============== Compilation tools ============
CC=$(AVR_TOOLS_DIR)/bin/avr-gcc
OBJCOPY=$(AVR_TOOLS_DIR)/bin/avr-objcopy
OBJDUMP=$(AVR_TOOLS_DIR)/bin/avr-objdump
CFLAGS=-w -Os
OBJCOPY_FLAGS=-O ihex -R .eeprom

#==============    Upload tools   ============

AVRDUDE=$(AVR_TOOLS_DIR)/bin/avrdude
AVRDUDE_FLAGS= -F -V 


#==============   Source files    ============

SUBDIRS := $(wildcard */) $(wildcard $(MOSLib)/*/)
SOURCES := $(wildcard $(addsuffix *.c,$(SUBDIRS))) $(wildcard *.c)
OBJFILES := $(patsubst %.c,%.o,$(SOURCES))

#==============       Target      ===========

TARGET_HEX = $(TARGET).hex
TARGET_ELF = $(TARGET).elf
TARGET  = $(notdir $(shell pwd))




all: build


#==========   Compile c files     =======
%.o: %.c
	$(CC) $(CFLAGS) -DF_CPU=$(ARDUINO_F_CPU) -I $(MOSLib) -mmcu=$(ARDUINO_MCU) -c -o $@ $<

#==========   link object files   =======
%.elf: $(OBJFILES)
	$(CC) -mmcu=$(ARDUINO_MCU) $(OBJFILES) -o $@

#==========   build final hex file =======
%.hex: %.elf
	$(OBJCOPY) $(OBJCOPY_FLAGS) $< $@


#==========  BUILD AND UPLOAD FOR DEFAULT PLATFORM : UNO ==========
build:  clean $(TARGET_HEX)
#
#
upload: build
	$(AVRDUDE) $(AVRDUDE_FLAGS) -c $(PROGRAMMER) -C $(AVRDUDE_CONF) -p $(ARDUINO_MCU) -P $(ARDUINO_PORT) -b $(ARDUINO_SERIAL_PORT_SPEED) -U flash:w:$(TARGET_HEX)
#
upload-store-log: upload
	echo "\n\n\n\n\n\n========LOGS STARTED AT $(CURRENT_TIME)======\n\n\n\n\n" >> screenLog.0
	screen -L $(ARDUINO_PORT)

#==========  BUILD AND UPLOAD FOR UNO =================

arduino-uno:
	$(MAKE) BOARD=uno build

arduino-uno-upload:
	$(MAKE) BOARD=uno upload

arduino-uno-upload-store-log:
	$(MAKE) BOARD=uno upload-store-log

#==========  BUILD AND UPLOAD FOR MEGA ADK ==============

arduino-mega-adk:
	$(MAKE) BOARD=megaADK build

arduino-mega-adk-upload:
	$(MAKE) BOARD=megaADK upload

arduino-mega-adk-upload-store-log:
	$(MAKE) BOARD=megaADK upload-store-log

#=========   CLEAN ========
clean:
	rm -rf $(addsuffix *.o,$(SUBDIRS))
	rm -rf *.o
	rm -rf *.elf
	rm -rf *.hex
