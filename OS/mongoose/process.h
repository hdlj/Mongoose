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




#ifndef PROCESS_H
#define PROCESS_H

#include <stdint.h>
#include <stdbool.h>

void KOSPInit();
uint8_t ** KOSPNext();
void  KOSPAdd(uint8_t* stackPointer);
uint8_t KOSPSize();
void KOSPSleep( uint16_t millis);
void KOSPSleepUpdate(uint16_t periode);
bool KOSPEventProcessIsSleeping();
uint8_t ** KOSPEvent();

#endif