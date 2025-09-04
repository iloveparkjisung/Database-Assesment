import easygui as eg
#this is our dictionary where the information the user wants to know, remove, add, find are in.
catalogue = {
    "Stoneling" : { #dictionary inside a dictionary to store more values so we could put in different keys.
        "Strength" : 7,
        "Speed" : 1,
        "Stealth" : 25,
        "Cunning" : 15
    } , 
    "Vexcream" : {
        "Strength" : 1,
        "Speed" : 6,
        "Stealth" : 21,
        "Cunning" : 19
    } , 
    "Dawnmirage" : {
        "Strength" : 5,
        "Speed" : 15,
        "Stealth" : 18,
        "Cunning" : 22
    } ,
    "Blazegolem" : {
        "Strength" : 15,
        "Speed" : 20,
        "Stealth" : 23,
        "Cunning" : 6
    } ,
    "Websnake" : {
        "Strength" : 7,
        "Speed" : 15,
        "Stealth" : 10,
        "Cunning" : 5
    } , 
    "Moldvine" : {
        "Strength" : 21,
        "Speed" : 18,
        "Stealth" : 14,
        "Cunning" : 5
    } , 
    "Vortexwing" : {
        "Strength" : 19,
        "Speed" : 13,
        "Stealth" : 19,
        "Cunning" : 2
    } , 
    "Rotthing" : {
        "Strength" : 16,
        "Speed" : 7,
        "Stealth" : 4,
        "Cunning" : 12
    } , 
    "Froststep" : {
        "Strength" : 14,
        "Speed" : 14,
        "Stealth" : 17,
        "Cunning" : 4
    } , 
    "Wispghoul" : {
        "Strength" : 17,
        "Speed" : 19,
        "Stealth" : 3,
        "Cunning" : 2
    } 
}

def view_monsters(): #this shows us what is currently inside the dictionary
    catalogue_text = "Existing NEOZONE monsters:"
    for monster_name, stat in catalogue.items(): #this would grab the information (name and stats)
        catalogue_text += f"\n\n{monster_name}'s Stats:\n" #while this would print it
        for stat, stat_number in stat.items(): #this would print the stats
            catalogue_text += f"{stat}: {stat_number}\n"
    eg.msgbox(catalogue_text, title="catalogue")

def make_monster():#this function helps the user search up their desired monster
    eg.msgbox("Create new NEOZONE monsters and customize their stats!", "Create Monster")
    name = eg.enterbox("Enter the name of the NEOZONE monster: ", title = "Monster Name").capitalize()
    if not name:
        eg.msgbox("Monster name cannot be blank!! Returning to the Main Menu", "ERROR!")
        return
    if name in catalogue: #we use these two so that the suer cannot enter an invalid monster!
        eg.msgbox(f"A NEOZONE monster named '{name}' already exists in the catalogue!\nMonster creation canceled returning to menu!", "ERROR!")
        return
    items = {} # we use an empty dictionary so we can put new things into it
    for stat_name in ["Strength", "Speed", "Stealth", "Cunning"]:
        while True:
            stat_num = eg.enterbox(f"Choose a value for {stat_name}! (Please enter a number between 1 - 25) : ", title = f"Set {stat_name}")
            if stat_num is None:
                eg.msgbox("User entered a blank space. Monster creation canceled.\nReturning to the menu", "ERROR")
                return
            try:
                stat_num = int(stat_num)
                if stat_num > 25:
                    eg.msgbox(f"The value for {stat_name} cannot exceed 25.\nCanceling monster creation, returning to Main Menu.", "ERROR")
                    return
                elif stat_num <= 1:
                    eg.msgbox(f"The value for {stat_name} cannot exceed 25.\nCanceling monster creation, returning to Main Menu.", "ERROR")
                    return  
                items[stat_name] = stat_num
                break
            except ValueError:
                eg.msgbox("Invalid stat number. Please enter a numeric value", "ERROR")

    catalogue [name] = items 
    eg.msgbox(f"New NEOZONE monster '{name} added.", "SUCCESS")

def main_catalogue(): #this will be our main interface where we can navigate and locate what we want to see
    while True:
        choice = eg.buttonbox(
            "=== NEOZONE: THE Monster Game Catalogue ===\nWhat would you like to do today?\n\nChoose one of the options to navigate!",#the welcoming message the user is receiving
            title = "THE Burger Shop",
            choices = ["Look at all the monsters >-<!", "Search for a MONSTER?! rawr :3", "Create the Monster of your dreams :O", "Delete a Monster :<", "Exit"]
        )
        if choice == 'Look at all the monsters >-<!': #if the user chooses one of the options it will do the fuctions which has specific tasks assigned using the def function.
            view_monsters()
        elif choice == 'Search for a MONSTER?! rawr :3':
            search_catalogue()
        elif choice == 'Create the Monster of your dreams :O':
            make_monster()
        elif choice == 'Delete a Monster :<':
            delete_monster()
        elif choice == 'Exit':
            eg.msgbox("Thank you for using NEOZONE: THE Monster Game Catalogue") 
            break #using break quits the code

def search_catalogue(): #in this def functions the user can search up certain monsters and see their stats
    monster = eg.choicebox("View NEOZONE monster", "View monster", list(catalogue.keys())) 
    if monster:
        monster_txt = f"{monster}'s Stats:\n"
        for stats, stats_number in catalogue[monster].items():#thsi prints the stats of th emonster the monster the user asked for
            monster_txt += f"{stats} : {stats_number}\n"
        eg.msgbox(monster_txt, title = f"NEOZONE monster details : {monster}")

def delete_monster():
    name = eg.choicebox("Choose the NEOZONE monster you would want to delete: ", "Delete a NEOZONE monster" ,list(catalogue.keys()))
    if name in catalogue:
        del catalogue[name]
        eg.msgbox(f"NEOZONE monster '{name}' was deleted.", "SUCCESS")

main_catalogue()