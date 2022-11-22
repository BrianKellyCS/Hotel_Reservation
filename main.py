
################################################################################################################################################################
# Menu for Hotel Jab Project
# Started 10.1.2022
#
# This is the main menu/ GUI for the Hotel Project. From here we will be able to manage the Guests or look up information or save/load information
################################################################################################################################################################
# TODO:
#       * Everything is a wip so far, please ignore any bugs
#       SPRINT 1: https://docs.google.com/document/d/1rrxGAHb_uLp-nZpFUXGhp3va9taUg57OEAkbsngGYAs/
#
###############################################################################
import PySimpleGUI as sg
from Images64 import * # A Seperate python file filled with Base64 strings of our images to make it easier to manage
from classes.hotel import Hotel
from datetime import date

DISPLAY_W, DISPLAY_H = 600,450
BG_COLOR = "#1E90FF"

print("Starting Menu...")
sg.theme('DarkTeal3')

infoText = "Welcome to JAB Hotel!"
hotel = Hotel()
hotel.initializeHotelData()
rooms = hotel.rooms
currentDate = date.today().strftime("%m/%d/%Y") #for default date to pass to function


def Login(): #Login Screen to choose which experience to view, returns a string saying what was chosen and a welcome message
    login = [[sg.Button(button_text='EMPLOYEE', key = '-EMPLOYEE-', size = (25,5),p=(100,50))],[sg.Button(button_text='GUEST', key = '-GUEST-', size = (25,5), p=(100,5))]]
    loginWindow = sg.Window("Login Screen", login, size=(400,400), finalize=True)

    #Sets default user message and status to non-specific guest
    userType = "Guest"
    userStatus = "Welcome Valued Guest!"

    while True:
        event, values = loginWindow.read(timeout=60)
        if event == "Exit" or event == sg.WIN_CLOSED:
            print("Defaulting to guest...")
            loginWindow.close()
            return userType, userStatus


        if event == '-EMPLOYEE-':
            print("This is an employee...")
            userType = "Employee"
            userStatus = "Hello, EMPLOYEE #8180!"
            loginWindow.close()
            return userType, userStatus


        if event == '-GUEST-': # For if the user selects guest, they can be logged in
            print("This is a guest...")
            userType = "Guest"
            userStatus = "Welcome VALUED Guest #9999!"
            loginWindow.close()
            return userType, userStatus

def InformationForm(): # Will let the user input their information
    FormLayout = [
        [sg.Text('Please enter reservation information: ')],
        [sg.Text('First Name', size =(15, 1)), sg.InputText(), sg.Text('Last Name', size =(15, 1), justification='Left'), sg.InputText()],
        [sg.Text('Phone', size =(15, 1)), sg.InputText(), sg.Text('Email', size =(15, 1), justification='Left'), sg.InputText()],
        [sg.Submit(), sg.Cancel()]
    ]
  
    FormWindow = sg.Window('Guest Information Entry', FormLayout)
    event, values = FormWindow.read()

    FormWindow.close()   
    if (event == "Submit"):
        if values[0] == '' or values [1] == '' or values [2] == '' or values [3] == '':
            print('Information not saved. Must fill out form completely')
        else:
            return values[0], values[1], values[2], values[3]

    if (event == "Cancel" or event == "Exit" or event == sg.WIN_CLOSED):
        return None



def SearchRoomsWindow():
    SEARCH_CANVAS_W, SEARCH_CANVAS_H = 300,350
    
    RoomTypeList = ["Basic", "Deluxe", "Suite"]
    SearchList = ["None"]
    roomChosen,roomSelected,roomDateStart,roomDateEnd = 0,0,"No Date","No Date"

    SearchLayout = [
        [sg.Text("Select Reservation Information: ", key='-RESERVETEXT-', font='Default 12', size = (30,1))],
        [sg.CalendarButton('Select Date',  target='-DATE-', format='%m/%d/%Y'), sg.Input(key='-DATE-', size=(20,1)), sg.CalendarButton('Select End Date',  target='-ENDDATE-', format='%m/%d/%Y'), sg.Input(key='-ENDDATE-', size=(20,1)) ],
        [sg.Text("Room Type ", key='-ROOMTYPETEXT-', size = (12,1)), sg.Combo(RoomTypeList, s=(15,22), enable_events=True, readonly=True, k='-ROOMTYPE-'), sg.Text("Room Number ", key='-ROOMCHOSENTEXT-', size = (12,1), justification="right"), sg.Combo(SearchList,default_value="None", s=(10,22), enable_events=True, readonly=True, k='-SEARCH-'), ],  
        [sg.Submit(key='-SUBMIT-'), sg.Cancel()]
    ]

    SearchWindow = sg.Window('Search Rooms', SearchLayout)

    while True:
        event, values = SearchWindow.read()
        if event in (sg.WIN_CLOSED, 'Exit', 'Cancel', None):
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

            if roomChosen == "None" or roomChosen == None:
                roomSelected = 0
                roomDateStart = "No Date"
                roomDateEnd = "No Date"

        if (event == "-SUBMIT-"):
            roomSelected = roomChosen
            roomDateStart = values['-DATE-']
            roomDateEnd = values['-ENDDATE-']
            break

    SearchWindow.close()
    print(f"Sending back: {roomChosen}")
    return roomSelected, roomDateStart, roomDateEnd

   
