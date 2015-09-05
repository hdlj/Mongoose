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

Based on AvrRTOS source code written by Tapio Hirvikorpi, Johannes Aalto (switch between contexts and initialization of a process's stack, main function adress storage): 
This kernel is based on AvrRTOS source code :www.electro-tech-online.com/attachments/avrrtos-c.73611/


and also  for the evaluation of the free RAM:
http://jeelabs.org/2011/05/22/atmega-memory-use/

==================================================================================*/



#import "kernel.h"
#include "process.h"
#include "event.h"
#include "message.h"
#include "timer.h"
#include "mongoose.h"
#include <hardware/hardware.h>

#define SAVE_CONTEXT()          \
	asm volatile (                        \
		"push r0                 ;Register R0 is saved first                             \n\t" \
		"in r0, __SREG__         ;Status Register is moved into R0                       \n\t" \
		"cli                     ;Interrupts are disabled as soon as possible            \n\t" \
		"push r0                 ;Status Register is saved                               \n\t" \
		"push r1                 ;Register R1 is saved                                   \n\t" \
		"clr r1                  ;Register R1 is cleared because gcc assumes it is zero  \n\t" \
		"push r2                 ;Registers R2...R31 are saved in a numerical order      \n\t" \
		"push r3                 \n\t" \
		"push r4                 \n\t" \
		"push r5                 \n\t" \
		"push r6                 \n\t" \
		"push r7                 \n\t" \
		"push r8                 \n\t" \
		"push r9                 \n\t" \
		"push r10                \n\t" \
		"push r11                \n\t" \
		"push r12                \n\t" \
		"push r13                \n\t" \
		"push r14                \n\t" \
		"push r15                \n\t" \
		"push r16                \n\t" \
		"push r17                \n\t" \
		"push r18                \n\t" \
		"push r19                \n\t" \
		"push r20                \n\t" \
		"push r21                \n\t" \
		"push r22                \n\t" \
		"push r23                \n\t" \
		"push r24                \n\t" \
		"push r25                \n\t" \
		"push r26                \n\t" \
		"push r27                \n\t" \
		"push r28                \n\t" \
		"push r30                \n\t" \
		"push r29                \n\t" \
		"push r31                \n\t" \
		"lds r26, currentStackPtr   ;The X register is loaded with the address to..     \n\t" \
		"lds r27, currentStackPtr+1 ;..which the Stack Pointer is to be saved           \n\t" \
		"in r0, __SP_L__         ;The low byte of the Stack Pointer is moved to R0   \n\t" \
		"st x+, r0               ;The low byte of the Stack Pointer is saved         \n\t" \
		"in r0, __SP_H__         ;The High byte of the Stack Pointer is moved to R0  \n\t" \
		"st x+, r0               ;The High byte of the Stack Pointer is saved        \n\t" \
);


#define LOAD_NEXT_CONTEXT()          \
	asm volatile (                        \
		"lds r26, currentStackPtr      \n\t" \
		"lds r27, currentStackPtr + 1  \n\t" \
		"ld r28, x+                 \n\t" \
		"out __SP_L__, r28          \n\t" \
		"ld r29, x+                 \n\t" \
		"out __SP_H__, r29          \n\t" \
		"pop r31                    \n\t" \
		"pop r30                    \n\t" \
		"pop r29                    \n\t" \
		"pop r28                    \n\t" \
		"pop r27                    \n\t" \
		"pop r26                    \n\t" \
		"pop r25                    \n\t" \
		"pop r24                    \n\t" \
		"pop r23                    \n\t" \
		"pop r22                    \n\t" \
		"pop r21                    \n\t" \
		"pop r20                    \n\t" \
		"pop r19                    \n\t" \
		"pop r18                    \n\t" \
		"pop r17                    \n\t" \
		"pop r16                    \n\t" \
		"pop r15                    \n\t" \
		"pop r14                    \n\t" \
		"pop r13                    \n\t" \
		"pop r12                    \n\t" \
		"pop r11                    \n\t" \
		"pop r10                    \n\t" \
		"pop r9                     \n\t" \
		"pop r8                     \n\t" \
		"pop r7                     \n\t" \
		"pop r6                     \n\t" \
		"pop r5                     \n\t" \
		"pop r4                     \n\t" \
		"pop r3                     \n\t" \
		"pop r2                     \n\t" \
		"pop r1                     \n\t" \
		"pop r0                     \n\t" \
		"out __SREG__, r0           \n\t" \
		"pop r0                     \n\t" \
);



/* Amount of memory (in bytes) used for stacks of each task*/
#define STACKSIZE_SMALL 100
#define STACKSIZE_NORMAL 200
#define STACKSIZE_LARGE 300




/* currentStackPtr is a pointer that points to a memory location where the
   "save_execution_context()" macro saves the stack pointer. Normally this memory
   location is in the "stackPtr" -array. */
uint8_t **currentStackPtr;

/* This is actually never used, because we don't return to main(), but we save
   the main functions stack pointer anyway. Main function could be used as an
   idle task */
uint8_t *mainStackPtr;

uint16_t stacksize_counter;

// private function which cannot be accessible by any other file
void KOSTimerTick();
void KOSIdle();
void KOSSwap();
void KOSNext();
void KOSSechuler(void);




void KOSIntialize(void)
{	
	
	KOSInfo("OS is loading");
	// store the main function for idle mode
	currentStackPtr = &mainStackPtr;
	// we start from kernel stack, then we add the event handler process and then the applications
	stacksize_counter = STACKSIZE_SMALL;

    KOSPInit();
    // initialisation of the event handler process with a NORMAL stack
	KOSAddApp(KOSEventCenterRun,NORMAL);
	// initialisation of inter process communication 
	KOSMessageInit();
	// initialisation of the event handler (FIFO queue of events)
	KOSEventInit();
	KOSInfo("OS is ready");
}

uint8_t ** KOSIdleMode(){
	return &mainStackPtr;
} 


void KOSRun(){
	KOSInfo("OS is launched");
	// start the timer
	KOSTimerStartMS(PERIODE_KERNEL,&KOSTimerTick);
}

 
 /*
 * Creates and initializes a stack for a new task. The stack should
 * look like after "save_execution_context()" - including the Program
 * Counter (PC) that points to the start of the task function.
 *
 * @param	entrypoint		Pointer to a function (initial PC value).
 *			*stackPointer	Pointer to the start of the stack. This is the
 *							memory location where the stack is initialized.
 *
 * @return	uint8_t*		Pointer to the top of the stack
 */

uint8_t* KOSInitializeStack(uint16_t entrypoint, uint8_t *stackPointer)
{
	/* Put some known values to the stack. This helps in debugging */
	*stackPointer = 0x11; //these 3 aren't used...
	stackPointer--;
	*stackPointer = 0x22;
	stackPointer--;
	*stackPointer = 0x33;
	stackPointer--;
	/* Place the task code entrypoint -pointer at the bottom of the stack */
	/* PCL - Program Counter Low byte */
	*stackPointer = (uint8_t) (entrypoint & (uint16_t)0x00ff);
	stackPointer--;
	/* PCH - Program Counter High byte */
	entrypoint >>= 8;
	*stackPointer = (uint8_t) (entrypoint & (uint16_t)0x00ff);
	stackPointer--;
	/* Create the rest of the stack as it would be after
	   "save_execution_context()" -macro */
	*stackPointer = 0x00; /* R0 */
	stackPointer--;
	*stackPointer = 0x80; /* SREG */
	stackPointer--;
	*stackPointer = 0x00; /* R1 */
	stackPointer--;
	*stackPointer = 0x02; /* R2 */
	stackPointer--;
	*stackPointer = 0x03; /* R3 */
	stackPointer--;
	*stackPointer = 0x04; /* R4 */
	stackPointer--;
	*stackPointer = 0x05; /* R5 */
	stackPointer--;
	*stackPointer = 0x06; /* R6 */
	stackPointer--;
	*stackPointer = 0x07; /* R7 */
	stackPointer--;
	*stackPointer = 0x08; /* R8 */
	stackPointer--;
	*stackPointer = 0x09; /* R9 */
	stackPointer--;
	*stackPointer = 0x10; /* R10 */
	stackPointer--;
	*stackPointer = 0x11; /* R11 */
	stackPointer--;
	*stackPointer = 0x12; /* R12 */
	stackPointer--;
	*stackPointer = 0x13; /* R13 */
	stackPointer--;
	*stackPointer = 0x14; /* R14 */
	stackPointer--;
	*stackPointer = 0x15; /* R15 */
	stackPointer--;
	*stackPointer = 0x16; /* R16 */
	stackPointer--;
	*stackPointer = 0x17; /* R17 */
	stackPointer--;
	*stackPointer = 0x18; /* R18 */
	stackPointer--;
	*stackPointer = 0x19; /* R19 */
	stackPointer--;
	*stackPointer = 0x20; /* R20 */
	stackPointer--;
	*stackPointer = 0x21; /* R21 */
	stackPointer--;
	*stackPointer = 0x22; /* R22 */
	stackPointer--;
	*stackPointer = 0x23; /* R23 */
	stackPointer--;
	*stackPointer = 0x24; /* R24 */
	stackPointer--;
	*stackPointer = 0x25; /* R25 */
	stackPointer--;
	*stackPointer = 0x26; /* R26 X */
	stackPointer--;
	*stackPointer = 0x27; /* R27 */
	stackPointer--;
	*stackPointer = 0x28; /* R28 Y */
	stackPointer--;
	*stackPointer = 0x29; /* R29 */
	stackPointer--;
	*stackPointer = 0x30; /* R30 Z */
	stackPointer--;
	*stackPointer = 0x31; /* R31 */
	stackPointer--;
	return stackPointer;	
}




int KOSFreeRam () {
  extern int __heap_start, *__brkval; 
  int v; 
  return (int) &v - (__brkval == 0 ? (int) &__heap_start : (int) __brkval); 
}




void KOSAddApp(void* functionEntryPoint, StackSize size)
{

	uint8_t* stackStart=(uint8_t*)0x08ff - stacksize_counter;
	if (size == SMALL)
	{
		stacksize_counter +=STACKSIZE_SMALL;
	}
	else if(size == NORMAL){
		stacksize_counter +=STACKSIZE_NORMAL;
	}
	else if(size == LARGE){
		stacksize_counter +=STACKSIZE_LARGE;
	}
	if (stacksize_counter>=KOSFreeRam())
	{
		HOSSafePrintInt(stacksize_counter);
		HOSSafePrintInt(KOSFreeRam());
		MOSError("The stack sizes requested cannot fit in the available RAM");
	}
	// initialization of the stack for this process
	uint8_t * end_stack = KOSInitializeStack((uint16_t)functionEntryPoint, stackStart);
    KOSPAdd(end_stack);
	return;
}


// clock interrupt
void KOSTimerTick()
{   
	/* Save the execution context to the stack */
	SAVE_CONTEXT();
	// update the array of sleep time
 	KOSPSleepUpdate(PERIODE_KERNEL);
 	KOSSechuler();
	/* Load an execution context from a stack */
	LOAD_NEXT_CONTEXT();
	/* Return from interrupt */
	asm volatile ( "reti" );
}

void KOSSwap(){
	// scheduler called outside a clock interrupt
	/* Save the execution context to the stack */
	SAVE_CONTEXT();
	KOSSechuler();
	/* Load an execution context from a stack */
	LOAD_NEXT_CONTEXT();
}

void KOSSwapEvent(){
	// the event handler can ask to the scheduler to be scheduled right away
	if (!KOSPEventProcessIsSleeping())
	{
		SAVE_CONTEXT();
		currentStackPtr=KOSPEvent();
		LOAD_NEXT_CONTEXT();
	}
}

void KOSSechuler(void)
{
 	currentStackPtr=KOSPNext();
}



void MOSSleep( uint16_t millis){
	MOSAtomicEnter();


	// if KERNEL_OPTIMISATION is set, the scheduler overhead will be anticipated (reduce delay error)
	#if KERNEL_OPTIMISATION == 1
	float millis_temp =  millis*PERIODE_KERNEL/(PERIODE_KERNEL+OVERHEAD_SCHEDULER)+1;
	uint16_t millis_opt = (uint16_t)millis_temp;
	KOSPSleep(millis_opt);

	#else
	KOSPSleep(millis);

	#endif

	KOSSwap();
	MOSAtomicExit();
}

void KOSInfo(string  info_message){
	MOSAtomicEnter();
	printf("=> INFO:    %s\n", info_message);
	MOSAtomicExit();
}


void MOSError(string  error_message){
	MOSAtomicEnter();
	printf("\nERROR: %s\n",error_message);



	// Mongoose goes to idle mode
	while(1){

	}
}

