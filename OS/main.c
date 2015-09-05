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



#include <mongoose/mongoose.h>
#include <MOSConfig.h>


 


int main(void)
{

	HOSSerialSetup();
	HOSDigitalInit();
	MOSAtomicEnter();
	KOSIntialize();
	/*  launch all the app */

	#ifdef APP1

	KOSAddApp(APP1,APP1_STACK);

	#endif 

	#ifdef APP2

	KOSAddApp(APP2,APP2_STACK);

	#endif

	#ifdef APP3

	KOSAddApp(APP3,APP3_STACK);

	#endif
	// block execution if no process is launched
	if (KOSPSize()==1){
		MOSError("No application is added to Mongoose");
	} 

	MOSAtomicExit();
	KOSRun();
	while(1){

	}
	
	/* The program should never exit the main function */
	return 0;
}


