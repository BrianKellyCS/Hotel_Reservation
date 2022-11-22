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

Class Variables: 
    totalReservations: list (contains list of all reservations)

Attributes:
    guestID: int  (ID number of guest who has the reservation)
    startDate: datetime (Starting date of reservation)
    endDate: datetime (End date of reservation)
    roomNumber: int (Room number on reservation)
    reservationNumber : int (Reservation number)

Methods:
    createReservation(guestID : int, startDate : datetime, endDate : datetime, roomNumber : int) 
        Creates a new reservation. 
        Ensures that the room is available before creating new reservation. 
        Displays a message if successful and appends new reservation to reservation_data.csv
        No Return value

    getReservationByRoom(roomNumber : int, dateToDisplay : datetime) 
        Returns reservation by room number or a message telling the user that the room is available
        Checks availability of room by calling isAvailableRoom() method from Room class. 
        If it is not available, then the method searches totalReservations list to return the reservation object.

    getReservationByResNum(reservationNumber : int) 
        Returns reservation object by searching totalReservations list for the reservation number 
        or a null value if no reservation found. 

    getReservationByGuestID(guestID : int) 
        Returns a list of reservation objects (since it is possible for a guest to have more than one reservation) by searching totalReservations by guest ID. 
        If none found, returns a string telling the user there were no reservations for the guest.

    editReservation(reservationNumber : int, newStartDate : datetime, newEndDate : datetime, roomNumber) 
        Changes dates or room number for reservation. 
        Starts by saving original reservation information, then checks availability by calling isAvailableRoom method from Room class. 
        If it is available, then method updates reservation_data.csv with new information. If it is not available, the original reservation information is saved. 
        No Return value

'''
class Reservation(Guest, Room):
    
    #Class variables
    totalReservations = []

    def __init__(self,guestID = None, startDate=None,endDate=None, roomNumber = None,reservationNumber = None):
        
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

    #Creates a new reservation
    def createReservation(self,guestID,startDate,endDate,roomNumber):
        guestObj = self.getGuestByID(guestID)   
        roomObj = self.getRoom(roomNumber)

        #Check if room is available before creating reservation
        if(not self.isAvailableRoom(roomNumber,startDate,endDate)):
            print(f'Room {roomNumber} is not available between {startDate} and {endDate}')
            return
        
        #Continue to create reservation
        try:
            newReservation = Reservation(guestObj.guestID,startDate,endDate,roomObj.roomNumber)
            print(f"Reservation successfully created for {guestObj.fName} {guestObj.lName} (Guest ID: {newReservation.guestID})\n")
            with open('data/reservation_data.csv', 'a',newline='') as stream:
                writer = csv.writer(stream)
                writer.writerow(newReservation)
                

        except Exception as e:
            print(e)
            newReservation = None
        
    #Returns reservation by room number  
    def getReservationByRoom(self,roomNumber,dateToDisplay):
        #Ensures dateToDisplay in correct format
        if type(dateToDisplay) == str:
            dateToDisplay = datetime.strptime(dateToDisplay, '%m/%d/%Y')
        
        #If room number is not available for selected date
        if not self.isAvailableRoom(roomNumber,dateToDisplay):
            
            #Search reservations
            for res in self.totalReservations:
                #Ensures dates being compared in correct format
                try:
                    resStart = datetime.strptime(res.startDate, '%m/%d/%Y')
                    resEnd = datetime.strptime(res.endDate, '%m/%d/%Y')
                except:
                    resStart = res.startDate
                    resEnd = res.endDate
                
                if res.roomNumber == roomNumber:
                    
                    #If room number is found and date is within the reservation date range
                    if (dateToDisplay >= resStart) and (dateToDisplay < resEnd):
                        
                        #Returns reservation for room number
                        return res
        else:
            return f'Room {roomNumber} is available'

    
    #Returns reservation by reservation number
    def getReservationByResNum(self,reservationNumber):
        for res in self.totalReservations:
            if res.reservationNumber == reservationNumber:
                return res
        else:
            print(f'No Reservation found for {reservationNumber}')
            return None

    #Return reservation by Guest ID
    def getReservationByGuestID(self,guestID):
        reservationList = []

        #Searches reservations for guest
        for res in self.totalReservations:
            if res.guestID == guestID:
                reservationList.append(str(res))

        #check if none found
        if(len(reservationList) == 0):
            return f'No reservations found for guest {guestID}'

        #Return reservations for guest
        return reservationList

        
    #Change dates or room number for reservation
    def editReservation(self, reservationNumber, newStartDate, newEndDate, roomNumber):
        selectedRes = self.getReservationByResNum(reservationNumber)
        
        #Save original reservation information incase dates for room are not available
        originalStart = selectedRes.startDate
        originalEnd = selectedRes.endDate
        originalRoom = selectedRes.roomNumber
        if selectedRes != None:
            #If it is a valid reservation number
            #Clear values in selected reservation
            selectedRes.startDate = None
            selectedRes.endDate = None
            selectedRes.roomNumber = None             
             
            if self.isAvailableRoom(roomNumber,newStartDate,newEndDate):
                #Update array
                selectedRes.startDate = newStartDate
                selectedRes.endDate = newEndDate
                selectedRes.roomNumber = roomNumber

                #Update in CSV File
                df = pd.read_csv('data/reservation_data.csv')
                filt = (df['reservationNumber'] == selectedRes.reservationNumber)
                df.loc[filt,'startDate'] = selectedRes.startDate
                df.loc[filt,'endDate'] = selectedRes.endDate
                df.loc[filt,'roomNumber'] = selectedRes.roomNumber
                df.to_csv('data/reservation_data.csv',index = False)

            else:
                #Save original information
                selectedRes.startDate = originalStart
                selectedRes.endDate = originalEnd
                selectedRes.roomNumber = originalRoom   


    #Cancels reservation by reservationNumber 
    def cancelReservation(self,reservationNumber):
        pass

    #Email reservation confirmation to guest
    def emailReservation(self,reservationNumber):
        pass


    

    
    



    

    
    

