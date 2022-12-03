import random
from classes.guest import *
from classes.room import *
import csv
import pandas as pd
from datetime import datetime


'''
Date of Code: 10/10/2022
Author: Brian Kelly
Description: A class used to represent a Reservation. Inherits from Guest and Room class
'''
class Reservation(Guest, Room):
    
    #Class variables
    totalReservations = []

    def __init__(self,guestID = None, startDate=None,endDate=None, roomNumber = None,reservationNumber = None):
        '''
        Attributes:
            guestID: int  (ID number of guest who has the reservation)
            startDate: datetime (Starting date of reservation)
            endDate: datetime (End date of reservation)
            roomNumber: int (Room number on reservation)
            reservationNumber : int (Reservation number)
        '''
        self.guestID = guestID
        self.reservationNumber = reservationNumber if reservationNumber != None else random.randint(1,500)#TO DO : method to assign better reservation number. ensure no repeat
        self.startDate = startDate
        self.endDate = endDate
        self.roomNumber = roomNumber

        Reservation.totalReservations.append(self)
        
    def __str__(self):
        return f"Customer Reservation: Guest ID: {self.guestID}, // Reservation #: {self.reservationNumber}, // Start Date: {self.startDate}, // End Date: {self.endDate} // Room Number: {self.roomNumber}"


    def __iter__(self):
        return iter([self.guestID,self.startDate,self.endDate,self.roomNumber,self.reservationNumber])

    def createReservation(self,guestID,startDate,endDate,roomNumber):
        '''
        Creates a new reservation. 
        Ensures that the room is available before creating new reservation. 
        Displays a message if successful and appends new reservation to reservation_data.csv
        Returns new reservation object if successful or None type if there was an error
        '''
        try:
            guestObj = self.getGuestByID(guestID)   
            roomObj = self.getRoom(roomNumber)


            startDate = datetime.strptime(startDate, '%Y-%m-%d').date()
            endDate = datetime.strptime(endDate, '%Y-%m-%d').date()


            if(not self.isAvailableRoom(roomNumber,startDate,endDate)):
                print(f'Room {roomNumber} is not available between {startDate} and {endDate}')
                return None
        


            newReservation = Reservation(guestObj.guestID,startDate,endDate,roomObj.roomNumber)
            with open('data/reservation_data.csv', 'a',newline='') as stream:
                writer = csv.writer(stream)
                writer.writerow(newReservation)
            return newReservation
                

        except Exception as e:
            print(e)
            newReservation = None
        
  
    def getReservationByRoom(self,roomNumber,dateToDisplay):
        '''
        Returns a string. reservation information by room number or a message telling the user that the room is available
        Checks availability of room by calling isAvailableRoom() method from Room class. 
        Searches totalReservations list to return the reservation information.
        '''

        if type(dateToDisplay) == str:
            dateToDisplay = datetime.strptime(dateToDisplay, '%Y-%m-%d').date()
        

        if not self.isAvailableRoom(roomNumber,dateToDisplay):
            for res in self.totalReservations:
                try:
                    resStart = datetime.strptime(res.startDate, '%Y-%m-%d').date()
                    resEnd = datetime.strptime(res.endDate, '%Y-%m-%d').date()
                except:
                    resStart = res.startDate
                    resEnd = res.endDate
                
                if res.roomNumber == roomNumber:
                    if (dateToDisplay >= resStart) and (dateToDisplay < resEnd):
                        return f'Reservation #: {res.reservationNumber}\nRoom #: {res.roomNumber}\nGuest ID: {res.guestID}\nStart Date: {res.startDate}\nEnd Date: {res.endDate}'

        else:
            return f'Room {roomNumber} is available'

    
    def getReservationByResNum(self,reservationNumber):
        '''
        Returns reservation object by searching totalReservations list for the reservation number 
        or a null value if no reservation found. 
        '''
        for res in self.totalReservations:
            if res.reservationNumber == reservationNumber:
                return res
        else:
            print(f'No Reservation found for {reservationNumber}\n')
            return None


    def getReservationByGuestID(self,guestID):
        '''
        Returns a list of reservation objects (since it is possible for a guest to have more than one reservation) by searching totalReservations by guest ID. 
        If none found, returns None.
        '''
        reservationList = []

        for res in self.totalReservations[1:]:
            if res.guestID == guestID:
                reservationList.append(list(res))

        if(len(reservationList) == 0):
            return None

        return reservationList

        
    def editReservation(self, newStartDate, newEndDate, roomNumber, reservationNumber):
        '''
        Changes dates or room number for reservation. 
        Starts by saving original reservation information, then checks availability by calling isAvailableRoom method from Room class. 
        If it is available, then method updates reservation_data.csv with new information. If it is not available, the original reservation information is saved. 
        No Return value
        '''
        selectedRes = self.getReservationByResNum(reservationNumber)
        if selectedRes == None:
            return
        
        originalStart = selectedRes.startDate
        originalEnd = selectedRes.endDate
        originalRoom = selectedRes.roomNumber       
             
        if self.isAvailableRoom(roomNumber,newStartDate,newEndDate):
            selectedRes.startDate = newStartDate
            selectedRes.endDate = newEndDate
            selectedRes.roomNumber = roomNumber


            df = pd.read_csv('data/reservation_data.csv')
            filt = (df['reservationNumber'] == selectedRes.reservationNumber)
            df.loc[filt,'startDate'] = selectedRes.startDate
            df.loc[filt,'endDate'] = selectedRes.endDate
            df.loc[filt,'roomNumber'] = selectedRes.roomNumber
            df.to_csv('data/reservation_data.csv',index = False)

        else:
            print('invalid date')
            selectedRes.startDate = originalStart
            selectedRes.endDate = originalEnd
            selectedRes.roomNumber = originalRoom   


    def cancelReservation(self,reservationNumber):
        '''
        Cancels reservation by reservationNumber
        Searches for reservation in reservation_data.csv. Removes row containing reservation if found
        Updates CSV File
        Returns string upon successfull cancelled reservation
        '''
        reservationToCancel = self.getReservationByResNum(reservationNumber)

        if reservationToCancel == None:
            return
   
        lines = list()
        with open('data/reservation_data.csv','r') as readFile:
            reader = csv.reader(readFile)
            for row in reader:
                lines.append(row)
                for field in row:
                    if field == str(reservationToCancel.reservationNumber):
                        lines.remove(row)


        with open('data/reservation_data.csv','w',newline = '') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(lines)
        
        return f'Successfully cancelled reservation: {reservationToCancel.reservationNumber}'

    #Email reservation confirmation to guest
    def emailReservation(self,reservationNumber):
        pass


    

    
    



    

    
    

