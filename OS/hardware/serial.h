


/* ===============================================================================
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>



Date: 2015


based on this source code written by Mika Tuupola:
https://github.com/tuupola/avr_demo/tree/master/blog/simple_usart

and this post:
http://www.appelsiini.net/2011/simple-usart-with-avr-libc

===============================================================================*/

#ifndef SERIAL_H
#define SERIAL_H

    
#include <stdio.h>
#include <stdarg.h>
#include <avr/pgmspace.h>
#define F_CPU 16000000UL
#define BAUD 9600
#include <util/setbaud.h>
#include <mongoose/mongoose.h>

// set up the serial port with a baud of 9600
void HOSSerialSetup();
// print a string without be interrupted
void HOSSafePrint(string input);
// print an integer without be interrupted
void HOSSafePrintInt(uint16_t data);

#endif