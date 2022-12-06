
#################################################################################################################################
# Hotel Reservation Project
#  Project by:
#  Jesse Carrillo
#  Brian Kelly
#  Anthony Rosas
#  Started 10.1.2022
#
# This is the main menu and GUI for the Hotel Project. From here we will be able to manage the Guests and Reservations visually
#################################################################################################################################
import PySimpleGUI as sg
from Images64 import * # A Seperate python file filled with Base64 strings of our images to make it easier to manage
from classes.hotel import Hotel
from datetime import date, datetime
import pydoc
import hashlib

DISPLAY_W, DISPLAY_H = 600,450
BG_COLOR = "#1E90FF"

print("Starting Menu...")
sg.theme('DarkTeal3')

infoText = "Welcome to JAB Hotel!"
hotel = Hotel()
rooms = hotel.rooms
currentDate = date.today().strftime("%Y-%m-%d")

def Login():
    '''Login as guest with valid username (email) and password. or as an employee. If new guest, fill out information form to enter main menu'''
    admin_hash = '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918'
    layout = [[sg.Text("Log In", size =(15, 1), font=40)],
            [sg.Text("Email", size =(15, 1), font=16),sg.InputText(key='-usrnm-', font=16)],
            [sg.Text("Password", size =(15, 1), font=16),sg.InputText(key='-pwd-', password_char='*', font=16)],
            [sg.Checkbox('Show Password',key='CHECK',default=False, enable_events=True)],
            [sg.Button('Ok'),sg.Button('Cancel'),sg.Button('Sign up')]]

    window = sg.Window("Log In", layout)

    while True:
        validCredentials = False
        event,values = window.read()

        if event == "Cancel" or event == sg.WIN_CLOSED:
            break

        if event == "Sign up":
            currentGuest = hotel.createGuest(InformationForm())
            if currentGuest != None:
                userType = 'Guest'
                userMessage = f"Welcome VALUED GUEST # {currentGuest.guestID}!"
                window.close()
                Main(userType,currentGuest,userMessage)
            else:
                userMessage = "Did not fill out form."

        if values['CHECK'] == True:
            try:
                window['-pwd-'].update(password_char='')
            except Exception as e:
                print(e)

        if values['CHECK'] == False:
            try:
                window['-pwd-'].update(password_char='*')
            except Exception as e:
                print(e) 

        if event == "Ok":
            try:
                auth = values['-pwd-'].encode()
                auth_hash = hashlib.sha256(auth).hexdigest()
                print(auth_hash)
            except Exception as e:
                print(e)

            #Check guests
            for guest in hotel.guests:
                if values['-usrnm-'].upper() == guest.email.upper() and auth_hash == guest.guestPWD:
                    validCredentials = True
                    currentGuest = guest
                    userType = 'Guest'
                    userMessage = f"Welcome VALUED GUEST # {currentGuest.guestID}!"
                    window.close()
                    break

            #Check if employee login
            if values['-usrnm-'] == 'admin' and auth_hash == admin_hash:
                validCredentials = True
                currentGuest = None
                userType = 'Employee'
                userMessage = 'This is an employee'
                window.close()
            elif not validCredentials:
                userMessage = "Invalid Username or Password.\nPlease try again."


            if not validCredentials:
                sg.popup(userMessage)
            else:
                Main(userType,currentGuest,userMessage)


    window.close()


def InformationForm(): 
    '''A form that lets the user input their information. If submit is pressed it will return four strings: First name, Last name, Phone Number and Email as typed in the form. If the form is not filled out or closed it will return None'''
    FormLayout = [
        [sg.Text('Please enter reservation information: ')],
        [sg.Text('First Name', size =(15, 1)), sg.InputText()], 
        [sg.Text('Last Name', size =(15, 1)), sg.InputText()],
        [sg.Text('Phone', size =(15, 1)), sg.InputText()], 
        [sg.Text('Email', size =(15, 1)), sg.InputText()],
        [sg.Text('Password', size =(15, 1)), sg.InputText()],
        [sg.Submit(), sg.Cancel()]
    ]
  
    FormWindow = sg.Window('Guest Information Entry', FormLayout)
    event, values = FormWindow.read()

    FormWindow.close()   
    if (event == "Submit"):
        if values[0] == '' or values [1] == '' or values [2] == '' or values [3] == '' or values[4] == '':
            print('Information not saved. Must fill out form completely')
        else:
            values[4] = values[4].encode()
            values[4] = hashlib.sha256(values[4]).hexdigest()
            return values[0], values[1], values[2], values[3], values[4]

    if (event == "Cancel" or event == "Exit" or event == sg.WIN_CLOSED):
        return None

def validCardNumber(cardNumber):
    '''Uses Luhn Algorithm to validate card number'''
    #Strip spaces or dashes from card number
    cardNumber = cardNumber.replace(' ','').replace('-','')

    #Check if card number is correct length and only has digits
    if len(cardNumber) not in [13,14,15,16] or not cardNumber.isdigit():
        return False

    # Reverse the card number
    cardNumber = cardNumber[::-1]
    
    # Convert the card number to a list of integers and double every second digit
    cardNumber = [int(x) * (i % 2 + 1) for i, x in enumerate(cardNumber)]
    
    # Subtract 9 from any doubled digits that are greater than 9
    cardNumber = [x - 9 if x > 9 else x for x in cardNumber]
    
    # Calculate the sum of all the digits
    sumOfDigits = sum(cardNumber)
    
    # Check if the sum is divisible by 10
    divisibleByTen = sumOfDigits % 10 == 0

    #Check if pass luhn algorithm
    if not divisibleByTen:
        return False
    
    #If al checks pass, card is valid
    return True

