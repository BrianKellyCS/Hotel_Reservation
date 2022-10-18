import csv
from classes.guest import *
from classes.room import *



class Hotel(Guest,Room):
    def __init__(self):
        self.rooms = Room.totalRooms #load rooms from data set
        self.guests = Guest.totalGuests #load customers from data set
        self.reservations = Reservation.totalReservations #load reservations from data set
    
    def initializeHotelData(self):
        room_data = list(csv.reader(open('data/room_data.csv')))
        guest_data = list(csv.reader(open('data/guest_data.csv')))
        reservation_data = list(csv.reader(open('data/reservation_data.csv')))

        for rooms in room_data:
            try:
                r = Room()
                r.roomType = rooms[0]
                r.roomNumber = rooms[1]
                try:
                    r.roomStatus = int(rooms[2])
                except:
                    r.roomStatus = rooms[2]
                r.roomPrice = rooms[3]
            except Exception as e:
                print(e)
        for guests in guest_data:
            Guest(guests[0],guests[1],guests[2],guests[3],guests[4])

        for res in reservation_data:
            Reservation()
    
    def managerReport(self): #2nd sprint
        pass




'''#Basic Functionality


hotel = Hotel()
hotel.initializeHotelData()

currentGuest = hotel.guests[2]

hotel.searchRooms("Basic") #Will be buttons in GUI, not entered text

roomToReserve = hotel.rooms[1] #Button in GUI to reserve the room selected

hotel.createReservation(currentGuest,"10/10/2020","10/13/2020",roomToReserve) #TO DO: calendar object in GUI to select dates. Parameters: (Guest object, Start Date, End Date, Room object)
print(currentGuest.reservation)




list = ["Bob", "job", "555-5555", "bobjob@yahoo.com"] #Comes from Guest Form
currentGuest = hotel.createGuest(list)
print(hotel.guests[-1])
#or
print(currentGuest)'''








