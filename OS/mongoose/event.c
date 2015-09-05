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






#include "event.h"
#include "kernel.h"
#include "mongoose.h"



void (*listener_ptr[NB_EVENT_MAX]);
void (*(*listeners)[NB_EVENT_MAX])();
listener currentFct ;
uint8_t size;
uint8_t top;




void KOSEventInit(){
	size = 0;
	top  = 0;
	currentFct = NULL;
	uint8_t index;
	for ( index = 0; index <NB_EVENT_MAX ; index++)
	{
		listener_ptr[index] = NULL;
	}
	listeners=&listener_ptr;
}


void KOSEventInsertListener(listener fct){
    uint8_t position = top+size;
    printf("B\n");
    if (size>=NB_EVENT_MAX)
    {
    	printf("overflow\n");
    	return;
    }
    if (currentFct==fct)
    {
    	printf("Rejected\n");
    	return;
    }
    if(position>=NB_EVENT_MAX){
    	position = position -  NB_EVENT_MAX;
    }
    printf("added\n");
    listener_ptr[position] = fct;
    size++;

}



void KOSEventCenterRun(){
	while(1){
			while(size > 0){
				MOSAtomicEnter();
				currentFct=listener_ptr[top];
				MOSAtomicExit();
				(*(*listeners+top))();
				MOSAtomicEnter();
				size--;
				top++;
				if (top>=NB_EVENT_MAX)
				{
					top=0;
				}
				currentFct = NULL;
				MOSAtomicExit();
			}
			KOSSwap();
	}
}


void MOSEventReceived(listener fct){
	MOSAtomicEnter();
	printf("Received\n");
	KOSEventInsertListener(fct);
	MOSAtomicExit();
	KOSSwapEvent();
}