def DisplayRoomsWindow(currentDate):
    dateToDisplay = currentDate
    print("Displaying Room List")
    # Size of room display and the floors of the hotel display
    ROOMS_DISPLAY_W, ROOMS_DISPLAY_H = 400, 400

    GROUND_FLOOR = 1
    MAX_FLOORS = 4

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
        [sg.CalendarButton('Select Date',  target='-DATE-', format='%m/%d/%Y'), sg.Input(key='-DATE-', size=(10,1)) ],
        [sg.Button(button_text='Submit', key = '-SUBMIT-', size = (5,1))],
        [sg.Text("Floor: 1", key='-FLOOR-', font='Default 12', size = (25,1), text_color="White")],
        [sg.Button(button_text='^', key = '-UP-', size = (25,5))],
        [sg.Button(button_text='v', key = '-DOWN-', size = (25,5))]
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
                print(hotel.getReservationByRoom(1,dateToDisplay))
            if (last_clicked == 6 or last_clicked == 7) and currentFloor == 1:
                print(hotel.getReservationByRoom(2,dateToDisplay))
            if (last_clicked == 8 or last_clicked == 9) and currentFloor == 1:
                print(hotel.getReservationByRoom(3,dateToDisplay))
            if (last_clicked == 10 or last_clicked == 11) and currentFloor == 1:
                print(hotel.getReservationByRoom(4,dateToDisplay))
            if (last_clicked == 4 or last_clicked == 5) and currentFloor == 2:
                print(hotel.getReservationByRoom(5,dateToDisplay))
            if (last_clicked == 6 or last_clicked == 7) and currentFloor == 2:
                print(hotel.getReservationByRoom(6,dateToDisplay))
            if (last_clicked == 8 or last_clicked == 9) and currentFloor == 2:
                print(hotel.getReservationByRoom(7,dateToDisplay))
            if (last_clicked == 10 or last_clicked == 11) and currentFloor == 2:
                print(hotel.getReservationByRoom(8,dateToDisplay))
            if last_clicked == 12 or last_clicked == 13:
                print(hotel.getReservationByRoom(9,dateToDisplay))
            if last_clicked == 14 or last_clicked == 15:
                print(hotel.getReservationByRoom(10,dateToDisplay))
            if last_clicked == 16 or last_clicked == 17:
                print(hotel.getReservationByRoom(11,dateToDisplay))
            if last_clicked == 18 or last_clicked == 19:
                print(hotel.getReservationByRoom(12,dateToDisplay))
            last_clicked = None

    RoomsDisplayWindow.close()


