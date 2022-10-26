import csv
from classes.guest import *
from classes.room import *
from classes.reservation import *


class Hotel(Room,Reservation):
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
            Guest(guests[0],guests[1],guests[2],guests[3],guests[4],guests[5])

        for idx,res in enumerate(reservation_data):
            if idx > 0:
                Reservation(res[0],datetime.strptime(res[1], '%m/%d/%Y'),datetime.strptime(res[2], '%m/%d/%Y'),res[3],res[4])
            else:
                Reservation(res[0],res[1],res[2],res[3],res[4])


    
    def managerReport(self): #2nd sprint
        pass




'''#Basic Functionality


hotel = Hotel()
hotel.initializeHotelData() #fetch data from csv files

currentGuest = hotel.guests[-1] #assign a guest from guest data (-1 index is the last guest in list)

hotel.searchRooms("Basic") #Will be buttons in GUI , not entered text
roomToReserve = hotel.rooms[1] #Button in GUI to reserve the room selected

#parameters for createReservation (guestID, startDate, endDate, roomNumber)
hotel.createReservation(currentGuest.guestID,"10/10/2020","10/13/2020",roomToReserve.roomNumber) 

#example creating guest from guest form
list = ["Bob", "job", "555-5555", "bobjob@yahoo.com"] #Comes from Guest Form
currentGuest = hotel.createGuest(list)
print(currentGuest) #or print(hotel.guests[-1]) 

#get guest by ID
print(hotel.returnGuestByID(17)) #returns Bob job

print(hotel.reservations[-1]) #prints latest reservation created''' 









