################################################################################################################################################################
# Menu for Hotel Jab Project
# Started 10.1.2022
#
# This is the main menu/ GUI for the Hotel Project. From here we will be able to manage the customers or look up information or save/load information
################################################################################################################################################################
# TODO:
#       * Everything is a wip so far, please ignore any bugs
#       SPRINT 1: https://docs.google.com/document/d/1rrxGAHb_uLp-nZpFUXGhp3va9taUg57OEAkbsngGYAs/
#
###############################################################################
import PySimpleGUI as sg
from Images64 import * # A Seperate python file filled with Base64 strings of our images to make it easier to manage

DISPLAY_W, DISPLAY_H = 600,450
BG_COLOR = "#1E90FF"

print("Starting Menu...")
sg.theme('DarkTeal3')

infoText = "Welcome to JAB Hotel!"
baseCancellationFee = 200

class Customer:
    def __init__(self, name="No Name", phone="No Phone", email="No Email", customerID =0, reservationNumber =0, roomNumber=0, roomType=0, checkedIn="No Reservation", checkedOut="No Reservation", nightsReserved = 0, orderedItems = "None", extrasTotal=0, cancellationFee=0,total=0 ):
        self.name = name
        self.phone = phone
        self.email = email

        self.customerID = customerID
        self.reservationNumber = reservationNumber

        self.roomNumber = roomNumber
        self.roomType = roomType
        self.checkedIn = checkedIn
        self.checkedOut = checkedOut
        self.nightsReserved = nightsReserved
        self.cancellationFee = cancellationFee
        
        self.orderedItems = orderedItems
        self.extrasTotal = extrasTotal
        self.total = total

    def assignCustomerID(self, IDnum): #Assign customer an ID Number
        self.customerID = IDnum

    def assignCustomerInfo(self, list): #Assign customer their information
        self.name = list[0] #Full Name
        self.phone = list[1] #Phone Number
        self.email = list[2] #Email

    def assignRoom(self, list):# Assign room information to customer
        self.roomType = list[0]
        self.roomNumber = list[1]
        self.checkedIn = list[2]
        self.checkedOut = list[3]
        self.nightsReserved = list[4]
        self.cancellationFee = (baseCancellationFee * self.roomType)

    def printInfo(self,verbose=True): #Can print all info or just a little bit
        if (verbose == True):
            print(f"Name #: {self.name} // CustomerID: {self.customerID} // Phone: {self.phone} // Email: {self.email} // roomNumber: {self.roomNumber} // roomType: {self.roomType} // Reservation Start: {self.checkedIn} // Reservation End: {self.checkedOut}")
            print(f"nightsReserved: {self.nightsReserved} // orderedItems: {self.orderedItems} // extrasTotal: {self.extrasTotal} // cancellationFee: {self.cancellationFee} // total: {self.total}")
        else:
            print(f"Name #: {self.name} // CustomerID: {self.customerID} // Phone: {self.phone} // Email: {self.email} // roomNumber: {self.roomNumber}")

class Room:
    def __init__(self,roomType=0,roomNumber=0, roomStatus=False,customerID=0,customerCount=0,reserveStart="No Reservation",reserveEnd="No Reservation"):
        self.roomType = roomType
        self.roomNumber = roomNumber
        self.roomStatus = roomStatus
        self.customerID = customerID
        self.customerCount = customerCount
        self.reserveStart = reserveStart
        self.reserveEnd = reserveEnd

    def cancelBooking(self,reservationNumber): #TODO- Set everything back to default
        print(f"Cancel Booking for reservation number {reservationNumber}")
    
    def setStatus(self,roomStatus): # Set to True or False
        if (roomStatus == True or roomStatus == False):
            self.roomStatus = roomStatus
        else:
            print("ERROR: Failed to set room status: Needs True or False")
    
    def assignRoom(self,reservationNumber,customerID,customerCount,reserveStart,reserveEnd): #TODO- Assign all of the variables to new values
        print(f"Assigning room to Reservation #: {self.reservationNumber}")
        self.reservationNuber = reservationNumber
        self.setStatus(True)

    def printInfo(self,verbose=True): #Can print all info or just a little bit
        if (verbose == True):
            print(f"Room #: {self.roomNumber} // CustomerID: {self.customerID} // Count: {self.customerCount} // Type: {self.roomType} // Status: {self.roomStatus} // Reservation Start: {self.reserveStart} // Reservation End: {self.reserveEnd}")
        else:
            print(f"Room #: {self.roomNumber} // Status: {self.roomStatus} // Reservation Start: {self.reserveStart} // Reservation End: {self.reserveEnd}")

