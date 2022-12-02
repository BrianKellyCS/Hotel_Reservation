from classes.hotel import *

hotel = Hotel()
hotel.initializeHotelData()

#Testing two methods from Reservation class
def test_getReservationByResNum():
    '''
    Parameter: reservation number 
    Returns a reservation object
    Testing the reservation object returned has correct guest ID
    '''
    assert hotel.getReservationByResNum(144).guestID == 18


def test_getReservationByGuestID():
    '''
    Parameter: Guest ID number 
    Returns a list of reservation objects
    Testing to ensure the list for Guest with ID: 18 returns proper number of reservations
    '''
    assert len(hotel.getReservationByGuestID(18)) == 1


#Testing two methods from Guest class
def test_getGuestByID():
    '''
    Parameter: guest ID 
    Returns Guest object
    Test ensures that returned guest Object has correct first name
    '''
    assert hotel.getGuestByID(18).fName == 'Bob'

def test_createGuest():
    '''
    Parameter: list of guest information.
    Returns the new guest object
    Test to ensure that the new guest has the correct first name
    '''
    guestInformation = ['Jimmy','Bob','555-5094','jimmyBob@yahoo.com']
    assert hotel.createGuest(guestInformation).fName == 'Jimmy'


#Testing two methods from Room class
def test_searchRooms():
    '''
    Parameters: room type, start date, end date
    Returns a list of room numbers.
    Testing to ensure that the number of 'Basic' rooms for this date range is 7. 
    (If all basic rooms available, length is 8. One reservation for this date range, so length = 7)
    '''
    assert len(hotel.searchRooms('Basic','10/13/2022','10/16/2022')) == 7

def test_isAvailableRoom():
    '''
    Parameters: room number, startdate, enddate
    Testing to ensure a room that has registration during date range returns False
    '''
    assert hotel.isAvailableRoom(3,'10/13/2022','10/16/2022') == False












