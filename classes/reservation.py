import random


class Reservation():
    
    #Class variables
    totalReservations = []

    def __init__(self,guestObj = None, startDate=None,endDate=None, roomObj = None):
        
        self.guestObj = guestObj
        self.reservationNumber = random.randint(1,500) if startDate != None else None #TO DO : method to assign better reservation number. ensure no repeat
        self.startDate = startDate
        self.endDate = endDate
        self.roomObj = roomObj

        Reservation.totalReservations.append(self)
        
    def __str__(self):
        return f"*Customer Reservation*\n{self.guestObj}\nReservation #: {self.reservationNumber}, // Start Date: {self.startDate}, // End Date: {self.endDate}\n{self.roomObj}"



    def createReservation(self,guestObj,startDate,endDate,roomObj):
        try:
            if int(guestObj.guestStatus) == 1:
                print("\nGuest already has reservation.\n")
            else:
                guestObj.reservation = Reservation(guestObj,startDate,endDate,roomObj)
                guestObj.setGuestStatus(1)
                roomObj.setRoomStatus(1)
                print(f"Reservation successfully created for {guestObj.fName} {guestObj.lName}\n")
                print(guestObj.reservation)
        except Exception as e:
            print(e)
        

    def editReservation(self,guestObj,startDate,endDate,roomObj):
        pass


    def cancelReservation(self,reservationNumber):
        pass


    def emailReservation(self,reservationNumber):
        pass


    

    
    



    

    
    

