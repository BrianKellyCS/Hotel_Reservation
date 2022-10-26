import random
from classes.guest import *
import csv



class Reservation(Guest):
    
    #Class variables
    totalReservations = []

    def __init__(self,guestID = None, startDate=None,endDate=None, roomNumber = None,reservationNumber = None):
        
        self.guestID = guestID
        self.reservationNumber = reservationNumber if reservationNumber != None else random.randint(1,500)#random.randint(1,500) if startDate != None else None #TO DO : method to assign better reservation number. ensure no repeat
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
        roomObj = self.returnRoomByNumber(roomNumber)
        try:
            if int(guestObj.guestStatus) == 1:
                print("\nGuest already has reservation.\n")
            else:
                newReservation = Reservation(guestObj.guestID,startDate,endDate,roomObj.roomNumber)
                guestObj.setGuestStatus(1)
                roomObj.setRoomStatus(1)
                print(f"Reservation successfully created for {guestObj.fName} {guestObj.lName} (Guest ID: {newReservation.guestID})\n")
                with open('data/reservation_data.csv', 'a',newline='') as stream:
                    writer = csv.writer(stream)
                    writer.writerow(newReservation)
                

        except Exception as e:
            print(e)
            newReservation = None
        
        
        

    def editReservation(self,guestObj,startDate,endDate,roomObj):
        pass


    def cancelReservation(self,reservationNumber):
        pass


    def emailReservation(self,reservationNumber):
        pass


    

    
    



    

    
    

