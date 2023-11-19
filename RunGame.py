#Harleen Kaur Hans
#Features chosen to implement: Accessing settings from text file 
#Anomaly that was added: Number Anomaly
#Any unique data it checks for: Digits/Numbers
#Any changes to rooms that were made to support this anomaly: Number/Digits were added to some rooms. But this code works fine even
#in those cases as it is designed to create number anomaly in some other room if there was no digit in room items in current room in accordance with
#this line: "In all cases, if the anomaly cannot be added to a room (i.e., add_anomaly() returns False), it should try another" in Assignmnet08 instructions. 

#Response to pair programming questions
#1. How did you pair program? We met in person ,shared screens at times and used github to share code and commit changes. 
#2. Did you work on any parts independently, and what parts if so? Yes, my partner did research on checking number in item at last index and
#   I worked  to make anomaly function work on another rooms if there is no digit in room items in current room.
#3. What tasks came up that were not planned in Assignment 8, if any? No, it worked well as per our expectations. Though new tasks camp
#   up while we were designing algorithm (bonus part) of Assignmnet 08 which was : handling digit at last index of room item
#4. About how often did you change who was driver and who was navigator? We changed it once after coding/designing Category 1 part
#   to ensure that we both had experience of being a navigator and driver. 
#5. If you were to pair program in the future, what changes will you make? We will try to switch roles of navigator and driver more frequently as 
#   it helped us to detect potential issued with our code and will try to make communications more clear and concrete to increase efficiency. 

import Duty
import random
import sys

def main():
    """
    The main function is mostly just here to setup the game and keep it running in a loop.
    It has a specific order of events that it follows.
    There are a lot of comments in here to help you understand what is going on, but 
    feel free to remove them if they impede your reading of the code.
    """

    # First, we set up all of the game data. 
    # This could have been done using the init() function's optional parameters,
    # but this should make it easier for you to modify it later.

    # These 'helper functions' just clean up the main function and make it more readable.
    # We need to add rooms to the game and we need to register what anomalies are possible.
    add_rooms()
    register_anomalies()

    # # It might be cleaner to put all of these into their own helper function. Feel free to do that if you think it would be better!
    

    

    if(len(sys.argv)>1):
        #Setting functionlaity to read settings from text file
        file=sys.argv[1]
        file_handler=open(file,"r")
        
        while True:
            #Initialisng file handler 
            file_data=file_handler.readline()

            #When empty line appears/ entire content of file is read 
            if(file_data==""):
                break
            #Accessing data from text file and using it to set settings 
            file_data=file_data.split(":")
            Duty.set_setting(file_data[0],file_data[1] ) 
        
        #Closing file handler 
        file_handler.close()

    #No command line argument is given 
    else:

        #Finalising default settings 
        Duty.set_setting("debug", True) 
        Duty.set_setting("timescale", 60)
        Duty.set_setting("probability", 0.1)
        Duty.set_setting("min_seconds_between_anomalies", 10*60)

    # Initialize the game with all of the data we've just set up.
    Duty.init()

    # This is the main game loop. It will run until the game_running variable is set to False.
    game_running = True
    while game_running:
        # The game keeps track of time while the player is idle, so it is possible we will need
        # to create multiple anomalies at a time the next time the player types a command.
        # `number_of_anomalies_to_create` also takes our probability setting into account.
        n_anomalies = Duty.number_of_anomalies_to_create()

        # We create one anomaly at a time, and we'll write a small helper function to clean up the main function.
        for _ in range(n_anomalies):
            # Keep looping until we can create the anomaly, just in case one of them fails
            anomaly_created = False
            while not anomaly_created:
                anomaly_created = create_anomaly()
            

        # This will update the game status to check if we've lost the game or reached the end.
        # Update returns True if the game should keep going or False if it should end after this loop.
        game_running = Duty.update()

        # Display shows all of the game data. If update() determined the game should end, display() will show the end screen.
        Duty.display()

        # This will pause the loop and wait for the user to type something, running the appropriate commands
        # to handle their actions.
        Duty.handle_input()

def add_rooms():
    """
    Adds all of the rooms to the game. 
    Duty.add_room() takes a string for the name of a room and a list of strings for the items in the room.
    """

    Duty.add_room("Living Room", ["42 \" TV Playing Golf", "Black Leather Sofa", "Circular Metal Coffee Table", "Wooden Bookshelf with 3 Shelves"])
    Duty.add_room("Kitchen", ["Gas Stove", "Retro Red Metal Refrigerator", "Oak Wooden Table", "4 Wooden Chairs"])
    Duty.add_room("Bedroom", ["Queen Size Bed", "Oak Wooden Nightstand", "Oak Wooden Dresser", "Oak Wooden Desk", "2 Oak Wooden Chairs"])
    Duty.add_room("Bathroom", ["Toilet with Oak Seat", "3 Chrome Sinks", "Shower with Blue Tiles", "Medicine Cabinet"])
    Duty.add_room("Garage",["Car","Screw Driver  no: 3"])