def HandleReservationsWindow(userType,currentGuest,createOrEdit):
    '''Opens a new window where the user can select a reservation start date, an end date and a room type and recieve a list of available rooms to reserve. Returns an int for the chosen room number, a string for the reservation start date ("MM/DD/YYYY") and a string for the reservation end date ("MM/DD"YYYY") when submit is pressed and the reservation is valid.'''
    SEARCH_CANVAS_W, SEARCH_CANVAS_H = 300,350
    SEARCH_IMAGE_W, SEARCH_IMAGE_H = 100,100

    RoomDisplayOne = sg.Graph(
        canvas_size=(SEARCH_IMAGE_W, SEARCH_IMAGE_H),
        graph_bottom_left=(0, 0),
        graph_top_right=(SEARCH_IMAGE_W, SEARCH_IMAGE_H),
        key="-ROOMBASICDISPLAY-",
        background_color='#61CCF6',
        enable_events=True,
        drag_submits=True)

    RoomDisplayTwo = sg.Graph(
        canvas_size=(SEARCH_IMAGE_W, SEARCH_IMAGE_H),
        graph_bottom_left=(0, 0),
        graph_top_right=(SEARCH_IMAGE_W, SEARCH_IMAGE_H),
        key="-ROOMMEDDISPLAY-",
        background_color='#61CCF6',
        enable_events=True,
        drag_submits=True)

    RoomDisplayThree = sg.Graph(
        canvas_size=(SEARCH_IMAGE_W, SEARCH_IMAGE_H),
        graph_bottom_left=(0, 0),
        graph_top_right=(SEARCH_IMAGE_W, SEARCH_IMAGE_H),
        key="-ROOMLARGEDISPLAY-",
        background_color='#61CCF6',
        enable_events=True,
        drag_submits=True)

    RoomTypeList = ["Basic", "Deluxe", "Suite"]
    SearchList = ["None"]
    roomChosen,roomSelected,roomDateStart,roomDateEnd = 0,0,"No Date","No Date"

    SearchLayoutL = [
        [sg.Text("Select Reservation Information: ", key='-RESERVETEXT-', font='Default 12', size = (30,1))],
        [sg.CalendarButton('Select Date',  target='-DATE-', format='%Y-%m-%d'), sg.Input(key='-DATE-', size=(20,1)), sg.CalendarButton('Select End Date',  target='-ENDDATE-', format='%Y-%m-%d'), sg.Input(key='-ENDDATE-', size=(20,1)) ],
        [sg.Text("Room Type ", key='-ROOMTYPETEXT-', size = (12,1)), sg.Combo(RoomTypeList, s=(15,22), enable_events=True, readonly=True, k='-ROOMTYPE-'), sg.Text("Room Number ", key='-ROOMCHOSENTEXT-', size = (12,1), justification="right"), sg.Combo(SearchList,default_value="None", s=(10,22), enable_events=True, readonly=True, k='-SEARCH-'), ],  
        [sg.Text('Reservation Cost: ', key='-INFO-')],
        [sg.Text(' ')],
        [sg.HSep()],
        [sg.Text("Payment Information: ", font='Default 12', size = (30,1))],
        [sg.Text('Card Number', size =(15, 1)), sg.InputText(key='-CARD-')],
        [sg.CalendarButton('Expiration Date:',  target='-EXP_DATE-', format='%Y-%m-%d'), sg.Input(key='-EXP_DATE-', size=(20,1))],
        [sg.Text(' ')],
        [sg.Text('Card CVV', size =(15, 1)), sg.InputText(key='-CVV-')],
        [sg.Submit(key='-SUBMIT-'), sg.Cancel()]
    ]

    small_desc = "Basic Room\nCost: $50 per night\nThis room is perfect for the single traveler or a couple.\nOne bed and a pullout couch available. \nIncludes complimentary breakfast."
    med_desc = "Deluxe Room\nCost: $75 per night\nThis room is large enough for the whole family to relax.\nTwo beds and a pullout couch available. \nIncludes complimentary breakfast."
    large_desc = "Presidential Suite\nCost: $125 per night\nOur largest room, this room is great for meetings or relaxing in luxury. \nTwo beds, living room area and kitchenette, this space easily houses a large group. \nIncludes complimentary breakfast and spa access."

    SearchLayoutR = [[RoomDisplayOne, sg.Multiline(default_text=small_desc,size=(30,5), key="-SMALLROOMDESC-", write_only=True)],
    [RoomDisplayTwo, sg.Multiline(default_text=med_desc,size=(30,5), key="-MEDROOMDESC-", write_only=True)],
    [RoomDisplayThree, sg.Multiline(default_text=large_desc,size=(30,5), key="-LARGEROOMDESC-", write_only=True)]
    ]

    SearchLayout = [[sg.Col(SearchLayoutL, p=0,vertical_alignment="t"),sg.Col(SearchLayoutR, p=0,vertical_alignment="t")]]

    SearchWindow = sg.Window('Search Rooms', SearchLayout)#, finalize = True)

    SmallRoomPicture = SearchWindow["-ROOMBASICDISPLAY-"]
    MedRoomPicture = SearchWindow["-ROOMMEDDISPLAY-"]
    LargeRoomPicture = SearchWindow["-ROOMLARGEDISPLAY-"]

    if userType == 'Employee':
        if createOrEdit == 'Create':
            justDisplayGuests = False
            currentGuest = DisplayGuests(userType,justDisplayGuests)
        print(currentGuest)

    if currentGuest == "No Guest Selected":
        roomSelected = 0
        roomDateStart = "No Date"
        roomDateEnd = "No Date"
        return roomSelected, roomDateStart, roomDateEnd, currentGuest
    else:
        while True:
            event, values = SearchWindow.read(timeout=1)

            SmallRoomPicture.draw_image(data=SmallRoomImage, location=(0,100))
            MedRoomPicture.draw_image(data=MedRoomImage,location=(0,100))
            LargeRoomPicture.draw_image(data=LargeRoomImage,location=(0,100))

            if event in (sg.WIN_CLOSED, 'Exit', 'Cancel', None):
                roomSelected = 0
                roomDateStart = "No Date"
                roomDateEnd = "No Date"
                break
            
            if (event == "-ROOMTYPE-"):
                typeChosen = values[event]
                SearchList = []
                if values['-DATE-'] != '' and values['-ENDDATE-'] != '':
                    SearchList = hotel.searchRooms(typeChosen,values['-DATE-'],values['-ENDDATE-'])
                SearchWindow['-SEARCH-'].update(value="None", values=SearchList)
                roomChosen = 0


            if (event == "-SEARCH-"):
                roomChosen = values[event]
                if createOrEdit == 'Edit':
                    userMessage = 'Updating Reservation'
                elif createOrEdit == 'Create':
                    delta = datetime.strptime(values['-ENDDATE-'], '%Y-%m-%d').date()  - datetime.strptime(values['-DATE-'], '%Y-%m-%d').date()
                    resCost = hotel.getRoom(roomChosen).roomPrice * delta.days
                    userMessage = f'Cost of Reservation: ${resCost}'
                SearchWindow['-INFO-'].update(userMessage)
                if roomChosen == "None" or roomChosen == None:
                    roomSelected = 0
                    roomDateStart = "No Date"
                    roomDateEnd = "No Date"

            if (event == "-SUBMIT-"):
                roomSelected = roomChosen
                roomDateStart = values['-DATE-']
                roomDateEnd = values['-ENDDATE-']
                
 
                #invalid dates
                if roomDateEnd <= roomDateStart:
                    sg.popup('Start Date must be before End Date')
                    roomSelected = 0
                    roomDateStart = "No Date"
                    roomDateEnd = "No Date"
                
                #invalid card number
                if not validCardNumber(values['-CARD-']):
                    sg.popup("Invalid Card number.\nPlease Re-enter.")
                #invalid cvv number length
                elif values['-CVV-'] == '' or len(values['-CVV-']) > 4:
                    sg.popup("Invalid CVV Number.\nPlease Re-enter.") 
                #expired card date
                elif datetime.strptime(values['-EXP_DATE-'], '%Y-%m-%d').date() <= datetime.strptime(currentDate, '%Y-%m-%d').date():
                    sg.popup("Card Date is Expired.\nPlease verify that the correct date was entered")
                else:
                    break

        SearchWindow.close()
        print(f"Sending back: {roomChosen}")
        return roomSelected, roomDateStart, roomDateEnd, currentGuest

   
