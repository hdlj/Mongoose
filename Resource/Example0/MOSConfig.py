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
# MOSConfig.py
# Declare here what application to launch
# with Mongoose and the corresponding stack
# size (SMALL, NORMAL or LARGE) 
#



APPLICATIONS = {
	"app1":{
		"startFunction" : "app1", "stackSize": "NORMAL"
	},
	"app2":{
		"startFunction" : "", "stackSize": ""
	},
	"app3":{
		"startFunction" : "",
		"stackSize": "" 
	}
}

