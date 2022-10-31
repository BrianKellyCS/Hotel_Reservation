import pandas as pd
from datetime import datetime
import PySimpleGUI as sg
from Images64 import * # A Seperate python file filled with Base64 strings of our images to make it easier to manage

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
    
    
    def getRoom(self,roomNumber):
        for idx in Room.totalRooms:
            if str(roomNumber) == str(idx.roomNumber):
                return idx
        return f'Room {roomNumber} not found'

    
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

    #Handles dates with *args, so function can be used for variable number of arguments:  2  for search rooms (start Date, endDate) and 1 for display rooms (date)
    def isAvailableRoom(self,roomNumber,*args):
        isAvailable = True
        if len(args) == 2:
            startDate = args[0]
            endDate = args[1]

            if type(startDate) == str:
                startDate = datetime.strptime(startDate, '%m/%d/%Y')
                endDate = datetime.strptime(endDate, '%m/%d/%Y')


            #Removes rooms with conflicting reservations
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
                        isAvailable = False
                        return isAvailable
            return isAvailable
        elif len(args) == 1:
            date = args[0]

            if type(date) == str:
                date = datetime.strptime(date, '%m/%d/%Y')

            #Removes rooms with conflicting reservations
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
                        isAvailable = True
                    else:
                        isAvailable = False
                        return isAvailable
            return isAvailable

    

    
        '''def filterByDates(self,roomList,startDate,endDate):

        #Removes rooms with conflicting reservations
        for idx,res in enumerate(self.totalReservations[1:]): #starting at index 1 (index 0 is header)
            
            #Try block ensures that the dates being compared are dateTime
            try:
                resStart = datetime.strptime(res.startDate, '%m/%d/%Y')
                resEnd = datetime.strptime(res.endDate, '%m/%d/%Y')
            except:
                resStart = res.startDate
                resEnd = res.endDate
            if (startDate < resStart and endDate <= resStart) or (startDate >= resEnd and endDate > resEnd):
                print('Room: ',res.roomNumber, 'Res #: ',res.reservationNumber,' kept')
            else:
                try:
                    roomList.remove(res.roomNumber)
                except Exception as e:
                    pass
        return roomList'''