def DisplayRoomsWindow(currentDate):
    '''Opens a new window that visually shows a floor by floor layout of the hotel and which rooms are available to reserve on a chosen date. After selecting a date and pressing submit the display will update and display the available rooms in green and the taken rooms in red. currentDate is used to start the calendar element on the correct day.'''
    dateToDisplay = currentDate
    print("Displaying Room List")
    # Size of room display and the floors of the hotel display
    ROOMS_DISPLAY_W, ROOMS_DISPLAY_H = 400, 400

    GROUND_FLOOR = 1
    MAX_FLOORS = 4
    message = ''

    currentFloor = 1
    currentFloorText = "Floor: " + str(currentFloor)+ ""
    floorChanged = True

    # For mouse click
    fig = None
    last_clicked = 0

    RoomsDisplay = sg.Graph(
        canvas_size=(ROOMS_DISPLAY_W, ROOMS_DISPLAY_H),
        graph_bottom_left=(0, 0),
        graph_top_right=(ROOMS_DISPLAY_W, ROOMS_DISPLAY_H),
        key="-DISPLAY-",
        background_color='#61CCF6',
        enable_events=True,
        drag_submits=True)

    RoomsLayoutR =    [[RoomsDisplay]]
    RoomsLayoutL = [
        [sg.CalendarButton('Select Date',  target='-DATE-', format='%Y-%m-%d'), sg.Input(key='-DATE-', size=(10,1)) ],
        [sg.Button(button_text='Submit', key = '-SUBMIT-', size = (5,1))],
        [sg.Text("Floor: 1", key='-FLOOR-', font='Default 12', size = (25,1), text_color="White")],
        [sg.Button(button_text='^', key = '-UP-', size = (25,5))],
        [sg.Button(button_text='v', key = '-DOWN-', size = (25,5))],
        [sg.Text(message, key='-MESSAGE-')]
    ]

    RoomsLayout = [[sg.Col(RoomsLayoutL, p=0), sg.Col(RoomsLayoutR, p=0)]]

    RoomsDisplayWindow = sg.Window("Room Display", RoomsLayout, finalize = True)
    RoomsGraph = RoomsDisplayWindow["-DISPLAY-"]

    # Draw floorplan for floor and room availability (From left to right 1-4)
    # Each room has two images, Full (Red) and Empty (Green)
    floorplans = [    RoomsGraph.draw_image(data=Floorplan, location=(0,ROOMS_DISPLAY_H)),  RoomsGraph.draw_image(data=FloorThree, location=(0,0)),RoomsGraph.draw_image(data=FloorFour, location=(0,0)) ]
    roomCoords = [(0,0),(19,150),(97,309),(224,309),(302,150)]
    roomMedCoords = [(0,0),(19,329),(146,329),(272,329)]
    roomLargeCoords = [(0,0),(90,349)]

    roomSquares = [ RoomsGraph.draw_image(data=RoomFull, location=(0,0)), RoomsGraph.draw_image(data=RoomEmpty, location=(0,0)), 
                    RoomsGraph.draw_image(data=RoomFull, location=(0,0)), RoomsGraph.draw_image(data=RoomEmpty, location=(0,0)),
                    RoomsGraph.draw_image(data=RoomFull, location=(0,0)), RoomsGraph.draw_image(data=RoomEmpty, location=(0,0)), 
                    RoomsGraph.draw_image(data=RoomFull, location=(0,0)), RoomsGraph.draw_image(data=RoomEmpty, location=(0,0)) ]
    
    roomMed = [ RoomsGraph.draw_image(data=RoomMedFull, location=(0,0)), RoomsGraph.draw_image(data=RoomMedEmpty, location=(0,0)), 
                RoomsGraph.draw_image(data=RoomMedFull, location=(0,0)), RoomsGraph.draw_image(data=RoomMedEmpty, location=(0,0)),
                RoomsGraph.draw_image(data=RoomMedFull, location=(0,0)), RoomsGraph.draw_image(data=RoomMedEmpty, location=(0,0)) ]

    roomLarge = [   RoomsGraph.draw_image(data=RoomLargeFull, location=(0,0)), RoomsGraph.draw_image(data=RoomLargeEmpty, location=(0,0)) ]

    RoomsDisplayWindow['-FLOOR-'].update(currentFloorText)

    while True:         # The Event Loop
        event, values = RoomsDisplayWindow.read(timeout=1)
        
        if event == '-SUBMIT-':
            dateToDisplay = values['-DATE-'] if values['-DATE-'] != '' else currentDate
            print(dateToDisplay)
            floorChanged = True
            RoomsDisplayWindow['-FLOOR-'].update(currentFloorText)

        if event in (sg.WIN_CLOSED, 'Exit', None):
            break

        if event == '-UP-':
            if currentFloor < MAX_FLOORS:
                currentFloor += 1
                floorChanged = True
            RoomsDisplayWindow['-FLOOR-'].update("Floor: "+str(currentFloor)+"")

        if event == '-DOWN-':
            if currentFloor > GROUND_FLOOR:
                currentFloor += -1
                floorChanged = True
            RoomsDisplayWindow['-FLOOR-'].update("Floor: "+str(currentFloor)+"")
    
        if floorChanged == True:
            posOffset = (currentFloor - 1)*4
            print(f"currFloor: {currentFloor}")
            if currentFloor < 3:
                RoomsGraph.relocate_figure(floorplans[0],0,ROOMS_DISPLAY_H)
                RoomsGraph.relocate_figure(floorplans[1],0,0)
                RoomsGraph.relocate_figure(floorplans[2],0,0)

                for x in range (0,6): #move medium rooms away
                    RoomsGraph.relocate_figure(roomMed[x],roomCoords[0][0],roomCoords[0][1])
                for x in range (0,2): #move large rooms away
                    RoomsGraph.relocate_figure(roomLarge[x],roomCoords[0][0],roomCoords[0][1])

                for x in range (1,5):
                    currRoom = x + posOffset
                    fullx = 2*x - 2
                    emptyx = 2*x - 1

                    if hotel.isAvailableRoom(currRoom,dateToDisplay): #Empty
                        print(f"Room:{currRoom} // {x} is not taken")
                        RoomsGraph.relocate_figure(roomSquares[emptyx],roomCoords[x][0],roomCoords[x][1])
                        RoomsGraph.relocate_figure(roomSquares[fullx],roomCoords[0][0],roomCoords[0][1])
                    else:
                        print(f"Room{currRoom} // {x} is Taken!")
                        RoomsGraph.relocate_figure(roomSquares[fullx],roomCoords[x][0],roomCoords[x][1])
                        RoomsGraph.relocate_figure(roomSquares[emptyx],roomCoords[0][0],roomCoords[0][1])


            if currentFloor == 3:
                RoomsGraph.relocate_figure(floorplans[1],0,ROOMS_DISPLAY_H)
                RoomsGraph.relocate_figure(floorplans[0],0,0)
                RoomsGraph.relocate_figure(floorplans[2],0,0)
                
                for x in range (0,8): #move all of the squares away
                    RoomsGraph.relocate_figure(roomSquares[x],roomCoords[0][0],roomCoords[0][1])
                for x in range (0,2): #move large rooms away
                    RoomsGraph.relocate_figure(roomLarge[x],roomCoords[0][0],roomCoords[0][1])

                for x in range (1,4):
                    currRoom = x + posOffset
                    fullx = 2*x - 2
                    emptyx = 2*x - 1

                    if hotel.isAvailableRoom(currRoom,dateToDisplay): #Empty
                        print(f"Room:{currRoom} // {x} is not taken")
                        RoomsGraph.relocate_figure(roomMed[emptyx],roomMedCoords[x][0],roomMedCoords[x][1])
                        RoomsGraph.relocate_figure(roomMed[fullx],roomMedCoords[0][0],roomMedCoords[0][1])
                    else:
                        print(f"Room{currRoom} // {x} is Taken!")
                        RoomsGraph.relocate_figure(roomMed[fullx],roomMedCoords[x][0],roomMedCoords[x][1])
                        RoomsGraph.relocate_figure(roomMed[emptyx],roomMedCoords[0][0],roomMedCoords[0][1])
                        
            if currentFloor == 4:
                    currRoom = posOffset
                    fullx = 0
                    emptyx = 1
                    RoomsGraph.relocate_figure(floorplans[2],0,ROOMS_DISPLAY_H)
                    RoomsGraph.relocate_figure(floorplans[0],0,0)
                    RoomsGraph.relocate_figure(floorplans[1],0,0)

                    for x in range (0,8): #move all of the squares away
                        RoomsGraph.relocate_figure(roomSquares[x],0,0)
                    for x in range (0,6): #move medium rooms away
                        RoomsGraph.relocate_figure(roomMed[x],roomCoords[0][0],roomCoords[0][1])

                    if hotel.isAvailableRoom(currRoom,dateToDisplay): #Empty
                        print(f"Room:{currRoom} is not taken")
                        RoomsGraph.relocate_figure(roomLarge[emptyx],roomLargeCoords[1][0],roomLargeCoords[1][1])
                        RoomsGraph.relocate_figure(roomLarge[fullx],roomLargeCoords[0][0],roomLargeCoords[0][1])
                    else:
                        print(f"Room{currRoom} is Taken!")
                        RoomsGraph.relocate_figure(roomLarge[fullx],roomLargeCoords[1][0],roomLargeCoords[1][1])
                        RoomsGraph.relocate_figure(roomLarge[emptyx],roomLargeCoords[0][0],roomLargeCoords[0][1])

            floorChanged = False 
        
        if event == '-DISPLAY-':
            mouse_x, mouse_y = values["-DISPLAY-"]

            clicked_figures = RoomsGraph.get_figures_at_location((mouse_x,mouse_y))
            #print(f"Items at this location: {clicked_figures}")

            fig = clicked_figures[len(clicked_figures)-1]

        elif event.endswith('+UP'): 
            last_clicked = fig
            fig = None
        
        if (last_clicked != 0 and last_clicked != None):
            if (last_clicked == 4 or last_clicked == 5) and currentFloor == 1:
                message = hotel.getReservationByRoom(1,dateToDisplay)
            if (last_clicked == 6 or last_clicked == 7) and currentFloor == 1:
                message = hotel.getReservationByRoom(2,dateToDisplay)
            if (last_clicked == 8 or last_clicked == 9) and currentFloor == 1:
                message = hotel.getReservationByRoom(3,dateToDisplay)
            if (last_clicked == 10 or last_clicked == 11) and currentFloor == 1:
                message = hotel.getReservationByRoom(4,dateToDisplay)
            if (last_clicked == 4 or last_clicked == 5) and currentFloor == 2:
                message = hotel.getReservationByRoom(5,dateToDisplay)
            if (last_clicked == 6 or last_clicked == 7) and currentFloor == 2:
                message = hotel.getReservationByRoom(6,dateToDisplay)
            if (last_clicked == 8 or last_clicked == 9) and currentFloor == 2:
                message = hotel.getReservationByRoom(7,dateToDisplay)
            if (last_clicked == 10 or last_clicked == 11) and currentFloor == 2:
                message = hotel.getReservationByRoom(8,dateToDisplay)
            if last_clicked == 12 or last_clicked == 13:
                message = hotel.getReservationByRoom(9,dateToDisplay)
            if last_clicked == 14 or last_clicked == 15:
                message = hotel.getReservationByRoom(10,dateToDisplay)
            if last_clicked == 16 or last_clicked == 17:
                message = hotel.getReservationByRoom(11,dateToDisplay)
            if last_clicked == 18 or last_clicked == 19:
                message = hotel.getReservationByRoom(12,dateToDisplay)
            last_clicked = None
            RoomsDisplayWindow['-MESSAGE-'].update(message)

    RoomsDisplayWindow.close()