def InformationForm(): # Will let the user input their information
    FormLayout = [
        [sg.Text('Please enter reservation information: ')],
        [sg.Text('First Name', size =(15, 1)), sg.InputText(), sg.Text('Last Name', size =(15, 1), justification='Left'), sg.InputText()],
        [sg.Text('Phone', size =(15, 1)), sg.InputText(), sg.Text('Email', size =(15, 1), justification='Left'), sg.InputText()],
        [sg.Submit(), sg.Cancel()]
    ]
  
    FormWindow = sg.Window('Customer Information Entry', FormLayout)
    event, values = FormWindow.read()

    FormWindow.close()   
    if (event == "Submit"):
        fullname = values[0] + " " + values[1]
        return fullname, values[2], values[3]

    if (event == "Cancel" or event == "Exit" or event == sg.WIN_CLOSED):
        return "No Name Set", "No Phone Set", "No Email Set"

def Login(): #Login Screen to choose which experience to view, returns a string saying what was chosen and a welcome message
    login = [[sg.Button(button_text='EMPLOYEE', key = '-EMPLOYEE-', size = (25,5),p=(100,50))],[sg.Button(button_text='GUEST', key = '-GUEST-', size = (25,5), p=(100,5))]]
    loginWindow = sg.Window("Login Screen", login, size=(400,400), finalize=True)

    #Sets default user message and status to non-specific guest
    userType = "Guest"
    userStatus = "Welcome Valued Customer!"

    while True:
        event, values = loginWindow.read(timeout=60)
        if event == "Exit" or event == sg.WIN_CLOSED:
            print("Defaulting to customer...")
            break

        if event == '-EMPLOYEE-':
            print("This is an employee...")
            userType = "Employee"
            userStatus = "Hello, EMPLOYEE #8180!"
            break

        if event == '-GUEST-': # For if the user selects guest, they can be logged in
            print("This is a customer...")
            userType = "Guest"
            userStatus = "Welcome VALUED CUSTOMER #9999!"
            break

    loginWindow.close()
    return userType, userStatus

def LoadRooms(rooms):
    # Makes all of the rooms for the hotel. If there is a database located, it will load from the database
    # Room 0: Janitors Closet (Empty room, do not assign)
    # Rooms 1-4: Basic room, size 1, Floor 1
    # Rooms 5-8: Basic rooms, size 1, Floor 2
    # Rooms 9-11: Large Rooms, size 2, Floor 3
    # Room 12: Presidential Suite, size 3, Floor 4 (only one)

    totalRooms = 13
    currentRoom = 0
    for x in range(currentRoom,totalRooms):
        rooms.append( Room(roomNumber = currentRoom) )
        currentRoom += 1

    # Test Rooms, uncomment them to see them turn in DisplayRooms
    # If you set their status to "True" they will show up red (room is full, can't reserve)
    #rooms[1].setStatus(True) 
    rooms[2].setStatus(True)
    #rooms[3].setStatus(True)
    #rooms[4].setStatus(True)
    #rooms[5].setStatus(True)
    #rooms[6].setStatus(True)
    rooms[7].setStatus(True)
    #rooms[8].setStatus(True)
    rooms[9].setStatus(True)
    #rooms[10].setStatus(True)
    rooms[11].setStatus(True)
    rooms[12].setStatus(True)

    return rooms

