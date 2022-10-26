import pandas as pd
from datetime import datetime

class Room:
    
    #Class variables
    totalRooms = []
    roomChoices = ['Basic','Deluxe','Suite']

    def __init__(self,roomType="",roomNumber=0, roomStatus=0,roomPrice = 0):
        self.roomType = roomType
        self.roomNumber = roomNumber
        self.roomStatus = roomStatus
        self.roomPrice = roomPrice

        Room.totalRooms.append(self)

    def __str__(self):
        return f"Room #: {self.roomNumber} // Room Type: {self.roomType} // Room Status: {self.roomStatus} // Room Price: {self.roomPrice}"
    
    def setRoomStatus(self, roomStatus):
        if int(roomStatus) == 0 or int(roomStatus) == 1:
            self.roomStatus = roomStatus

            df = pd.read_csv('data/room_data.csv')
            filt = (df['roomNumber'] == int(self.roomNumber))
            df.loc[filt,'roomStatus'] = roomStatus
            df.to_csv('data/room_data.csv',index = False)
        else:
            print("ERROR: Attempt to set Room Status with invalid parameter.\n")
    


    def searchRooms(self, roomType,startDate,endDate):
        roomList = []
        startDate = datetime.strptime(startDate, '%m/%d/%Y')
        endDate = datetime.strptime(endDate, '%m/%d/%Y')
        if roomType in self.roomChoices:
            
            #Gathers all rooms of room type
            for idx in Room.totalRooms:
                if idx.roomType == roomType and idx.roomStatus == 0:
                    roomList.append(idx.roomNumber)

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
            
            return roomList

    def returnRoomByNumber(self,roomNumber):
        found = 0
        for idx in Room.totalRooms:
            if str(roomNumber) == str(idx.roomNumber):
                return idx
                found = 1
        if not found:
            return f'Room {roomNumber} not found'





    
    