# Modified list sort method, original by GeeksforGeeks: https://www.geeksforgeeks.org/python-sort-list-according-second-element-sublist/
def Sort(sub_li, location):
    # reverse = None (Sorts in Ascending order)
    # key is set to sort using second element of 
    # sublist lambda has been used
    sub_li.sort(key = lambda x: x[location])
    return sub_li

def GenerateManagerReport():
    '''Opens a new window that visually compiles the guest and reservation data into a more human readable format. The data is loaded in from the database and is sorted and displayed based on the chosen date and method by the user.'''
    print("Starting Manager Report")
    REPORT_DISPLAY_W, REPORT_DISPLAY_H = 500, 150
    JAB_MINI_W, JAB_MINI_H = 300, 350

    # Displays for images and graphs
    ReportDisplay = sg.Graph(
        canvas_size=(REPORT_DISPLAY_W, REPORT_DISPLAY_H),
        graph_bottom_left=(0, 0),
        graph_top_right=(REPORT_DISPLAY_W, REPORT_DISPLAY_H),
        key="-REPORTDISPLAY-",
        background_color='#61CCF6',
        pad = (25,10),
        enable_events=True)
    
    JabMiniDisplay = sg.Graph(
        canvas_size=(JAB_MINI_W, JAB_MINI_H),
        graph_bottom_left=(0, 0),
        graph_top_right=(JAB_MINI_W, JAB_MINI_H),
        key="-REPORTDISPLAY-",
        background_color='#61CCF6',
        pad = 25,
        enable_events=True)

    #Get current date and extract the month number from it as default
    dateToDisplay = currentDate
    currentMonth = int(dateToDisplay[0] + dateToDisplay[1])

    MonthsList = ['January', 'February', 'March', 'April', 'May','June','July','August','September','October','November','December']
    YearsList = ['2022']
    TimeList = ['Monthly', 'Yearly']

    TwentyEightDays = [2]
    ThirtyDays = [4,6,9,11]
    ThirtyOneDays = [ 1,3,5,7,8,10,12]

    # Load Guest data as it will display in the report
    guestsList = []
    guestCount = 0

    for guest in hotel.guests:
        if guestCount >= 1:
            tempGuest = []
            tempGuest.append(guest.fName)
            tempGuest.append(guest.lName)
            tempGuest.append(guest.guestID)
            tempGuest.append(guest.phone)
            tempGuest.append(guest.email)
            
            guestsList.append(tempGuest)
        guestCount = guestCount + 1

    # Load Reservation data formatted to read better in report
    reservationList = []
    reservationCount = 0

    for reservation in hotel.reservations:
        try:
            if reservationCount >= 1:
                tempReservation = [] # Formats data to be more readable
                tempReservation.append(guestsList[int(reservation.guestID)-1][1]) #gets guest name from the ID number
                tempReservation.append(reservation.guestID)
                tempReservation.append(reservation.reservationNumber)
                tempReservation.append(reservation.roomNumber)
                # Only the dates, no timestamps
                tempReservation.append(str(reservation.startDate)[0:10])
                tempReservation.append(str(reservation.endDate)[0:10])

                reservationList.append(tempReservation)
            reservationCount = reservationCount + 1
        except Exception as e:
            print(e)
    
    # Empty lists, will hold sorted data
    sortedReservationList = []
    profitList = []

    GuestLayout = [[sg.T("Guest Information (" + str(len(guestsList)) + " Total):", s=(50,1))],
     [sg.Table(guestsList, ['First Name','Last Name','ID','Phone','Email'], justification="left", alternating_row_color="#394a6d", auto_size_columns= False, num_rows=15, col_widths = (12,12,4,10,21))] #True, num_rows=15, max_col_width = 19)] 
    ]

    ReservationLayout = [[sg.T("All Reservations (" + str(len(reservationList)) + " Total):", s=(30,1))],
    [sg.Table(reservationList, ['Surname','Guest ID','Reservation #','Room #','Start','End'], key ='-RESERVATIONTABLE-', justification="center", alternating_row_color="#394a6d", auto_size_columns=False, col_widths = (16,8,8,8,9,10), num_rows=15)]#max_col_width = 25, num_rows=15)]
    ]

    SortedReservationsLayout = [[sg.T("Sorted Results:", s=(30,1))],
    [sg.Table(sortedReservationList, ['Surname','Guest ID','Reservation #','Room #','Start','End'], key ='-SORTEDTABLE-', justification="center", alternating_row_color="#394a6d", auto_size_columns=False, col_widths = (16,8,8,8,9,10), num_rows=15)]#max_col_width = 25, num_rows=15)]
    #[sg.Table(sortedReservationList, ['Name','ID','Start','End','Total'], key ='-SORTEDTABLE-', justification="left", alternating_row_color="#394a6d", auto_size_columns=False, col_widths = (30,4,9,9,7), num_rows=15)]#max_col_width = 25, num_rows=15)]
    ]

    ProfitLayout = [[sg.T("Profit Summary:", s=(30,1))],
    [sg.Table(profitList, ['Name','ID','Start','End','Total'], key ='-PROFITSTABLE-', justification="center", alternating_row_color="#394a6d", auto_size_columns=False, col_widths = (30,4,9,9,7), num_rows=15)]#max_col_width = 25, num_rows=15)]
    ]

    ReportLayoutL = [
        [sg.Text("Manager's Report", font='Default 12', text_color = "white", size = (30,1))],
        [sg.CalendarButton('Select Date',  target='-DATE-', format='%Y-%m-%d',title="Select Date"), sg.Input(key='-DATE-', size=(20,1))],
        [sg.Text("Sort by", size = (6,1)), sg.Combo(TimeList, default_value=TimeList[0], s=(15,22), enable_events=True, readonly=True, k='-TIMESELECT-'), sg.Button(button_text='Submit', key = '-TIMESUBMIT-', size = (6,1))],
        [sg.Button(button_text='Return', key = '-RETURN-', size = (10,1), pad = (125,20))],
        [JabMiniDisplay]
    ]

    ReportLayoutR =    [[ReportDisplay],
    [sg.Text('Information:',s=(15,1))], 
    [sg.TabGroup([[sg.Tab('Guest Information', GuestLayout, key="-GUESTTAB-" ), sg.Tab('All Reservations', ReservationLayout, key = "-RESERVATIONTAB-" ), sg.Tab('Reservations (Sorted)',  SortedReservationsLayout, key = "-SORTEDTAB-" ), sg.Tab('Profits',  ProfitLayout ,visible=True,key='-PROFITSTAB-')]], size = (550,300), enable_events=True )]
    ]

    ReportLayout = [[sg.Col(ReportLayoutL, p=0, vertical_alignment="t"), sg.Col(ReportLayoutR, p=0, vertical_alignment="t")]]

    ReportDisplayWindow = sg.Window("Manager's Report", ReportLayout, finalize = True)
    ReportGraph = ReportDisplayWindow["-REPORTDISPLAY-"]

    JabMiniImage = ReportDisplayWindow["-REPORTDISPLAY-"]
    JabMiniImage.draw_image(data=Logo, location=(0,350))

    while True:         # The Event Loop
        event, values = ReportDisplayWindow.read(timeout=1)
        
        if event in (sg.WIN_CLOSED, 'Exit', '-RETURN-', None):
            break

        if (event == "-TIMESUBMIT-"):
            # If a date is chosen and the submit button is pressed, get sort type
            typeChosen = values["-TIMESELECT-"]

            if values['-DATE-'] != '':
                # Initialize values+tables and get working date information from selected date
                workingDate = values['-DATE-']
                workingDate = datetime.strptime(workingDate, '%Y-%m-%d').date()
                #currentMonth = int(values['-DATE-'][0] + values['-DATE-'][1])
                #currentYear = int(values['-DATE-'][6:10])
                currentMonth = workingDate.month
                currentYear = workingDate.year

                sortedReservationList = []
                profitList = []

                if currentMonth in ThirtyDays: #Set max days for months
                    days = 30
                if currentMonth in ThirtyOneDays:
                    days = 31
                if currentMonth in TwentyEightDays:
                    days = 28

                if typeChosen == "Monthly":
                    sortEnds = []
                    sortStarts = []
                    profitEnds = []
                    profitStarts = []
                    totalProfit = 0

                    # Prep the final sorted lists for data
                    sortedReservationList.append(["Reservations for month of ", ""+ MonthsList[currentMonth-1] ,"" + str(currentYear)])
                    profitList.append(["Profits for month of " + MonthsList[currentMonth-1]+" "+ str(currentYear)])

                    for reservations in reservationList:
                        startYear = int(reservations[4][0:4]) #Set Year
                        endYear = int(reservations[5][0:4])
                        profitWrite = False

                        if (startYear == currentYear or endYear == currentYear):
                            startMonth = int(reservations[4][5:7]) #Set Month
                            endMonth = int(reservations[5][5:7])

                            startDay = int(reservations[4][8:10]) #Set Day
                            endDay = int(reservations[5][8:10])
                            roomNum = reservations[3]

                            if ((endMonth == currentMonth) and (endMonth != startMonth)): # Reservation ends in month
                                # Adds the reservations ending in the month to a list to be sorted
                                sortEnds.append(reservations)
                                
                                # Extracts the room price and nights stayed to get total for room
                                roomProfit = rooms[roomNum].roomPrice * endDay

                                # Formatted list that will show profits for each reservation
                                tempProfitList = []
                                tempProfitList.append(reservations[0])
                                tempProfitList.append(reservations[1])
                                tempProfitList.append(reservations[4])
                                tempProfitList.append(reservations[5])
                                tempProfitList.append(roomProfit)
                                totalProfit = totalProfit + roomProfit

                                profitEnds.append(tempProfitList)
                                
                            if ((startMonth == currentMonth)and (endMonth == currentMonth)): # Reservation is in current month
                                sortStarts.append(reservations)

                                daysStayed = (endDay - startDay + 1)
                                roomProfit = rooms[roomNum].roomPrice * daysStayed

                                profitWrite = True


                            if ((startMonth == currentMonth)and (endMonth != currentMonth)): # Reservation is in current month
                                sortStarts.append(reservations)

                                daysStayed = (days - startDay + 1)
                                roomProfit = rooms[roomNum].roomPrice * daysStayed
                                
                                profitWrite = True

                            if profitWrite == True:
                                # Formatted list that will show profits for each reservation
                                tempProfitList = []
                                tempProfitList.append(reservations[0])
                                tempProfitList.append(reservations[1])
                                tempProfitList.append(reservations[4])
                                tempProfitList.append(reservations[5])
                                tempProfitList.append(roomProfit)

                                profitStarts.append(tempProfitList)
                                totalProfit = totalProfit + roomProfit

                    # Sort the lists depending on what is being used
                    Sort(sortEnds,5)
                    Sort(profitEnds,4)

                    Sort(sortStarts,4)
                    Sort(profitStarts,3)

                    # Append the final sorted lists in order to the displayed list
                    for x in sortEnds:
                        sortedReservationList.append(x)
                    for y in sortStarts:
                        sortedReservationList.append(y)

                    for x in profitEnds:
                        profitList.append(x)
                    for y in profitStarts:
                        profitList.append(y)
                    profitList.append(["Total for Month: $" + str(totalProfit)])

                if typeChosen == "Yearly":
                    sortEnds = []
                    sortStarts = []

                    profitEnds = []
                    profitStarts = []
                    totalProfit = 0

                    # Prep the final sorted lists for data
                    sortedReservationList.append(["Reservations for Year ", str(currentYear)])
                    profitList.append(["Profits for Year " + str(currentYear)])

                    for reservations in reservationList:
                        startYear = int(reservations[4][0:4]) #Set Year
                        endYear = int(reservations[5][0:4])

                        endDay = int(reservations[5][8:10])
                        startDay = int(reservations[4][8:10]) #Set Day
                            
                        roomNum = reservations[3]

                        if ((startYear != currentYear) and (endYear == currentYear)): #Started in a previous year
                            print("This entry started in previous year")
                            sortEnds.append(reservations)
                            roomProfit = rooms[roomNum].roomPrice * endDay # Assumes that they are ending the first month of the year!

                            # Formatted list that will show profits for each reservation
                            tempProfitList = []
                            tempProfitList.append(reservations[0])
                            tempProfitList.append(reservations[1])
                            tempProfitList.append(reservations[4])
                            tempProfitList.append(reservations[5])
                            tempProfitList.append(roomProfit)
                            totalProfit = totalProfit + roomProfit

                            profitEnds.append(tempProfitList)
                            
                        if ((startYear == currentYear)):# and (endYear == currentYear)): # Reservation is all in current year
                            print("This entry is all in the current year")
                            sortStarts.append(reservations)

                            # Checks if the reservation goes into another month
                            if startDay <= endDay:
                                daysStayed = (endDay - startDay + 1)
                            if ((endDay < startDay) and (endYear == currentYear)):
                                daysStayed = (days - startDay + 1) + endDay # days in month + days in other month    
                            if ((endDay < startDay) and (endYear != currentYear)):
                                daysStayed = (days - startDay + 1)
                                if daysStayed <= 0: daysStayed = 1 #Quick bugfix for smaller months
                            roomProfit = rooms[roomNum].roomPrice * daysStayed

                            tempProfitList = []
                            tempProfitList.append(reservations[0])
                            tempProfitList.append(reservations[1])
                            tempProfitList.append(reservations[4])
                            tempProfitList.append(reservations[5])
                            tempProfitList.append(roomProfit)

                            profitStarts.append(tempProfitList)
                            totalProfit = totalProfit + roomProfit

                    # Sort the lists depending on what is being used
                    Sort(sortEnds,5)
                    Sort(profitEnds,4)

                    Sort(sortStarts,4)
                    Sort(profitStarts,3)

                    # Append the final sorted lists in order to the displayed list
                    for x in sortEnds:
                        sortedReservationList.append(x)
                    for y in sortStarts:
                        sortedReservationList.append(y)

                    for x in profitEnds:
                        profitList.append(x)
                    for y in profitStarts:
                        profitList.append(y)
                    profitList.append(["Total for Year: $" + str(totalProfit)])
                
                # Update the table displays to show new sorted data
                ReportDisplayWindow['-SORTEDTABLE-'].update(values=sortedReservationList)
                ReportDisplayWindow['-PROFITSTABLE-'].update(values=profitList)

    ReportDisplayWindow.close()

