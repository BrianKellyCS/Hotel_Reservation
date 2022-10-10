from classes.room import *
from classes.guest import *
from classes.reservation import *
import csv

def getData():
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

getData()
