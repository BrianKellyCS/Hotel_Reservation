import pandas as pd
import csv

'''
Date of Code: 10/10/2022
Authors: Brian Kelly, Jesse Carrillo
Description: A class used to represent a guest.
'''
class Guest:

    totalGuests = []

    def __init__(self, fName="No First Name", lName ="No Last Name", phone="No Phone", email="No Email", guestPWD = None,guestID = 0):
        self.fName = fName
        self.lName = lName
        self.phone = phone
        self.email = email
        self.guestPWD = guestPWD
        self.guestID = guestID
        

        Guest.totalGuests.append(self)

    
    def __str__(self):
        return f"Name: {self.fName} {self.lName} // guestID: {self.guestID} // Phone: {self.phone} // Email: {self.email}"

    def __iter__(self):
        return iter([self.fName,self.lName,self.phone,self.email,self.guestPWD,self.guestID,])


    def assignGuestID(self,id):
        '''
        Assigns new Guest with an ID number. Function called during creation of new guest in createGuest method. 
        Parameter is previous guests ID. Ensures no repeat ID is assigned by checking guest list and incrementing ID until valid. 
        No return value
        '''
        isValidID = True
        for idx in Guest.totalGuests:
            if id == idx.guestID:
                isValidID = False
                self.assignGuestID(int(id)+1)
 
        if isValidID:
            self.guestID = id
 
            
    def getGuestByID(self,id):
        '''Returns Guest by ID. Searches totalGuests list and returns a Guest object if found or a string notifying user that the Guest was not found'''
        for idx in Guest.totalGuests:
            if id == idx.guestID:
                return idx

        return f'Guest {id} not found'


    def validateGuestInfo(self,guestInfo):
        if not type(guestInfo[0]) is str:
            raise Exception("First Name must be a valid string.")

        if len(guestInfo[0]) < 1:
                raise Exception("First Name must have at least one character.")
        
        if not type(guestInfo[1]) is str:
            raise Exception("Last Name must be a valid string.")
            
        if len(guestInfo[1]) < 1:
                raise Exception("Last Name must have at least one character.")

        if not type(guestInfo[2]) is str:
            raise Exception("Phone number must be a valid string.")
            
        if len(guestInfo[2]) < 1:
            raise Exception("Phone Number must have at least one character.")

        if not type(guestInfo[3]) is str:
            raise Exception("Email must be a valid string.")
            
        if len(guestInfo[3]) < 1:
            raise Exception("Email must have at least one character.")

    def createGuest(self, guestInfo):
        '''
        Creates a new Guest object from the guestInfo list parameter. 
        assignGuestID is called to assign the new Guest an ID number. 
        Appends guest_data.csv with new guest information.
        Returns newGuest object or an error message if unsuccessful.
        '''
        try:
            self.validateGuestInfo(guestInfo)
            
            newGuest = Guest(guestInfo[0],guestInfo[1],guestInfo[2],guestInfo[3],guestInfo[4])
            newGuest.assignGuestID(Guest.totalGuests[-2].guestID)
            with open('data/guest_data.csv', 'a',newline='') as stream:
                writer = csv.writer(stream)
                writer.writerow(newGuest)
        except Exception as e:
            print(e)
            newGuest = None
        return newGuest


    



        


    

    
    

