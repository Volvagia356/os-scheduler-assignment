import os

#This file contains miscellaneous UI functions

#Gets integer from user, with validation
def get_int(query,min_val=None,max_val=None,error_msg="Invalid input!"):
    while True:
        try:
            value=int(raw_input(query))
            if (min_val!=None and value<min_val) or (max_val!=None and value>max_val):
                raise IndexError
            return value
        except (ValueError,IndexError):
            print error_msg

#Clears screen, based on OS
def clear_screen():
    os.system('cls' if os.name=='nt' else 'clear')

#Displays menu with choices
def show_menu(choices,query="Selection: ",error_msg="Invalid selection!"):
    for i in range(len(choices)):
        print "{}) {}".format(i+1,choices[i])
    return get_int(query,1,len(choices),error_msg)-1