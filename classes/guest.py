import pandas as pd
import csv

'''
Date of Code: 10/10/2022
Authors: Brian Kelly, Jesse Carrillo
Description: A class used to represent a guest.

Class Variable: 
    totalGuests : list (contains list of all guests)

Attributes:
    fName : str  (first name of guest)
    lName : str (last name of guest)
    phone : str (phone number of guest)
    email : str (email of guest)
    guestID : int (guest’s ID number) 

Methods:
    assignGuestID(id : int) 
        Assigns new Guest with an ID number. Function called during creation of new guest in createGuest method. 
        Parameter is previous guests ID. Ensures no repeat ID is assigned by checking guest list and incrementing ID until valid. 
        No return value

    getGuestByID(id : int ) 
        Searches totalGuests list and returns a Guest object if found or a string notifying user that the Guest was not found

    createGuest(guestInfo : list) 
        Creates a new Guest object from the guestInfo list parameter. 
        assignGuestID is called to assign the new Guest an ID number. 
        Appends guest_data.csv with new guest information.
        Returns newGuest object or an error message if unsuccessful.

'''
class Guest:
    
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
        return f"Name: {self.fName} {self.lName} // guestID: {self.guestID} // Phone: {self.phone} // Email: {self.email}"

    def __iter__(self):
        return iter([self.fName,self.lName,self.phone,self.email,self.guestID,])

    #Assigns new guest with guest ID.
    def assignGuestID(self,id): 
        isValidID = True
        for idx in Guest.totalGuests:
            if id == idx.guestID:
                isValidID = False
                self.assignGuestID(int(id)+1) #increment number until valid
 
        if isValidID:
            self.guestID = id
 
            

    #Return guest by Guest ID
    def getGuestByID(self,id):
        for idx in Guest.totalGuests:
            if id == idx.guestID:
                return idx

        return f'Guest {id} not found'

   #Assigns guest their information from the form          
    def createGuest(self, guestInfo):
        try:
            newGuest = Guest(guestInfo[0],guestInfo[1],guestInfo[2],guestInfo[3])
            
            #sends previous guests ID as parameter, new guest's ID increments by one (while ensuring not a repeat)
            newGuest.assignGuestID(Guest.totalGuests[-2].guestID)
            with open('data/guest_data.csv', 'a',newline='') as stream:
                writer = csv.writer(stream)
                writer.writerow(newGuest)
        except Exception as e:
            print(e)
            newGuest = None
        return newGuest


    



        


    

    
    

