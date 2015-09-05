
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


==================================================================================*/


#ifndef DIGITAL_H
#define DIGITAL_H


#include <stdint.h>
#include <avr/io.h>
#include <avr/interrupt.h>
#include <stdbool.h>
#include <stddef.h>
#include <mongoose/mongoose.h>


#define NB_PIN 13

void HOSDigitalSetup(uint8_t pin);
void HOSDigitalOn(uint8_t pin);
void HOSDigitalOff(uint8_t pin);
void HOSDigitalListen(uint8_t pin, void * listener);
void HOSDigitalInit();



#endif