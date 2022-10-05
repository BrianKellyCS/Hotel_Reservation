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
    
def DisplayRooms():
    print("Displaying Room List")
    # Canvas to display interactable objects
    ROOMS_DISPLAY_W, ROOMS_DISPLAY_H = 400, 400

    GROUND_FLOOR = 1
    MAX_FLOORS = 4

    RoomsDisplay = sg.Graph(
        canvas_size=(ROOMS_DISPLAY_W, ROOMS_DISPLAY_H),
        graph_bottom_left=(0, 0),
        graph_top_right=(ROOMS_DISPLAY_W, ROOMS_DISPLAY_H),
        key="-DISPLAY-",
        background_color='#61CCF6',
        enable_events=True)

    RoomsLayoutR =    [[RoomsDisplay]]
    RoomsLayoutL = [
        [sg.Text("Floor: 1", key='-FLOOR-', font='Default 12', size = (25,1), text_color="White")],
        [sg.Button(button_text='^', key = '-UP-', size = (25,5))],
        [sg.Button(button_text='v', key = '-DOWN-', size = (25,5))]
    ]

    RoomsLayout = [[sg.Col(RoomsLayoutL, p=0), sg.Col(RoomsLayoutR, p=0)]]

    RoomsDisplayWindow = sg.Window("Room Display", RoomsLayout, finalize = True)
    RoomsGraph = RoomsDisplayWindow["-DISPLAY-"]

    currentFloor = 1
    currentFloorText = "Floor:" + str(currentFloor)+ ""
    RoomsDisplayWindow['-FLOOR-'].update("Floor: "+str(currentFloor)+"")

    while True:         # The Event Loop
        event, values = RoomsDisplayWindow.read(timeout=1)
        
        if event in (sg.WIN_CLOSED, 'Exit', None):
            break
        if event == '-UP-':
            if currentFloor < MAX_FLOORS:
                currentFloor += 1
            RoomsDisplayWindow['-FLOOR-'].update("Floor: "+str(currentFloor)+"")

        if event == '-DOWN-':
            if currentFloor > GROUND_FLOOR:
                currentFloor += -1
            RoomsDisplayWindow['-FLOOR-'].update("Floor: "+str(currentFloor)+"")
    

        if event == '-DISPLAY-':
            print("Clicked screen")

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
        [sg.Button(button_text='List All Rooms [Debug]', key = '-MENU3-', size = (25,5))],
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
    totalRooms = 0

    rooms = []
    rooms.append( Room() )

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

            # This adds one to total room count and makes a test room with the given information
            # TODO- Change to take to a form to collect all of the needed information instead
            totalRooms = totalRooms + 1
            print(f"Making room number: {totalRooms}")
            rooms.append(Room(1,totalRooms,True,299,2,"08.04.1992",reserveEnd="08.04.2077"))
            rooms[totalRooms].printInfo()
        
        if event == '-MENU3-':
            print("Clicked Menu 3")
            window['-INFO-'].update("Menu 3 Clicked")
            
            #Prints all room information to console
            for obj in rooms:
                obj.printInfo()
        
        if event == '-MENU4-':
            print("Clicked Menu 4")
            window['-INFO-'].update("Menu 4 Clicked")  

            # Opens a new window with interactive display for hotel rooms
            DisplayRooms()
    window.close()

Main()
