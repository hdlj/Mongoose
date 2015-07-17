#include "type.h"



string MOSStringConcatenate(string str1,string str2){
	string result;
    result = calloc(strlen(str1), sizeof(char));
    strcpy(result,str1);
    strcat(result,str2);
	return result;
}