def DisplayGuests(userType,justDisplayGuests):
    '''
    Formats guests for readability and displays in a table.
    Lists all guests if Employee

    '''
    message = ""
    
    if userType == 'Employee':
        headings = [hotel.guests[0].guestID,hotel.guests[0].lName,hotel.guests[0].fName,hotel.guests[0].email]
        data = []
        #Display reservations for all guests
        for guest in hotel.guests[1:]:
            dataToAdd = [guest.guestID, guest.lName, guest.fName, guest.email]
            data.append(list(dataToAdd))

    layout = [
            [sg.Button(button_text = 'Select Guest', key = '-SELECT-', visible = False if justDisplayGuests else True),sg.Text('Select Guest from Table to create Reservation',key='-INSTRUCTION-',visible = False if justDisplayGuests else True)],
            [sg.Button(button_text = 'Create New Guest', key = '-NEW-')],
            [sg.Table(
                values=data, 
                headings=headings, 
                max_col_width=25,
                auto_size_columns=True,
                justification='right',
                num_rows=20,
                key='-TABLE-',
                expand_x=True,
                expand_y=True,
                enable_click_events=True,
                enable_events = True
            )],
            [sg.Text(message,key='-MESSAGE-')]
    ]

    window = sg.Window('Guest List', layout, resizable=True, finalize=True)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, None):
            window.close()
            selectedGuest = "No Guest Selected"
            return selectedGuest

        if event == '-TABLE-':
            try:
                print(data[values['-TABLE-'][0]])
                message = ''
                window['-MESSAGE-'].update(message)
            except Exception as e:
                print(e)
        
        if event == '-SELECT-':
            if len(values['-TABLE-']) == 0:
                message = 'No Guest Selected'
                window['-MESSAGE-'].update(message)
                
            else:
                print(type(data[values['-TABLE-'][0]][0]))
                selectedGuest = hotel.getGuestByID(int(data[values['-TABLE-'][0]][0]))
                print("IN SELECT",selectedGuest)
                window.close()
                return selectedGuest

        if event == '-NEW-':
            newGuest = hotel.createGuest(InformationForm())
            if newGuest != None:
                dataToAdd = [newGuest.guestID, newGuest.lName, newGuest.fName, newGuest.email]
                data.append(list(dataToAdd))

            #update table
            window['-TABLE-'].update(data)
        

      
    window.close()

