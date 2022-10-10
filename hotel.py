from init_data import *


class Hotel(Guest,Room):
    def __init__(self):
        self.rooms = Room.totalRooms #load rooms from data set
        self.guests = Guest.totalGuests #load customers from data set
        self.reservations = Reservation.totalReservations #load reservations from data set
    
    def managerReport(self): #2nd sprint
        pass



'''
#Basic Functionality


hotel = Hotel()

currentGuest = hotel.guests[2]

hotel.searchRooms("Basic") #Will be buttons in GUI, not entered text

roomToReserve = hotel.rooms[1] #Button in GUI to reserve the room selected

hotel.createReservation(currentGuest,"10/10/2020","10/13/2020",roomToReserve) #TO DO: calendar object in GUI to select dates. Parameters: (Guest object, Start Date, End Date, Room object)
print(currentGuest.reservation)




list = ["Bob", "job", "555-5555", "bobjob@yahoo.com"] #Comes from Guest Form
currentGuest = hotel.createGuest(list)
print(hotel.guests[-1])
#or
print(currentGuest)



'''




