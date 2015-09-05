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
#
#===============================================================================


#
# MOSApi.py
# Declare here operating system functions
# which can be called by applications
# It maps function name to their return type
# Only float , uint8 t , uint16 t , string and CList can be used


MONGOOSE = {}
# Mongoose functions
MONGOOSE["MOSSleep"]        = "void"
MONGOOSE["MOSAtomicEnter"]  = "void"
MONGOOSE["MOSAtomicExit"]   = "void"
MONGOOSE["MOSError"]        = "void"
MONGOOSE["MOSSendMessage"]  = "void"
MONGOOSE["MOSReadChannel"]  = "uint16_t"

#....

