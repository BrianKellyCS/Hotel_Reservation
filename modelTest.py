from classes.hotel import *
from datetime import date
'''
Author: Brian Kelly
Date: 11/22/2022
'''

#Initialize hotel and data
hotel = Hotel()

#Initialize a current user as the last user in guest list
currentGuest = hotel.guests[-1] 

#Search for rooms 
hotel.searchRooms("Basic",'2022-10-13','2022-10-16')

#Select available room
roomToReserve = hotel.rooms[1] 

#Create reservation
hotel.createReservation(currentGuest.guestID,'2022-10-13','2022-10-16',roomToReserve.roomNumber) 




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
hotel.editReservation('2022-10-13','2022-10-16',1,'437')


# Test making a guest with different names
guestTest = ["Mr", "Mister", "111-222-3333", "Mr.Tester@gmail.com"]
currentGuest = hotel.createGuest(guestTest)
print(currentGuest)

guestBadTest1 = ["", "Lastname", "111-222-3333", "Mr.Tester@gmail.com"]
guestBadTest2 = ["Firstname", "", "111-222-3333", "Mr.Tester@gmail.com"]
guestBadTest3 = ["Firstname", "Lastname", 111, "Mr.Tester@gmail.com"]
guestBadTest4 = ["Firstname", "Lastname", "111-222-3333", 3]

print("")
print(guestBadTest1)
currentGuest = hotel.createGuest(guestBadTest1)

print(guestBadTest2)
currentGuest = hotel.createGuest(guestBadTest2)

print(guestBadTest3)
currentGuest = hotel.createGuest(guestBadTest3)

print(guestBadTest4)
currentGuest = hotel.createGuest(guestBadTest4)
