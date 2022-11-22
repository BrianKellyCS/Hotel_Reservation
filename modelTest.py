from classes.hotel import *
from datetime import date
'''
Author: Brian Kelly
Date: 11/22/2022
'''

#Initialize hotel and data
hotel = Hotel()
hotel.initializeHotelData()

#Initialize a current user as the last user in guest list
currentGuest = hotel.guests[-1] 

#Search for rooms 
hotel.searchRooms("Basic","11/20/2022","11/22/2022")

#Select available room
roomToReserve = hotel.rooms[1] 

#Create reservation
hotel.createReservation(currentGuest.guestID,"11/10/2022","11/12/2022",roomToReserve.roomNumber) 




#Create new guest
#Assign new guest as current guest
list = ["Bob", "Gob", "555-5555", "bobgob@yahoo.com"]
currentGuest = hotel.createGuest(list)
print(currentGuest)

#Get Guest by guest ID
print(hotel.getGuestByID(17)) #returns Bob Gob
print(hotel.getGuestByID(35325)) #returns guest not found


#Get reservation by guest ID
print(hotel.getReservationByGuestID(156))

#Change reservation # 437 to new dates
hotel.editReservation(437,"10/20/2022","10/21/2022",1)
