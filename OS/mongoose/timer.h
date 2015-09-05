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
   

#ifndef TIMER_H
#define TIMER_H


#include <avr/interrupt.h>
#include <avr/io.h>
#include <stdio.h>
#include <stdarg.h>


#define F_CPU  16000000.0
#define TIMER_PRESCALER 8
#define MAX_16BIT 65536

void KOSTimerStartMS(uint16_t ms, void (*action) (void));

#endif