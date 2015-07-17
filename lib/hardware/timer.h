

#ifndef TIMER_H
#define TIMER_H


#include <avr/interrupt.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdarg.h>
#include "../hardware/serial.h"

#define F_CPU  16000000.0
#define TIMER_PRESCALER 8
#define MAX_16BIT 65536

void timer_start_ms (uint16_t ms, void (*action) (void));



#endif