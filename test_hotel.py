from classes.hotel import *

hotel = Hotel()

#Testing three methods from Reservation class
def test_createReservation():
    '''
    Parameters: Guest ID, Start date, End date, Room Number
    Returns Reservation object if valid. or None type if invalid parameters
    '''
    assert type(hotel.createReservation(12,'2022-09-13','2022-09-16',4)) == Reservation
    assert hotel.createReservation('invalid','guest',3,'here') == None

    


def test_getReservationByResNum():
    '''
    Parameter: reservation number 
    Returns a reservation object if valid. Or None if invalid reservation number
    Testing the reservation object returned has correct guest ID
    '''
    validResNum = 'C6653'
    correctGuestID = 34
    invalidResNum = '2235235235'

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
    Returns the new guest object if valid, or None if invalid (invalid if strings are not used or string length not at least 1 character)
    '''
    validGuestInformation = ['Jimmy','Bob','555-5094','jimmyBob@yahoo.com','71bd19d37f19be2c394c2292e32268636e3db282c5c5ad7d4bb14bd09a7e1966']
    correctFirstName = validGuestInformation[0]
    invalidGuestInformation = ['No data',3,'']

    assert type(hotel.createGuest(validGuestInformation)) == Guest
    assert hotel.createGuest(validGuestInformation).fName == correctFirstName

    # Field is left blank
    assert hotel.createGuest(invalidGuestInformation) == None
    
    # Field is not a string
    assert hotel.createGuest([invalidGuestInformation[1],validGuestInformation[1],validGuestInformation[2],validGuestInformation[3],validGuestInformation[4]]) == None
    assert hotel.createGuest([validGuestInformation[0],validGuestInformation[1],invalidGuestInformation[1],validGuestInformation[3],validGuestInformation[4]]) == None

    # Field is not a valid length
    assert hotel.createGuest([validGuestInformation[0],invalidGuestInformation[2],validGuestInformation[2],validGuestInformation[3],validGuestInformation[4]]) == None
    assert hotel.createGuest([validGuestInformation[0],validGuestInformation[1],validGuestInformation[2],invalidGuestInformation[2],validGuestInformation[4]]) == None


#Testing two methods from Room class
def test_searchRooms():
    '''
    Parameters: room type, start date, end date
    Returns a list of room numbers.
    List with all available 'Basic' rooms will be length of 8
    '''

    '''Testing to ensure list of 'Basic' rooms is will be length of 7 when 1 registration during date range. 8 if 0 registrations'''
    assert len(hotel.searchRooms('Basic','2022-10-13','2022-10-16')) == 7
    assert len(hotel.searchRooms('Basic','2022-10-13','2022-10-15')) == 8

def test_isAvailableRoom():

    '''Date Range: Testing to ensure a room that has registration during date range returns False'''
    assert hotel.isAvailableRoom(3,'2022-10-13','2022-10-16') == False
    assert hotel.isAvailableRoom(4,'2022-10-13','2022-10-16') == True

    '''Single Date: Returns false if room is not available on selected date'''
    assert hotel.isAvailableRoom(3,'2022-10-16') == False
    assert hotel.isAvailableRoom(3,'2022-10-19') == True












