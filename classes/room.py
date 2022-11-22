import pandas as pd
from datetime import datetime

'''

Date of Code: 10/10/2022
Authors: Brian Kelly, Jesse Carrillo
Description: A class used to represent a room.

Class Variables: 
    totalRooms: list (contains list of all rooms)
    roomChoices : list (contains list of different room types in hotel: Basic, Deluxe, Suite) 

Attributes:
    roomType: str  (Type of room)
    roomNumber: int (Room number)
    roomPrice: int (Cost of room)

Methods:
    getRoom(roomNumber : int) 
        Searches totalRooms list and Returns Room object

    searchRooms(roomType : str, startDate : datetime, endDate : datetime) 
        Searches room by room type with selected date range. 
        Returns a list of room numbers that are available within the start and end date

    isAvailableRoom(roomNumber : int, *args : datetime (1 or 2 dates)) 
        Checks availability for room number based on date(s) in parameter.
        Calls helper function checkDate() if one date is sent as parameter. checkDate returns a bool value
        Calls helper function checkDateRange() if a start and end date are sent as parameters. checkDateRange returns a bool value
        Method returns a boolean value of True or False depending on if the room is available or not.

    checkDate(roomNumber : int, date : datetime)
        Helper function for isAvailableRoom
        Searches reservations for availability by room number with selected date
        Returns bool value. True if room is available on the date. False if not

    checkDateRange(roomNumber: int, startDate : datetime, endDate : datetime)
        Helper function for isAvailableRoom
        Searches reservations for availability by room number with date range
        Returns bool value. True if room is available in date range, False if not.

'''
class Room:
    
    #Class variables
    totalRooms = []
    roomChoices = ['Basic','Deluxe','Suite']

    def __init__(self,roomType="",roomNumber=0,roomPrice = 0):
        self.roomType = roomType
        self.roomNumber = roomNumber
        self.roomPrice = roomPrice

        Room.totalRooms.append(self)

    def __str__(self):
        return f"Room #: {self.roomNumber} // Room Type: {self.roomType} // Room Price: {self.roomPrice}"
    
    #Returns room
    def getRoom(self,roomNumber):
        for idx in Room.totalRooms:
            if roomNumber == idx.roomNumber:
                return idx
        return f'Room {roomNumber} not found'

    #Searches rooms by room type with selected date range
    def searchRooms(self, roomType,startDate,endDate):
        roomList = []
        startDate = datetime.strptime(startDate, '%m/%d/%Y')
        endDate = datetime.strptime(endDate, '%m/%d/%Y')
        if roomType in self.roomChoices:
            
            #Gathers all available rooms of room type within selected dates
            for idx in Room.totalRooms:
                if idx.roomType == roomType and self.isAvailableRoom(idx.roomNumber,startDate,endDate):
                    roomList.append(idx.roomNumber)

            return roomList

    #Checks availability for room number based off date selected
    #Handles dates with *args, so function can be used for a single date or date range
    def isAvailableRoom(self,roomNumber,*args):

        if len(args) == 1:
            return self.checkDate(roomNumber,args[0])

        elif len(args) == 2:
             return self.checkDateRange(roomNumber,args[0],args[1])           

    #Helper function for isAvailableRoom
    #Searches reservations for availability by room number with selected date
    def checkDate(self,roomNumber,date):

        if type(date) == str:
            date = datetime.strptime(date, '%m/%d/%Y')

        for res in self.totalReservations[1:]: #starting at index 1 (index 0 is header)
            #Try block ensures that the dates being compared are dateTime
            try:
                resStart = datetime.strptime(res.startDate, '%m/%d/%Y')
                resEnd = datetime.strptime(res.endDate, '%m/%d/%Y')
            except:
                resStart = res.startDate
                resEnd = res.endDate
            if str(res.roomNumber) == str(roomNumber):
                if (date < resStart) or (date >= resEnd):
                    continue
                else:
                    return False
        return True


    #Helper function for isAvailableRoom
    #Searches reservations for availability by room number with date range
    def checkDateRange(self,roomNumber,startDate,endDate):

        if type(startDate) == str:
            startDate = datetime.strptime(startDate, '%m/%d/%Y')
            endDate = datetime.strptime(endDate, '%m/%d/%Y')


        for res in self.totalReservations[1:]: #starting at index 1 (index 0 is header)
            #Try block ensures that the dates being compared are dateTime
            try:
                resStart = datetime.strptime(res.startDate, '%m/%d/%Y')
                resEnd = datetime.strptime(res.endDate, '%m/%d/%Y')
            except:
                resStart = res.startDate
                resEnd = res.endDate
            if str(res.roomNumber) == str(roomNumber):
                if (startDate < resStart and endDate <= resStart) or (startDate >= resEnd and endDate > resEnd):
                    continue
                else:
                    return False
        return True