def register_anomalies():
    """
    Each anomaly we want to add to the game must be "Registered". 
    This is so the game knows what anomalies are possible.
    They will all be stored in UPPERCASE to make it easier to compare them later.
    """
    Duty.register_anomaly("CAMERA MALFUNCTION")
    Duty.register_anomaly("MISSING ITEM")
    Duty.register_anomaly("ITEM MOVEMENT")
    #Registering new number anomaly
    Duty.register_anomaly("NUMBER ANOMALY")


def create_anomaly() -> bool:
    """
    This little helper function handles the control flow for three steps:
    1. Choose a random room that does not have an anomaly, because rooms can only have one anomaly.
    2. Choose a random anomaly from the list of registered anomalies.
    3. Create the anomaly in the room.

    Return True if an anomaly was created, False if no anomaly was created.
    """

    # Choose a random room that does not have an anomaly
    room = Duty.get_random_unchanged_room()

    # Pick a random anomaly from the list of registered anomalies
    # Note: It is possible that some anomalies you create can't work in every room.
    # Maybe you will need additional logic to make sure the anomaly makes sense in the room.
    anomaly = Duty.get_random_anomaly()

    # Camera Malfunction is actually a special one.
    # It will not show this camera when clicking through if 
    # It sees CAMERA MALFUNCTION as the anomaly name
    if anomaly == "CAMERA MALFUNCTION":
        # All anomalies are stores as all uppercase
        # Since a camera malfunction means no items are shown, we pass an empty list
        return Duty.add_anomaly("CAMERA MALFUNCTION", room, [])
    elif anomaly == "MISSING ITEM":
        # We pass the name of the room to these functions to separate out the logic
        return missing_item(room)
    elif anomaly == "ITEM MOVEMENT":
        return item_movement(room)
    
    # Calling number_anomaly function if it is the anomlay to be created 
    elif anomaly=="NUMBER ANOMALY":
        bool=number_anomaly(room)

        #getting list of rooms 
        rooms=Duty.get_rooms()

        #Calling number_anomaly function on another room if it returns false on current room and returning True otherwise 
        for i in rooms:
            if bool==True:
                return bool
            else:
                bool=number_anomaly(room)    
        return bool
            
    else:
        print(f"ERROR: Anomaly {anomaly} not found")
        return False

def missing_item(room: str) -> bool:
    """
    Removes a random item from the room. This is a pretty straightforward one.
    1. Get the list of items in the room. (Duty.get_room_items())
    2. Choose a random item to remove. (random.randint())
    3. Make a copy of the list of items and remove the item from the copy. (list slicing)
    4. Create the anomaly with the new list of items. (Duty.add_anomaly())
    """
    items = Duty.get_room_items(room)
    item_index_to_remove = random.randint(0, len(items)-1)
    new_items = items[:]
    new_items.pop(item_index_to_remove)
    
    # add_anomaly returns True if the anomaly was created, False if it was not.
    return Duty.add_anomaly("MISSING ITEM", room, new_items)

def item_movement(room: str) -> bool:
    """
    Re-arranges two items in a room. This one is a little more complicated.
    1. Get the list of items in the room. (Duty.get_room_items())
    2. Choose two random items to swap. (random.randint())
    3. Make a copy of the list of items and swap the two items. (list slicing)
    4. Create the anomaly with the new list of items. (Duty.add_anomaly())
    """

    items = Duty.get_room_items(room)

    # If there is only one item in the room, we can't move anything!
    if len(items) < 2:
        return False

    # Find two random items to swap
    item_to_move = random.randint(0, len(items)-1)
    item_to_move_to = random.randint(0, len(items)-1)

    # Make sure the two items are not the same
    while item_to_move == item_to_move_to:
        item_to_move_to = random.randint(0, len(items)-1)

    # Make a copy to avoid accidentally modifying the original item list
    new_items = items[:]

    # The below swap is also possible with the line: new_items[item_to_move], new_items[item_to_move_to] = new_items[item_to_move_to], new_items[item_to_move]
    item_a = new_items[item_to_move]
    item_b = new_items[item_to_move_to]
    new_items[item_to_move] = item_b
    new_items[item_to_move_to] = item_a

    return Duty.add_anomaly("ITEM MOVEMENT", room, new_items)


def number_anomaly(room: str)->bool:

    #List of all items in room 
    items = Duty.get_room_items(room)

    #Creating deep copy of items 
    new_items=items[:]
    i=0
    bool=True

    #Traversing items in room  
    while(i<len(items)):
        j=0

        #Traversing single room item character by character 
        while (j<len(items[i])):

            #Checking if character is digit 
            if (items[i][j].isdigit() and (items[i][-1].isdigit() or items[i][j+1]==" ")):

                # +1/-1 on digit at random 
                x=random.randint(-1,1)
                while(x==0):
                    x=random.randint(-1,1)

                #Changing room item in new list 
                new_items[i] = new_items[i][:j] + str(int(items[i][j]) + x) + new_items[i][j + 1:]
                bool=False
                break
            j+=1
        i+=1

        #Breaking the loop once number anomaly is created in any of the room items 
        if(bool == False):
            break

    return Duty.add_anomaly("NUMBER ANOMALY",room, new_items)



main()