def DisplayReservations(userType,currentGuest):
    '''
    Formats reservations for readability and displays in a table.
    Lists all reservations if Employee
    or lists all reservations for Current Guest
    '''
    message = ""

    if userType == 'Guest':
        #if currentGuest == None:
            #message = "Get started by filling out guest form"
            #return message

        #Only display reservations for curent guest
        guestReservations = hotel.getReservationByGuestID(currentGuest.guestID)
        if guestReservations == None:
            message = f'No Reservations for guest {currentGuest.guestID}'
            return message
        print(hotel.getReservationByGuestID(currentGuest.guestID))
        headings = list(hotel.reservations[0])
        data = []
        for res in guestReservations:
            data.append(list(res))

    
    elif userType == 'Employee':
        currentGuest = None
        headings = list(hotel.reservations[0])
        data = []
        #Display reservations for all guests
        for res in hotel.reservations[1:]:
            data.append(list(res))
    
    layout = [
            [sg.Button(button_text = 'Cancel Reservation', key = '-DELETE-'),sg.Button(button_text = 'Edit Reservation', key = '-EDIT-'),sg.Button('Exit')],
            [sg.Table(
                values=data, 
                headings=headings, 
                max_col_width=25,
                auto_size_columns=True,
                justification='right',
                num_rows=20,
                key='-TABLE-',
                expand_x=True,
                expand_y=True,
                enable_click_events=True,
                enable_events = True
            )],
            [sg.Text(message,key='-MESSAGE-')]
    ]

    window = sg.Window('Reservation Data', layout, resizable=True, finalize=True)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit', 'Cancel', None):
            break
        if event == '-TABLE-':
            try:
                print(data[values['-TABLE-'][0]])
                message = ''
                window['-MESSAGE-'].update(message)
            except Exception as e:
                print(e)
        if event == '-DELETE-':
            if len(values['-TABLE-']) == 0:
                message = 'No Reservation Selected'
                window['-MESSAGE-'].update(message)
                
            else:
                response = sg.popup_yes_no('Are you sure you want to\nCancel this Reservation?')
                if response == 'Yes':
                    #index 4 in table is reservation number
                    resToCancel = hotel.getReservationByResNum(data[values['-TABLE-'][0]][5])
                    print(resToCancel)
                    message = hotel.cancelReservation(resToCancel.reservationNumber)
                    window['-MESSAGE-'].update(message)
                    #Remove reservation from table data and hotel reservations array
                    del data[values['-TABLE-'][0]]

                    for i,res in enumerate(hotel.reservations):
                        if resToCancel.reservationNumber == res.reservationNumber:
                            del hotel.reservations[i]
                    

                    #update table
                    window['-TABLE-'].update(data)
        
        if event == '-EDIT-':
            if len(values['-TABLE-']) == 0:
                print('no reservation selected')
            else:
                resToEdit = hotel.getReservationByResNum(data[values['-TABLE-'][0]][5])
                currentGuest = hotel.getGuestByID(resToEdit.guestID)

                #Save original reservation info incase of cancelling the edit window
                originalResCost = resToEdit.reservationCost
                originalStart = resToEdit.startDate
                originalEnd = resToEdit.endDate
                originalRoom = resToEdit.roomNumber

                #Clear values in reservation selected to edit
                resToEdit.startDate = None
                resToEdit.endDate = None
                resToEdit.roomNumber = None
                createOrEdit = 'Edit'

                newRoom, newStartDate, newEndDate,currentGuest = HandleReservationsWindow(userType,currentGuest,createOrEdit)
                if newRoom != 0:
                    #updates database CSV file
                    hotel.editReservation(newStartDate,newEndDate,newRoom,resToEdit.reservationNumber)
                    newResCost = hotel.calculateResCost(newRoom,newStartDate,newEndDate)
                    #update table data
                    data[values['-TABLE-'][0]][1] = newStartDate
                    data[values['-TABLE-'][0]][2] = newEndDate
                    data[values['-TABLE-'][0]][3] = newRoom
                    data[values['-TABLE-'][0]][4] = newResCost

                    #update hotel reservations array
                    for res in hotel.reservations:
                        if resToEdit.reservationNumber == res.reservationNumber:
                            res.startDate = newStartDate
                            res.endDate = newEndDate
                            res.roomNumber = newRoom
                            res.reservationCost = newResCost

                    window['-TABLE-'].update(data)
                    if newResCost > originalResCost:
                        sg.popup(f'${newResCost - originalResCost} will be charged to your card.')
                    if originalResCost > newResCost:
                        sg.popup(f'${originalResCost - newResCost} will be refunded to your card.')
                    
                else:
                    print('no room selected')
                    resToEdit.startDate = originalStart
                    resToEdit.endDate = originalEnd
                    resToEdit.roomNumber = originalRoom

            
    window.close()


