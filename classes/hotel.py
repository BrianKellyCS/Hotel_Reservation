import csv
from classes.reservation import *

'''

Date of Code: 10/10/2022
Author: Brian Kelly
Description: A class used to represent a Hotel. Inherits from Reservation class.

Attributes:
    rooms : list (list of Room objects from totalRooms variable in Room class)
    guests : list (list of Guest objects from totalGuests variable in Guest class)
    reservations : list (list of Reservation objects from totalReservation variable in Reservation class)

Methods:
    initializeHotelData() 
        Initialize all hotel data from csv data. 
        Opens room_data.csv, guest_data.csv and reservation_data.csv files and reads data in proper format. 
        No return value

'''
class Hotel(Reservation):
    def __init__(self):
        self.rooms = Room.totalRooms #load rooms from data set
        self.guests = Guest.totalGuests #load customers from data set
        self.reservations = Reservation.totalReservations #load reservations from data set
    
    #Initialize all hotel data from csv data
    def initializeHotelData(self):
        room_data = list(csv.reader(open('data/room_data.csv')))
        guest_data = list(csv.reader(open('data/guest_data.csv')))
        reservation_data = list(csv.reader(open('data/reservation_data.csv')))


        #Bringing in data from CSV Files. index > 0 to ignore headers and bring data in correct data type
        for index,rooms in enumerate(room_data):
            if index > 0:
                Room(str(rooms[0]),int(rooms[1]),int(rooms[2]))
            else:
                Room(rooms[0],rooms[1],rooms[2])

        for index,guests in enumerate(guest_data):
            if index > 0:
                Guest(str(guests[0]),str(guests[1]),str(guests[2]),str(guests[3]),int(guests[4]))
            else:
                Guest(guests[0],guests[1],guests[2],guests[3],guests[4])

        for index,res in enumerate(reservation_data):
            if index > 0:
                Reservation(int(res[0]),datetime.strptime(res[1], '%m/%d/%Y'),datetime.strptime(res[2], '%m/%d/%Y'),int(res[3]),int(res[4]))
            else:
                Reservation(res[0],res[1],res[2],res[3],res[4])


    
    def managerReport(self): #2nd sprint
        pass












