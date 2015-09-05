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






#ifndef KERNEL_H
#define KERNEL_H

#include "mongoose.h"


// period of the kernel clock
#define PERIODE_KERNEL  3
// overhead in ms 
#define OVERHEAD_SCHEDULER 0.03

void KOSRun();
void KOSAddApp(void* functionEntryPoint, StackSize size);
void KOSIntialize();
// the event handler can ask to the scheduler to be scheduled right away
void KOSSwapEvent();
// evaluation of the free RAM
int  KOSFreeRam ();
// print info messages
void KOSInfo(string  info_message);
#endif 