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









#ifndef MESSAGE_H
#define MESSAGE_H
#include <stdint.h>



typedef enum MState {
	ALREADY_READ, 
	NOT_READ,
} MState;

typedef enum CState {
	FREE, 
	LOCKED
} Channel;


typedef struct Message{
	uint16_t data;
	MState   state;

} Message;


void KOSMessageInit();


#endif