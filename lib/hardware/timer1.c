
#include "timer1.h"

volatile uint8_t timer1_counter;
volatile uint16_t timer1_overflow_number;


// timer 1 is a 16 bits timer
void timer_1_init()
{

	/*TCCR1B |= (1 << CS11); // prescaler of 8 -> 16Mhz/8 -> reduce frequency to 2MHz
	TCNT1  = 0; // counter of timer 1 -> 0
	TIMSK1  |= (1 << TOIE1);// enable overflow in order to trigger the interrupt
	timer1_counter = 0;
	timer1_overflow_number = 15; //500 ms 
	*/
}

/*
ISR (TIMER1_OVF_vect)
{
	timer1_counter++;
	if (timer1_counter >= timer1_overflow_number)
	{
		timer1_counter = 0; // we reach the timer 
		printf("every two seconds\n");
	}

}
*/

/*
// timer1 overflow
ISR(TIMER1_OVF_vect) {
    printf("***** Timer1 Overflow *****\n");
}


// timer 0 overflow 
ISR(TIMER0_OVF_vect) {

	timer0_ticks++; //61 ticks -> 2 seconds 8.0 MHz
	if(timer0_ticks==30){
		printf(" %u seconds\n",seconds+1);
	}
	if (timer0_ticks==61)
	{
		timer0_ticks=0;
		seconds++;
		seconds++;
		printf("AND %u \n",seconds);
	}

}*/
