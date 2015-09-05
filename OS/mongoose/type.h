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



#ifndef TYPE_H
#define TYPE_H

#include <string.h>
#include <stdint.h>

typedef char* string;
#define MAX_SIZE  5

typedef struct CList{
    uint16_t data[MAX_SIZE];
    uint8_t  size;
    
} CList;


uint16_t listElementAt(uint8_t position, CList* list);
void listAddElement(uint16_t element, CList * list);
void listSetElementAt(uint8_t position, CList* list, uint16_t data);
#endif