def DisplayRooms(rooms):
    print("Displaying Room List")
    # Canvas to display interactable objects
    ROOMS_DISPLAY_W, ROOMS_DISPLAY_H = 400, 400

    GROUND_FLOOR = 1
    MAX_FLOORS = 4

    currentFloor = 1
    currentFloorText = "Floor: " + str(currentFloor)+ ""
    floorChanged = False

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
        [sg.Text("Floor: 1", key='-FLOOR-', font='Default 12', size = (25,1), text_color="White")],
        [sg.Button(button_text='^', key = '-UP-', size = (25,5))],
        [sg.Button(button_text='v', key = '-DOWN-', size = (25,5))]
    ]

    RoomsLayout = [[sg.Col(RoomsLayoutL, p=0), sg.Col(RoomsLayoutR, p=0)]]

    RoomsDisplayWindow = sg.Window("Room Display", RoomsLayout, finalize = True)
    RoomsGraph = RoomsDisplayWindow["-DISPLAY-"]

    # Draw floorplan and room availability (From left to right 1-4)
    # Each room has two images, Full (Red) and Empty (Green)
    #RoomsGraph.draw_image(data=Floorplan, location=(0,ROOMS_DISPLAY_H))
    floorplans = [    RoomsGraph.draw_image(data=Floorplan, location=(0,ROOMS_DISPLAY_H)),  RoomsGraph.draw_image(data=FloorThree, location=(0,0)),RoomsGraph.draw_image(data=FloorFour, location=(0,0)) ]
    roomCoords = [(0,0),(19,150),(97,309),(224,309),(302,150)]
    roomMedCoords = [(0,0),(19,329),(146,329),(272,329)]
    roomLargeCoords = [(0,0),(90,349)]

    roomSquares = [ RoomsGraph.draw_image(data=RoomFull, location=(0,0)),   
                    RoomsGraph.draw_image(data=RoomEmpty, location=(0,0)), 
                    RoomsGraph.draw_image(data=RoomFull, location=(0,0)),
                    RoomsGraph.draw_image(data=RoomEmpty, location=(0,0)),
                    RoomsGraph.draw_image(data=RoomFull, location=(0,0)),
                    RoomsGraph.draw_image(data=RoomEmpty, location=(0,0)), 
                    RoomsGraph.draw_image(data=RoomFull, location=(0,0)),
                    RoomsGraph.draw_image(data=RoomEmpty, location=(0,0)) ]
    
    roomMed = [ RoomsGraph.draw_image(data=RoomMedFull, location=(0,0)),   
                RoomsGraph.draw_image(data=RoomMedEmpty, location=(0,0)), 
                RoomsGraph.draw_image(data=RoomMedFull, location=(0,0)),
                RoomsGraph.draw_image(data=RoomMedEmpty, location=(0,0)),
                RoomsGraph.draw_image(data=RoomMedFull, location=(0,0)),
                RoomsGraph.draw_image(data=RoomMedEmpty, location=(0,0)), 
    ]

    roomLarge = [   RoomsGraph.draw_image(data=RoomLargeFull, location=(0,0)),   
                    RoomsGraph.draw_image(data=RoomLargeEmpty, location=(0,0)), 
    ]
    #roomSquares = [roomOneFull, roomOneEmpty, roomTwoFull,roomTwoEmpty, roomThreeFull,roomThreeEmpty,roomFourFull,roomFourEmpty]
    
    #Room 1
    if rooms[1].roomStatus == 1: #Taken
        RoomsGraph.relocate_figure(roomSquares[0],roomCoords[1][0],roomCoords[1][1])
    else:
        RoomsGraph.relocate_figure(roomSquares[1],roomCoords[1][0],roomCoords[1][1])

    #Room 2
    if rooms[2].roomStatus == 1:
        RoomsGraph.relocate_figure(roomSquares[2],roomCoords[2][0],roomCoords[2][1])
    else:
        RoomsGraph.relocate_figure(roomSquares[3],roomCoords[2][0],roomCoords[2][1])

    #Room 3
    if rooms[3].roomStatus == 1:
        RoomsGraph.relocate_figure(roomSquares[4],roomCoords[3][0],roomCoords[3][1])
    else:
        RoomsGraph.relocate_figure(roomSquares[5],roomCoords[3][0],roomCoords[3][1])

    #Room 4
    if rooms[4].roomStatus == 1:
        RoomsGraph.relocate_figure(roomSquares[6],roomCoords[4][0],roomCoords[4][1])
    else:
        RoomsGraph.relocate_figure(roomSquares[7],roomCoords[4][0],roomCoords[4][1])

    RoomsDisplayWindow['-FLOOR-'].update(currentFloorText)

    fig = None
    last_clicked = 0

    while True:         # The Event Loop
        event, values = RoomsDisplayWindow.read(timeout=1)
        
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

                    if rooms[currRoom].roomStatus == 1: #Full
                        print(f"Room{currRoom} // {x} is Taken!")
                        RoomsGraph.relocate_figure(roomSquares[fullx],roomCoords[x][0],roomCoords[x][1])
                        RoomsGraph.relocate_figure(roomSquares[emptyx],roomCoords[0][0],roomCoords[0][1])
                    else:
                        print(f"Room:{currRoom} // {x} is not taken")
                        RoomsGraph.relocate_figure(roomSquares[emptyx],roomCoords[x][0],roomCoords[x][1])
                        RoomsGraph.relocate_figure(roomSquares[fullx],roomCoords[0][0],roomCoords[0][1])

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

                    if rooms[currRoom].roomStatus == 1:
                        print(f"Room{currRoom} // {x} is Taken!")
                        RoomsGraph.relocate_figure(roomMed[fullx],roomMedCoords[x][0],roomMedCoords[x][1])
                        RoomsGraph.relocate_figure(roomMed[emptyx],roomMedCoords[0][0],roomMedCoords[0][1])
                    else:
                        print(f"Room:{currRoom} // {x} is not taken")
                        RoomsGraph.relocate_figure(roomMed[emptyx],roomMedCoords[x][0],roomMedCoords[x][1])
                        RoomsGraph.relocate_figure(roomMed[fullx],roomMedCoords[0][0],roomMedCoords[0][1])

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

                    if rooms[currRoom].roomStatus == 1:
                        print(f"Room{currRoom} is Taken!")
                        RoomsGraph.relocate_figure(roomLarge[fullx],roomLargeCoords[1][0],roomLargeCoords[1][1])
                        RoomsGraph.relocate_figure(roomLarge[emptyx],roomLargeCoords[0][0],roomLargeCoords[0][1])
                    else:
                        print(f"Room:{currRoom} is not taken")
                        RoomsGraph.relocate_figure(roomLarge[emptyx],roomLargeCoords[1][0],roomLargeCoords[1][1])
                        RoomsGraph.relocate_figure(roomLarge[fullx],roomLargeCoords[0][0],roomLargeCoords[0][1])

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
            if last_clicked == 4 or last_clicked == 5:
                print(f'Room 1')
            if last_clicked == 6 or last_clicked == 7:
                print('Room 2')
            if last_clicked == 8 or last_clicked == 9:
                print('Room 3')
            if last_clicked == 10 or last_clicked == 11:
                print('Room 4')
            if last_clicked == 12 or last_clicked == 13:
                print("Room 1 Third Floor")
            if last_clicked == 14 or last_clicked == 15:
                print("Room 2 Third Floor")
            if last_clicked == 16 or last_clicked == 17:
                print("Room 3 Third Floor")
            if last_clicked == 18 or last_clicked == 19:
                print("Presidential Suite- Fourth Floor")
            last_clicked = None

    RoomsDisplayWindow.close()

