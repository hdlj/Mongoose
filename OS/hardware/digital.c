
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


#import "digital.h"


char    HOSDGetPort(uint8_t pin);
uint8_t HOSDGetPin(uint8_t pin);
uint8_t HOSDGetInterrupt(uint8_t pin);
uint8_t HOSDGetPinInput(uint8_t pin);
void 	HOSDigitalInterrupt();

#define NB_DIGITAL 13

volatile bool digitalInput[NB_PIN];
volatile bool digitalState[NB_PIN];
listener action[NB_PIN];

void HOSDigitalInit(){
	uint8_t index ;
	for ( index = 0; index <NB_PIN ; index++)
	{
		digitalInput[index] = false;
		digitalState[index] = true;
	}
}


void HOSDigitalListen(uint8_t pin, void * listener){
	if (HOSDGetPort(pin) == 'D')
	{
		// setup the interrupt on port D with the good pin
		DDRD  &= ~_BV(HOSDGetPin(pin));
		PORTD |= _BV(HOSDGetPin(pin));
		// at each interrupt, this pin will be check in order to trigger the listener
		// In fact, ports cna share the same interrupt vector
		digitalInput[pin] = true;
		PCICR |= _BV(PCIE2);
    	PCMSK2 |= _BV(HOSDGetInterrupt(pin));

    	if (listener != NULL)
    	{
    		// add the listener to the corresponding pin
    		action[pin] = listener;
    	}
    	
	}
}



void HOSDigitalInterrupt(){
	uint8_t i;
    
    // find wich port has been triggered
	for ( i = 2; i < NB_PIN; ++i)
	{
		if (digitalInput[i] && bit_is_clear(PIND, HOSDGetPinInput(i)) && !(digitalState[i])){
			digitalState[i] = true;
			// send the corresponding listener to the event handler process
			MOSEventReceived(action[i]);
			return;
		}
		else{
			if (bit_is_set(PIND, HOSDGetPinInput(i))) {
	        	digitalState[i] = false;
	    	}
		}
	}
}


ISR (PCINT2_vect)
{
	// interrupt vector for port D
	HOSDigitalInterrupt();
}


void HOSDigitalOn(uint8_t pin){
	// turn on the pin 
	if (HOSDGetPort(pin)=='D')
	{
		PORTD |= _BV(HOSDGetPin(pin));
	}
	else if (HOSDGetPort(pin)=='B')
	{
		PORTB |= _BV(HOSDGetPin(pin));
	}
}

void HOSDigitalOff(uint8_t pin){
	// turn off the pin
	if (HOSDGetPort(pin)=='D')
	{
		PORTD &= ~_BV(HOSDGetPin(pin));
	}
	else if (HOSDGetPort(pin)=='B')
	{
		PORTB &= ~_BV(HOSDGetPin(pin));
	}
}

void HOSDigitalSetup(uint8_t pin){
	// setup the pin 
	if (HOSDGetPort(pin)=='D')
	{
		DDRD |= _BV(HOSDGetPin(pin));
	}
	else if (HOSDGetPort(pin)=='B')
	{
		DDRB |= _BV(HOSDGetPin(pin));
	}
	HOSDigitalOff(pin);

}



uint8_t HOSDGetPin(uint8_t pin){
	switch (pin) {
		case 0 :
			return PORTD0;
		case 1 :
			return PORTD1;
		case 2 :
			return PORTD2;
		case 3 :
			return PORTD3;
		case 4 :
			return PORTD4;
		case 5 :
		 	return PORTD5;
		case 6 :
			return PORTD6;
		case 7 : 
			return PORTD7;
		case 8 :
			return PORTB0;
		case 9 : 
			return PORTB1;
		case 10 :
			return PORTB2;
		case 11 :
			return PORTB3;
		case 12 :
			return PORTB4;
		case 13 :
			return PORTB5;
	}
}

uint8_t HOSDGetInterrupt(uint8_t pin){
	switch (pin) {
		case 0 :
			return PCINT16;
		case 1 :
			return PCINT17;
		case 2 :
			return PCINT18;
		case 3 :
			return PCINT19;
		case 4 :
			return PCINT20;
		case 5 :
		 	return PCINT21;
		case 6 :
			return PCINT22;
		case 7 : 
			return PCINT23;
	}
}


uint8_t HOSDGetPinInput(uint8_t pin){
	switch (pin) {
		case 0 :
			return PIND0;
		case 1 :
			return PIND1;
		case 2 :
			return PIND2;
		case 3 :
			return PIND3;
		case 4 :
			return PIND4;
		case 5 :
		 	return PIND5;
		case 6 :
			return PIND6;
		case 7 : 
			return PIND7;
	}
}





char HOSDGetPort(uint8_t pin){
	if (pin>=0 && pin<=7){
		return 'D';
	}
	if (pin>=8 && pin<=13){
		return 'B';
	}
	return 'A';
}
