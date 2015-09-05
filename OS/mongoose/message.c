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








#include "message.h"
#include "kernel.h"
#include "mongoose.h"

#define MAX_CHANNEL 6

Message kMessage[MAX_CHANNEL];
Channel kChannel[MAX_CHANNEL];
MState  KMState[MAX_CHANNEL];


bool MLockChannel(uint8_t port);
void MFreeChannel(uint8_t port);
bool MChannelStateRead(uint8_t port);


void KOSMessageInit(){
	uint8_t index;
	MOSAtomicEnter();
	for(index = 0; index <MAX_CHANNEL; index++){
		kMessage[index].data = 0;
		KMState[index] = ALREADY_READ;
		kChannel[index] = FREE;
	}
	MOSAtomicExit();
}

void MOSSendMessage(uint16_t msg, uint8_t port){
	// wait until the channel is freed
	while(!MLockChannel(port)){
		KOSSwap();
	}
	if (MChannelStateRead(port))
	{
		kMessage[port].data  = msg;
	    KMState[port] = NOT_READ;
		MFreeChannel(port);
		KOSSwap();
	}
	else{
		// cannot overwrite an unread value so the channel is freed

		MFreeChannel(port);
		KOSSwap();
		//the process has to try again
		MOSSendMessage(msg,port);
	}
}

uint16_t MOSReadChannel(uint8_t port){
	while(!MLockChannel(port)){
		KOSSwap();
	}
	if (!MChannelStateRead(port))
	{
		Message current = kMessage[port];
		KMState[port] = ALREADY_READ;
		MFreeChannel(port);
		KOSSwap();
		return current.data;
	}
	else{
		// cannot read a value which has been alread read
		MFreeChannel(port);
		KOSSwap();
		//the process has to try again
		return MOSReadChannel(port);
	}
}

bool MLockChannel(uint8_t port){
	// atomic operation in order to avoid race condition
	MOSAtomicEnter();
	if (kChannel[port] == FREE)
	{
		kChannel[port] == LOCKED;
		MOSAtomicExit();
		return true;
	}
	MOSAtomicExit();
	return false;
}

void MFreeChannel(uint8_t port){
	MOSAtomicEnter();
	kChannel[port] == FREE;
	MOSAtomicExit();
}

bool MChannelStateRead(uint8_t port){
	MOSAtomicEnter();
	if(KMState[port]==ALREADY_READ){
		MOSAtomicExit();
		return true;
	}
	MOSAtomicExit();
	return false;
}


