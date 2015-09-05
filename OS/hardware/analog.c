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



#include "analog.h"


void HOSAnalogSetup()
{
    // set the reference voltage
    ADMUX |= (1<<REFS0);
    // prescaler of 128
    ADCSRA |= (1<<ADPS2);
    ADCSRA |= (1<<ADPS1);
    ADCSRA |= (1<<ADPS0);
    // enable ADC
    ADCSRA |= (1<<ADEN);    
}
uint16_t HOSAnalogRead(uint8_t ADCchannel)
{
    //select ADC channel
    ADMUX &= ~(1<<MUX0);
    ADMUX &= ~(1<<MUX1);
    ADMUX &= ~(1<<MUX2);
    ADMUX &= ~(1<<MUX3);
    switch (ADCchannel) {
        case 0 :
            break;
        case 1 :
            ADCSRA |= (1<<MUX0);
        case 2 :
            ADCSRA |= (1<<MUX1);
        case 3 :
            ADCSRA |= (1<<MUX1);
            ADCSRA |= (1<<MUX2);
    }  
    //Conversion mode : single
    ADCSRA |= (1<<ADSC);
    // ADSC will return to 0 when the conversion is done
    while( ADCSRA & (1<<ADSC) );
    // read the result
   return ADC;
}

