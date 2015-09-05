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



#include "process.h"
#include "event.h"
#include "kernel.h"
#include "mongoose.h"

#define PROCESSMAX 5
uint8_t *processStack[PROCESSMAX];//last position for the idle task
uint16_t processSleep[PROCESSMAX];
uint8_t currentProcess=PROCESSMAX;
uint8_t processSize = 0;
uint8_t processSleeping = 0;

uint8_t ** MOSIdleMode();

void KOSPInit(){
 	
	// store the stack pointer of each process (0 by default)
	uint8_t index;
	for (  index = 0; index<PROCESSMAX;index++) {
        processStack[index] = 0;
        processSleep[index] = 0;
    }

}

uint8_t ** KOSPNext(){
	currentProcess++;
	if (currentProcess>= processSize)
	{
		currentProcess=0;
	}
	if (processSleep[currentProcess] > 0)
	{
		processSleeping++;
		if (processSleeping>=processSize)
		{
			//everyone is sleeping
			//enter in idle mode
			//printf("MOS IDLE MODE EVERYONE IS SLEEPING\n");
			processSleeping = 0;
			return KOSIdleMode();
		}
		return KOSPNext();
	}
	processSleeping = 0;
	return processStack+currentProcess;
}



uint8_t ** KOSPEvent(){
	return processStack+0;
}

bool KOSPEventProcessIsSleeping(){
	if (processSleep[0]==0)
	{
		return false;
	}
	return true;
}

void  KOSPAdd(uint8_t* stackPointer){
	 if (processSize>=PROCESSMAX)
	 {
	 	 MOSError("--> OS ERROR: TOO MANY APPLICATIONS\n");
	 }
	 processStack[processSize]=stackPointer;
	 processSize++;
}

void KOSPSleep( uint16_t millis){
	processSleep[currentProcess] = millis;
}

void KOSPSleepUpdate(uint16_t periode){
	MOSAtomicEnter();
	uint8_t index = 0;
	for (index = 0; index < PROCESSMAX; ++index)
	 {
	 	uint16_t current = processSleep[index];

	 	if (current < periode)
	 	{
	 		processSleep[index]  = 0;
	 	}
	 	else{
	 		processSleep [index] = current - periode;
	 	}
	}
	MOSAtomicExit();
}

uint8_t KOSPSize(){
	return processSize;
}
