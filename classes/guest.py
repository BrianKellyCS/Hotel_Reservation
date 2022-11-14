import pandas as pd
import csv

import os
from pathlib import Path
DATA_PATH = Path(__file__).parents[1] / "./data/"
GUEST_FILE_PATH = os.path.join(DATA_PATH,"guest_data.csv")

class Guest():
    
    #Class variables
    totalGuests = []


    
    def __init__(self, fName="No First Name", lName ="No Last Name", phone="No Phone", email="No Email", guestID = 0):
        self.fName = fName
        self.lName = lName
        self.phone = phone
        self.email = email
        self.guestID = guestID
        

        Guest.totalGuests.append(self)

    
    def __str__(self):
        return f"Name: {self.fName} {self.lName} // guestID: {self.guestID} // Phone: {self.phone} // Email: {self.email}"#// Reservation #: {None if self.reservation == None else self.reservation.reservationNumber}"

    def __iter__(self):
        return iter([self.fName,self.lName,self.phone,self.email,self.guestID,])

    def assignGuestID(self,id): 
        isValid = 1
        
        for idx in Guest.totalGuests:
            if str(id) == str(idx.guestID):
                isValid = 0
        if isValid == 1:
            self.guestID = id
        else:
            self.assignGuestID(int(id)+1) #increment number until valid

    
    def returnGuestByID(self,id):
        found = 0
        for idx in Guest.totalGuests:
            if str(id) == str(idx.guestID):
                return idx
                found = 1
        if not found:
            return f'Guest {id} not found'

            
    def createGuest(self, list): #Assigns guest their information from the form
        try:
            newGuest = Guest(list[0],list[1],list[2],list[3])
            newGuest.assignGuestID(Guest.totalGuests[-2].guestID) #sends previous guests ID as parameter, new guest's ID increments by one (while ensuring not a repeat)
##            with open('data/guest_data.csv', 'a',newline='') as stream:
            with open(GUEST_FILE_PATH, 'a',newline='') as stream:

                writer = csv.writer(stream)
                writer.writerow(newGuest)
        except Exception as e:
            print(e)
            newGuest = None
        return newGuest

    
    def setGuestStatus(self,guestStatus):
        if int(guestStatus) == 0 or int(guestStatus) == 1:
            self.guestStatus = guestStatus
##            df = pd.read_csv('data/guest_data.csv')
            df = pd.read_csv(GUEST_FILE_PATH)
            filt = (df['guestID'] == int(self.guestID))
            df.loc[filt,'guestStatus'] = guestStatus
##            df.to_csv('data/guest_data.csv',index = False)
            df.to_csv(GUEST_FILE_PATH,index = False)

        else:
            print("\nERROR: Attempt to set Guest Status with invalid parameter.\n")
    



        


    

    
    