def Main(userType, currentGuest,userMessage): #Main Menu, launches all of the options
    '''Main function that drives the GUI and program. On start will prompt the user to login and will adjust the display based on wheter the user is a "Guest" or "Employee." The guest display is simpler, only allowing to login again, input user information and make a reservation. The employee display allows also adds the ability to visually search the rooms, check reservations made and access the manager's report. If this is closed the program will close.'''

    DISPLAY_CANVAS_W, DISPLAY_CANVAS_H = 300,350
    # Display area used for logo image
    Display = sg.Graph(
        canvas_size=(DISPLAY_CANVAS_W, DISPLAY_CANVAS_H),
        graph_bottom_left=(0, 0),
        graph_top_right=(DISPLAY_CANVAS_W, DISPLAY_CANVAS_H),
        key="-DISPLAY-",
        enable_events=True,
        background_color=BG_COLOR,
        drag_submits=True)


    layoutLeft = [
        [sg.Button(button_text='Switch User', key = '-SWITCH-', size = (25,3))],
        [sg.Button(button_text='Display Guests', key = '-DISPLAY_GUESTS-', visible = True if userType == "Employee" else False, size = (25,3))],
        [sg.Button(button_text='Create Reservation', key = '-CREATE_RES-', size = (25,3))],
        [sg.Button(button_text='Display Reservations', key = '-DISPLAY_RES-', size = (25,3))],
        [sg.Button(button_text='Display Rooms', key = '-DISPLAY_ROOMS-', visible = True if userType == "Employee" else False, size = (25,3))],
        [sg.Button(button_text='Manager Report', key = '-REPORT-', visible = True if userType == "Employee" else False, size = (25,3))],
        [sg.Text(infoText, key='-INFO-', font='Default 12', size = (25,30), p = (10,10))]
        ] 
        

    layoutRight = [[Display]]

    layout = [[sg.Col(layoutLeft, p=0), sg.Col(layoutRight, p=0)]]

    # Set up main window
    window = sg.Window("Welcome to Hotel JAB", layout, size=(DISPLAY_W,DISPLAY_H), finalize = True)
    graph = window["-DISPLAY-"]
    graph.draw_image(data=Logo, location=(0,350))


    window['-INFO-'].update(userMessage)
    
    while True:     # The Event Loop
        event, values = window.read()#timeout=1)

        if event in (sg.WIN_CLOSED, 'Exit', None):
            window.close()
            break

        # Check if any GUI elements have been interacted with
        if event == '-SWITCH-':
            currentGuest = None #resets guest information if switch user selected
            print("Clicked Menu 1")
            # A test for the login messages


            #Set employee funcionality to visible or hidden depending on userType
            window['-DISPLAY_GUESTS-'].update(visible = True if userType == 'Employee' else False)
            window['-DISPLAY_ROOMS-'].update(visible = True if userType == 'Employee' else False)
            window['-REPORT-'].update(visible = True if userType == 'Employee' else False)
            window.close()
            Login()

        if event == '-CREATE_RES-':
            print("Clicked Menu 2")
            window['-INFO-'].update("Menu 2 Clicked")
            
            #Brings in value of currentGuest
            #global currentGuest
            #print(f"Current Guest: {currentGuest.fName}")

            print("Selecting room reservation")

            createOrEdit = 'Create'
            roomNumber, rDateStart, rDateEnd,currentGuest  = HandleReservationsWindow(userType,currentGuest,createOrEdit)

            if roomNumber != 0: #If there is a room, start on reservation checks
                roomToReserve = hotel.rooms[int(roomNumber)]
            
                #Once room is selected, checks guest information.
                if currentGuest == None:
                
                    #If none assigned, prompted to fill out guest form
                    print("Get Started by filling out the Guest Form")
                else:    
                    #If form filled out or guest info already assigned. continues to set reservation
                    res = hotel.createReservation(currentGuest.guestID,rDateStart,rDateEnd,roomToReserve.roomNumber)
                    sg.popup(f'Successfully created reservation for {currentGuest.fName}.\nYour Reservation number is {res.reservationNumber}\nA Confirmation e-mail will be sent out shortly.')
            else: #No Room/Window Closed
                print("No Room Selected")

        if event == '-DISPLAY_GUESTS-':

            justDisplayGuests = True
            currentGuest = DisplayGuests(userType,justDisplayGuests)


        if event == '-DISPLAY_ROOMS-':
            print("Clicked Menu 4")
            window['-INFO-'].update("Menu 4 Clicked")  

            # Opens a new window with interactive display for hotel rooms
            DisplayRoomsWindow(currentDate)

        if event == '-DISPLAY_RES-':
            print("Clicked Menu 5")
            window['-INFO-'].update("Menu 5 Clicked")
            userMessage = DisplayReservations(userType,currentGuest)
            window['-INFO-'].update(userMessage)


        if event == '-REPORT-':
            print("Clicked Menu 6")
            window['-INFO-'].update("Menu 6 Clicked")

            GenerateManagerReport()

    window.close()


if __name__ == '__main__':
    Login()