def GenerateManagerReport():
    print("Starting Manager Report")
    REPORT_DISPLAY_W, REPORT_DISPLAY_H = 500, 150
    JAB_MINI_W, JAB_MINI_H = 300, 350

    #Get current date and extract the month number from it
    dateToDisplay = currentDate
    currentMonth = int(dateToDisplay[0] + dateToDisplay[1])

    MonthsList = ['January', 'February', 'March', 'April', 'May','June','July','August','September','October','November','December']
    YearsList = ['2022']
    ReportList = ['Reservations', 'Profits']
    TimeList = ['Weekly','Monthly', 'Yearly']

    TwentyEightDays = [2]
    ThirtyDays = [4,6,9,11]
    ThirtyOneDays = [ 1,3,5,7,8,10,12]

    displayString = ""
    for guest in hotel.guests:
        displayString = displayString + str(guest) + "\n"

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

    GuestLayout = [[sg.T("Customer Information:", s=(50,1))],
    #[sg.Table([["Bob","Smith",3,"111-111-1111","11/01/2022","11/02/2022"], ["555-555-5555",5,6],[],[]], ['First Name','Last Name','ID','Phone','Start','End' ], alternating_row_color="#394a6d", max_col_width = 10, num_rows=15)]
    [sg.Multiline(default_text=displayString,size=(60,15), font='Courier 8', expand_x=True, expand_y=True, write_only=True, enable_events = True, autoscroll=True, auto_refresh=True)]
    ]
    WeeklyLayout = [[sg.T("Sort by Week", s=(15,1))],
    [sg.Table([["BobBOBbobBOBbobby","SmithJohnSon",3,"111-111-1111","11/01/2022","11/02/2022"], ["555-555-5555",5,6],[],[]], ['First Name','Last Name','ID','Phone','Start','End'], justification="left", alternating_row_color="#394a6d", auto_size_columns=True, max_col_width = 14, num_rows=15)]

    ]
    MonthlyLayout = [[sg.T("Sort by Month", s=(50,1))]]
    YearlyLayout = [[sg.T("Sort by Year", s=(15,1))]]


    ReportLayoutL = [
        [sg.Text("Manager's Report", font='Default 12', text_color = "white", size = (30,1))],
        [sg.CalendarButton('Select Date',  target='-DATE-', format='%m/%d/%Y'), sg.Input(key='-DATE-', size=(20,1))],
#        [sg.Text("Month", size = (6,1)), sg.Combo(MonthsList, s=(15,22), default_value = MonthsList[currentMonth-1], enable_events=True, readonly=True, k='-MONTHSELECT-'), sg.Combo(YearsList, s=(7,22), default_value = YearsList[0], enable_events=True, readonly=True, k='-YEARSELECT-')], 
        [sg.Text("Sort by", size = (6,1)), sg.Combo(ReportList, default_value=ReportList[0], s=(15,22), enable_events=True, readonly=True, k='-TIMESELECT-'), ],
        [sg.Button(button_text='Return', key = '-RETURN-', size = (10,1), pad = (125,20))],
        [JabMiniDisplay]
    ]
    ReportLayoutR =    [[ReportDisplay],
    [sg.Text('Information:',s=(15,1))], 
#    [sg.TabGroup([[sg.Tab('Tab1',[[sg.T("Text1", s=(15,2))]]), sg.Tab('Tab2', [[sg.T("Text2", s=(15,2)) ]]) ]]) ]
    [sg.TabGroup([[sg.Tab('Guest Information', GuestLayout, key="-GUESTTAB-" ),sg.Tab('Monthly',  MonthlyLayout ), sg.Tab('Weekly',  WeeklyLayout ),  sg.Tab('Yearly',  YearlyLayout ,visible=True,key='-YEARLYTAB-')]], size = (550,300) )]
    ]

#    print(hotel.guests[0].fName)

    ReportLayout = [[sg.Col(ReportLayoutL, p=0, vertical_alignment="t"), sg.Col(ReportLayoutR, p=0, vertical_alignment="t")]]

    ReportDisplayWindow = sg.Window("Manager's Report", ReportLayout, finalize = True)
    ReportGraph = ReportDisplayWindow["-REPORTDISPLAY-"]

    JabMiniImage = ReportDisplayWindow["-REPORTDISPLAY-"]
    JabMiniImage.draw_image(data=Logo, location=(0,350))

    #DisplayGuests()
    while True:         # The Event Loop
        event, values = ReportDisplayWindow.read(timeout=1)
        
        if event in (sg.WIN_CLOSED, 'Exit', '-RETURN-', None):
            break

        if (event == "-TIMESELECT-"):
            typeChosen = values[event]

            SearchList = []
            if values['-DATE-'] != '':
                workingDate = values['-DATE-']
                currentMonth = int(values['-DATE-'][0] + values['-DATE-'][1])
                print(workingDate)
                if currentMonth in ThirtyDays:
                    print("YOUR MONTH HAS THIRTY DAYS!!!")
                if currentMonth in ThirtyOneDays:
                    print("Your Month has thirty ONE DAYS")
                if currentMonth in TwentyEightDays:
                    print("This is Februrary")

    ReportDisplayWindow.close()
