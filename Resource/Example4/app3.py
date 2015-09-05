#=============================================================================
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>'''
#
#    Date: 2015
#    based on this source code which has been written by Paul Bourke:
#    http://paulbourke.net/miscellaneous/dft/
#
#===============================================================================








import MOSFoundation
import math



def app3 (): 
	iRe =[] 
	iIm =[] 
	oRe =[] 
	oIm =[]
	while(True):
		for x in range (5):
			result = MOSReadChannel(0)
			iRe[x] = result
			iIm[x] = 0
			MOSAtomicEnter()
			DFT(iRe, iIm, oRe, oIm)
			MOSAtomicExit()


def intToFloat(n : int) -> float: 
	return n/1.0

def DFT(iRe : list, iIm : list, oRe :list, oIm: list): 
	n=5
	for w in range(n):
		oRe[w] = 0
		oIm[w] = 0 
		a = 0.0 
		cosa = 0.0 
		sina = 0.0
		for x in range(n):
			a = (2 * M_PI * w * x )/ intToFloat(n)
			cosa = cos(a)
			sina = sin(a)
			oRe[w] = oRe[w] + iRe[x] * cosa - iIm[x] * sina 
			oIm[w] = oIm[w] + iRe[x] * sina + iIm[x] * cosa
			oRe[w] = oRe[w]/n
			oIm[w] = oIm[w]/n