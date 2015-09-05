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


/*==================================================================================


==================================================================================*/


#ifndef MOS_H

#define MOS_H

#include <stddef.h>
#include <stdbool.h>
#include <stdint.h>
#include "type.h"
// define if scheduler needs to anticipate its overhead
#define KERNEL_OPTIMISATION 0


typedef enum Stack {
	SMALL, 
	NORMAL,
	LARGE
} StackSize;


/*==================================================================================

Public functions accesible by applications and drivers

==================================================================================*/

//Event 
typedef void (*listener)(void);
void MOSEventReceived(listener fct);


// Kernel

#define MOSAtomicEnter()  asm("CLI")
#define MOSAtomicExit()   asm("SEI")

void MOSSleep(uint16_t millis);
void MOSError(string  error_message);


// Inter Process Communication

void MOSSendMessage(uint16_t msg, uint8_t port);
uint16_t MOSReadChannel(uint8_t port);


#endif