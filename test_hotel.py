from classes.hotel import *

hotel = Hotel()
hotel.initializeHotelData()

#Testing two methods from Reservation class
def test_getReservationByResNum():
    '''
    Parameter: reservation number 
    Returns a reservation object if valid. Or None if invalid reservation number
    Testing the reservation object returned has correct guest ID
    '''
    validResNum = 144
    correctGuestID = 18
    invalidResNum = 2235235235

    assert hotel.getReservationByResNum(validResNum).guestID == correctGuestID
    assert hotel.getReservationByResNum(invalidResNum) == None


def test_getReservationByGuestID():
    '''
    Parameter: Guest ID number 
    Returns a list of reservation objects. returns None type if invalid guest ID
    Testing to ensure the list for Guest with ID: 18 returns proper number of reservations
    '''
    validGuestID = 18
    correctLength = 1
    invalidGuestID = 323235

    assert len(hotel.getReservationByGuestID(validGuestID)) == correctLength
    assert hotel.getReservationByGuestID(invalidGuestID) == None


#Testing two methods from Guest class
def test_getGuestByID():
    '''
    Parameter: guest ID 
    Returns Guest object if found. A string to display in GUI if not found
    Test ensures that returned guest Object has correct first name
    '''
    validGuestID = 18
    correctGuestName = 'Bob'
    invalidGuestID = 90294

    assert hotel.getGuestByID(validGuestID).fName == correctGuestName
    assert hotel.getGuestByID(invalidGuestID) == f'Guest {invalidGuestID} not found'

def test_createGuest():
    '''
    Parameter: list of guest information.
    Returns the new guest object if valid, or None if invalid
    '''
    validGuestInformation = ['Jimmy','Bob','555-5094','jimmyBob@yahoo.com']
    correctFirstName = validGuestInformation[0]
    invalidGuestInformation = ['No data',3]

    assert type(hotel.createGuest(validGuestInformation)) == Guest
    assert hotel.createGuest(validGuestInformation).fName == correctFirstName
    assert hotel.createGuest(invalidGuestInformation) == None


#Testing two methods from Room class
def test_searchRooms():
    '''
    Parameters: room type, start date, end date
    Returns a list of room numbers.
    List with all available 'Basic' rooms will be length of 8
    '''

    '''Testing to ensure list of 'Basic' rooms is will be length of 7 when 1 registration during date range. 8 if 0 registrations'''
    assert len(hotel.searchRooms('Basic','10/13/2022','10/16/2022')) == 7
    assert len(hotel.searchRooms('Basic','10/13/2022','10/15/2022')) == 8

def test_isAvailableRoom():

    '''Date Range: Testing to ensure a room that has registration during date range returns False'''
    assert hotel.isAvailableRoom(3,'10/13/2022','10/16/2022') == False
    assert hotel.isAvailableRoom(4,'10/13/2022','10/16/2022') == True

    '''Single Date: Returns false if room is not available on selected date'''
    assert hotel.isAvailableRoom(3,'10/16/2022') == False
    assert hotel.isAvailableRoom(3,'10/19/2022') == True












