import pandas as pd

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
    


    def searchRooms(self, roomType):
        roomList = []

        if roomType in self.roomChoices:
            for idx in Room.totalRooms:
                if idx.roomType == roomType and idx.roomStatus == 0:
                    print(idx)
                    roomList.append(idx.roomNumber) #Returns a list of room numbers available
            
            return roomList
                
        else:
            print("Must enter a valid room type\n")

    def returnRoomByNumber(self,roomNumber):
        found = 0
        for idx in Room.totalRooms:
            if str(roomNumber) == str(idx.roomNumber):
                return idx
                found = 1
        if not found:
            return f'Room {roomNumber} not found'





    
    

