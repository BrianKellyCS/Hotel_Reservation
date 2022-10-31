import random
from classes.guest import *
import csv
from datetime import datetime



class Reservation(Guest):
    
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
        return f"*Customer Reservation*\nGuest ID: {self.guestID}, // Reservation #: {self.reservationNumber}, // Start Date: {self.startDate}, // End Date: {self.endDate} // Room Number: {self.roomNumber}"


    def __iter__(self):
        return iter([self.guestID,self.startDate,self.endDate,self.roomNumber,self.reservationNumber])

    def createReservation(self,guestID,startDate,endDate,roomNumber):
        guestObj = self.returnGuestByID(guestID)
        roomObj = self.getRoom(roomNumber)
        try:

            newReservation = Reservation(guestObj.guestID,startDate,endDate,roomObj.roomNumber)
            print(f"Reservation successfully created for {guestObj.fName} {guestObj.lName} (Guest ID: {newReservation.guestID})\n")
            with open('data/reservation_data.csv', 'a',newline='') as stream:
                writer = csv.writer(stream)
                writer.writerow(newReservation)
                

        except Exception as e:
            print(e)
            newReservation = None
        
        
    def getReservation(self,roomNumber,dateToDisplay):
        #Ensures dateToDisplay in correct format
        if type(dateToDisplay) == str:
            dateToDisplay = datetime.strptime(dateToDisplay, '%m/%d/%Y')
        if not self.isAvailableRoom(roomNumber,dateToDisplay):
            for res in self.totalReservations:
                #Ensures dates being compared in correct format
                try:
                    resStart = datetime.strptime(res.startDate, '%m/%d/%Y')
                    resEnd = datetime.strptime(res.endDate, '%m/%d/%Y')
                except:
                    resStart = res.startDate
                    resEnd = res.endDate
                if str(res.roomNumber) == str(roomNumber):
                    if (dateToDisplay >= resStart) and (dateToDisplay < resEnd):
                        #Returns reservation for room number within specified date
                        return res
        else:
            return f'Room {roomNumber} is available'

    def editReservation(self,guestObj,startDate,endDate,roomObj):
        pass


    def cancelReservation(self,reservationNumber):
        pass


    def emailReservation(self,reservationNumber):
        pass


    

    
    



    

    
    