def Main(): #Main Menu, launches all of the options
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
        [sg.Button(button_text='Login', key = '-MENU1-', size = (25,5))],
        [sg.Button(button_text='Create Test Room [Debug]', key = '-MENU2-', size = (25,5))],
        [sg.Button(button_text='Customer Form [Debug]', key = '-MENU3-', size = (25,5))],
        [sg.Button(button_text='Display Rooms', key = '-MENU4-', size = (25,5))],
        [sg.Text(infoText, key='-INFO-', font='Default 12', size = (25,30), p = (10,10))]
        ]

    layoutRight = [[Display]]

    layout = [[sg.Col(layoutLeft, p=0), sg.Col(layoutRight, p=0)]]

    # First start user login popup
    userType, userMessage = Login()

    # Set up main window
    window = sg.Window("Welcome to Hotel JAB", layout, size=(DISPLAY_W,DISPLAY_H), finalize = True)
    graph = window["-DISPLAY-"]
    graph.draw_image(data=Logo, location=(0,350))

    window['-INFO-'].update(userMessage)
    
    # Creates an empty list to store the rooms in and creates an empty test room
    #totalRooms = 0

    rooms = []
    LoadRooms(rooms)
    #rooms.append( Room() )

    customers = []
    customers.append( Customer() )
    
    while True:     # The Event Loop
        event, values = window.read()#timeout=1)

        if event in (sg.WIN_CLOSED, 'Exit', None):
            break

        # Check if any GUI elements have been interacted with
        if event == '-MENU1-':
            print("Clicked Menu 1")
            # A test for the login messages
            userType, userMessage = Login()
            window['-INFO-'].update(userMessage)

        if event == '-MENU2-':
            print("Clicked Menu 2")
            window['-INFO-'].update("Menu 2 Clicked")
            
            for obj in rooms:
                obj.printInfo()
            # This adds one to total room count and makes a test room with the given information
            # TODO- Change to take to a form to collect all of the needed information instead
            #rooms.append( Room() )
            #totalRooms = totalRooms + 1
            #print(f"Making room number: {totalRooms}")
            #rooms.append(Room(1,totalRooms,True,299,2,"08.04.1992",reserveEnd="08.04.2077"))
            #rooms[totalRooms].printInfo()
        
        if event == '-MENU3-':
            print("Clicked Menu 3")
            window['-INFO-'].update("Menu 3 Clicked")
            #Prints all room information to console
            #for obj in rooms:
            #    obj.printInfo()

            customers[0].assignCustomerInfo( InformationForm() )
            customers[0].printInfo()

        if event == '-MENU4-':
            print("Clicked Menu 4")
            window['-INFO-'].update("Menu 4 Clicked")  

            # Opens a new window with interactive display for hotel rooms
            DisplayRooms(rooms)
    window.close()

Main()
