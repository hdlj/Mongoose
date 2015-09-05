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

    

#include "timer.h"
#include "mongoose.h"

void (*timer_action) (void) = NULL;

volatile uint8_t timer_counter;
static uint16_t timer_ticks;
volatile uint16_t timer_overflow_number;


void KOSSetupTimer( uint16_t ms){
    float timerOverflow   = (ms/1000.0)/(MAX_16BIT*TIMER_PRESCALER/F_CPU)+1;
    timer_overflow_number = (uint16_t) timerOverflow;
    timer_ticks       =  (long)((timerOverflow - timer_overflow_number)*MAX_16BIT);
    
    TCNT1 = MAX_16BIT- timer_ticks; // adjust the timer counter to have the good delay
}


void KOSTimerStart(uint16_t ms){
    TCCR1B |= (1 << CS11); // prescaler of 8 -> 16Mhz/8 -> reduce frequency to 2MHz
    KOSSetupTimer(ms);
    TIMSK1  |= (1 << TOIE1);// enable overflow in order to trigger the interrupt
    timer_counter = 0;
}

void KOSTimerStartMS(uint16_t ms, void (*action) (void) ){
	timer_action=action;
    KOSTimerStart(ms);
}


ISR(TIMER1_OVF_vect){

    timer_counter++;
    if (timer_counter >= timer_overflow_number)
    {
        timer_counter=0;
        timer_action();
        TCNT1 = MAX_16BIT- timer_ticks;
    }

}





