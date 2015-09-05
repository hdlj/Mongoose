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

    
#include "type.h"
#include "mongoose.h"
    




void listAddElement(uint16_t element, CList * list){
    if (list->size>=MAX_SIZE) {
        MOSError("List overflow");
        return;
    }
    list->data[list->size]=element;
    list->size++;
}


uint16_t listElementAt(uint8_t position, CList* list){
    if (position>=list->size) {
        MOSError("NOT ACCESSIBLE");
        return 0;
    }
    return list->data[position];
}


void listSetElementAt(uint8_t position, CList* list, uint16_t data){
    if (position>=MAX_SIZE) {
        return;
    }
    if(position+1>list->size){
        list->size=position+1;
    }
    else{
        list->size++;
    }
    list->data[position]=data;
}
