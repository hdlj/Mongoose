#import "digital.h"
char getPort(uint8_t pin);
uint8_t getPin(uint8_t pin);

void MOSDigitalOn(uint8_t pin){
	if (getPort(pin)=='D')
	{
		PORTD |= _BV(getPin(pin));
	}
	else if (getPort(pin)=='B')
	{
		PORTB |= _BV(getPin(pin));
	}
}

void MOSDigitalOff(uint8_t pin){
	if (getPort(pin)=='D')
	{
		PORTD &= ~_BV(getPin(pin));
	}
	else if (getPort(pin)=='B')
	{
		PORTB &= ~_BV(getPin(pin));
	}
}

void MOSDigitalSetup(uint8_t pin){
	if (getPort(pin)=='D')
	{
		DDRD |= _BV(getPin(pin));
	}
	else if (getPort(pin)=='B')
	{
		DDRB |= _BV(getPin(pin));
	}
	MOSDigitalOff(pin);

}

uint8_t getPin(uint8_t pin){
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


char getPort(uint8_t pin){
	if (pin>=0 && pin<=7){
		return 'D';
	}
	if (pin>=8 && pin<=13){
		return 'B';
	}
	return 'A';
}