#                SearchList = hotel.searchRooms(typeChosen,values['-DATE-'],values['-ENDDATE-'])
#            SearchWindow['-SEARCH-'].update(value="None", values=SearchList)
#            roomChosen = 0


def DisplayReservations():
    for res in hotel.reservations:
        print(res)

def DisplayGuests():
    for guest in hotel.guests:
        print(guest)

def Main(): #Main Menu, launches all of the options
    global userType
    currentGuest = None
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
        [sg.Button(button_text='Switch User', key = '-MENU1-', size = (25,3))],
        [sg.Button(button_text='Guest Form', key = '-MENU3-', size = (25,3))],
        [sg.Button(button_text='Search Rooms', key = '-MENU2-', size = (25,3))],
        [sg.Button(button_text='Display Rooms', key = '-MENU4-', visible = True if userType == "Employee" else False, size = (25,3))],
        [sg.Button(button_text='Display Reservations', key = '-MENU5-', visible = True if userType == "Employee" else False, size = (25,3))],
        [sg.Button(button_text='Display Guests', key = '-MENU6-', visible = True if userType == "Employee" else False, size = (25,3))],
        [sg.Text(infoText, key='-INFO-', font='Default 12', size = (25,30), p = (10,10))]
        ] 
        

    layoutRight = [[Display]]

    layout = [[sg.Col(layoutLeft, p=0), sg.Col(layoutRight, p=0)]]

    # Set up main window
    window = sg.Window("Welcome to Hotel JAB", layout, size=(DISPLAY_W,DISPLAY_H), finalize = True)
    graph = window["-DISPLAY-"]
    graph.draw_image(data=Logo, location=(0,350))

    global userMessage
    window['-INFO-'].update(userMessage)
    
    while True:     # The Event Loop
        event, values = window.read()#timeout=1)

        if event in (sg.WIN_CLOSED, 'Exit', None):
            break

        # Check if any GUI elements have been interacted with
        if event == '-MENU1-':
            currentGuest = None #resets guest information if switch user selected
            print("Clicked Menu 1")
            # A test for the login messages
            userType, userMessage = Login()
            window['-INFO-'].update(userMessage)

            #Set employee funcionality to visible or hidden depending on userType
            window['-MENU4-'].update(visible = True if userType == 'Employee' else False)
            window['-MENU5-'].update(visible = True if userType == 'Employee' else False)
            window['-MENU6-'].update(visible = True if userType == 'Employee' else False)

        if event == '-MENU2-':
            print("Clicked Menu 2")
            window['-INFO-'].update("Menu 2 Clicked")
            
            #Brings in value of currentGuest
            #global currentGuest
            print(f"Current Guest: {currentGuest}")


            print("Selecting room reservation")
            r, rDateStart, rDateEnd  = SearchRoomsWindow()

            if r != 0: #If there is a room, start on reservation checks
                roomToReserve = hotel.rooms[int(r)]
            
                #Once room is selected, checks guest information.
                if currentGuest == None:
                
                    #If none assigned, prompted to fill out guest form
                    print("Get Started by filling out the Guest Form")
                else:    
                    #If form filled out or guest info already assigned. continues to set reservation
                    print(rDateStart)
                    print(rDateEnd)
                    hotel.createReservation(currentGuest.guestID,rDateStart,rDateEnd,roomToReserve.roomNumber) #Example reservation
            else: #No Room/Window Closed
                print("No Room Selected")

        if event == '-MENU3-':
            print("Clicked Menu 3")
            window['-INFO-'].update("Menu 3 Clicked")

            #Updates currentGuest value from form
            currentGuest = hotel.createGuest(InformationForm())
            if currentGuest != None: #If user exits form before filling out
                print("Updated Current Guest to:",currentGuest.fName,currentGuest.lName, "(ID: ",currentGuest.guestID,")")

        if event == '-MENU4-':
            print("Clicked Menu 4")
            window['-INFO-'].update("Menu 4 Clicked")  

            # Opens a new window with interactive display for hotel rooms
            DisplayRoomsWindow(currentDate)

        if event == '-MENU5-':
            print("Clicked Menu 5")
            window['-INFO-'].update("Menu 5 Clicked")

            DisplayReservations()

        if event == '-MENU6-':
            print("Clicked Menu 6")
            window['-INFO-'].update("Menu 6 Clicked")

            #DisplayGuests()
            GenerateManagerReport()

    window.close()




# First start user login popup to get userType
userType, userMessage = Login()

Main()

