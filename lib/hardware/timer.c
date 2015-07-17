

#include "timer.h"
#include <avr/io.h>

void (*timer_action) (void) = NULL;

volatile uint8_t timer_counter;
volatile uint16_t timer_overflow_number;

void setupTimer( uint16_t ms){
    float timerOverflow   = (ms/1000.0)/(MAX_16BIT*TIMER_PRESCALER/F_CPU)+1;
    timer_overflow_number = (uint16_t) timerOverflow;
    uint16_t timer_ticks       =  (long)((timerOverflow - timer_overflow_number)*MAX_16BIT);
    
    TCNT1 = MAX_16BIT- timer_ticks;
}


void timer_start(uint16_t ms){
    TCCR1B |= (1 << CS11); // prescaler of 8 -> 16Mhz/8 -> reduce frequency to 2MHz
    setupTimer(ms);
    TIMSK1  |= (1 << TOIE1);// enable overflow in order to trigger the interrupt
    timer_counter = 0;
}

void timer_start_ms (uint16_t ms, void (*action) (void) ){
	timer_action=action;
    timer_start (ms);
}


ISR(TIMER1_OVF_vect){/*timer 1 interrupt service routine */

    timer_counter++;
    if (timer_counter >= timer_overflow_number)
    {
        
        timer_counter=0;
        timer_action();
    }

}