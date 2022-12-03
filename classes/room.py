import pandas as pd
from datetime import datetime

'''
Date of Code: 10/10/2022
Authors: Brian Kelly, Jesse Carrillo
Description: A class used to represent a room.
'''
class Room:
    '''
    Class Variables: 
        totalRooms: list (contains list of all rooms)
        roomChoices : list (contains list of different room types in hotel: Basic, Deluxe, Suite) 
    '''
    totalRooms = []
    roomChoices = ['Basic','Deluxe','Suite']

    def __init__(self,roomType="",roomNumber=0,roomPrice = 0):
        '''
        Attributes:
            roomType: str  (Type of room)
            roomNumber: int (Room number)
            roomPrice: int (Cost of room)
        '''
        self.roomType = roomType
        self.roomNumber = roomNumber
        self.roomPrice = roomPrice

        Room.totalRooms.append(self)

    def __str__(self):
        return f"Room #: {self.roomNumber} // Room Type: {self.roomType} // Room Price: {self.roomPrice}"
    

    def getRoom(self,roomNumber):
        '''Searches totalRooms list and Returns Room object'''
        for idx in Room.totalRooms:
            if roomNumber == idx.roomNumber:
                return idx
        return f'Room {roomNumber} not found'

    def searchRooms(self, roomType,startDate,endDate):
        '''
        Searches room by room type with selected date range. 
        Returns a list of room numbers that are available within the start and end date
        '''
        roomList = []
        startDate = datetime.strptime(startDate, '%Y-%m-%d').date()
        endDate = datetime.strptime(endDate, '%Y-%m-%d').date()
        if roomType in self.roomChoices:
            for idx in Room.totalRooms:
                if idx.roomType == roomType and self.isAvailableRoom(idx.roomNumber,startDate,endDate):
                    roomList.append(idx.roomNumber)

            return roomList


    def isAvailableRoom(self,roomNumber,*args):
        '''
        Checks availability for room number based on date(s) in parameter.
        Calls helper function checkDate() if one date is sent as parameter. checkDate returns a bool value
        Calls helper function checkDateRange() if a start and end date are sent as parameters. checkDateRange returns a bool value
        Method returns a boolean value of True or False depending on if the room is available or not.
        '''
        if len(args) == 1:
            return self.checkDate(roomNumber,args[0])

        elif len(args) == 2:
             return self.checkDateRange(roomNumber,args[0],args[1])           


    def checkDate(self,roomNumber,date):
        '''
        Helper function for isAvailableRoom
        Searches reservations for availability by room number with selected date
        Returns bool value. True if room is available on the date. False if not
        '''
        if type(date) == str:
            date = datetime.strptime(date, '%Y-%m-%d').date()

        for res in self.totalReservations[1:]:
            try:
                resStart = datetime.strptime(res.startDate, '%Y-%m-%d').date()
                resEnd = datetime.strptime(res.endDate, '%Y-%m-%d').date()
            except:
                resStart = res.startDate
                resEnd = res.endDate
            if str(res.roomNumber) == str(roomNumber):
                if (date < resStart) or (date >= resEnd):
                    continue
                else:
                    return False
        return True


    def checkDateRange(self,roomNumber,startDate,endDate):
        '''
        Helper function for isAvailableRoom
        Searches reservations for availability by room number with date range
        Returns bool value. True if room is available in date range, False if not.
        '''
        if type(startDate) == str:
            startDate = datetime.strptime(startDate, '%Y-%m-%d').date()
            endDate = datetime.strptime(endDate, '%Y-%m-%d').date()


        for res in self.totalReservations[1:]:
            try:
                resStart = datetime.strptime(res.startDate, '%Y-%m-%d').date()
                resEnd = datetime.strptime(res.endDate, '%Y-%m-%d').date()
            except:
                resStart = res.startDate
                resEnd = res.endDate
            if str(res.roomNumber) == str(roomNumber):
                if (startDate < resStart and endDate <= resStart) or (startDate >= resEnd and endDate > resEnd):
                    continue
                else:
                    return False
        return True


