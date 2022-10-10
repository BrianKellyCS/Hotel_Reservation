
from reservation import *


class Guest(Reservation):
    
    #Class variables
    totalGuests = []
    reservation = None

    
    def __init__(self, fName="No First Name", lName ="No Last Name", phone="No Phone", email="No Email", guestStatus =0, guestID = 0):
        self.fName = fName
        self.lName = lName
        self.phone = phone
        self.email = email
        self.guestID = guestID
        self.guestStatus = guestStatus
        

        Guest.totalGuests.append(self)

    
    def __str__(self):
        return f"Name: {self.fName} {self.lName} // guestID: {self.guestID} // Phone: {self.phone} // Email: {self.email} // Guest Status: {self.guestStatus}// Reservation #: {None if self.reservation == None else self.reservation.reservationNumber}"


    def assignGuestID(self, IDnum): #FINISH Assign guest an ID Number
        self.guestID = IDnum

    def createGuest(self, list): #Assigns guest their information from the form
        try:
            newGuest = Guest(list[0],list[1],list[2],list[3])
        except Exception as e:
            print(e)
            newGuest = None
        return newGuest

    
    def setGuestStatus(self,guestStatus):
        if int(guestStatus) == 0 or int(guestStatus) == 1:
            self.guestStatus = guestStatus
        else:
            print("\nERROR: Attempt to set Guest Status with invalid parameter.\n")
    



        


    

    
    

