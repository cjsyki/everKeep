#!/usr/bin/python
print "Content-Type: text/html\n"
print ""

import os, cgitb

"""
current_user = open("current user.txt", "w")

current_user.write("")

current_user.close()
"""
cgitb.enable()

temp = open("current user.csv", "r")
users_logged_in = temp.readlines()
temp.close()

User_IP_Address = os.environ["REMOTE_ADDR"]

##Finds the current users ip address, and removes ALL CASES of it int hte csv file  
def check_current_user():
    d = []
    for element in users_logged_in:
        d += [element]
    #print d
    for element in d[:]:
        if User_IP_Address in element:
            d.remove(element)
    #print d
    new_current_users = "".join(d)
    temp = open("current user.csv", "w")
    temp.write(new_current_users)
    temp.close()

check_current_user()

print "You have logged off. Click <a href=\"main.py\">here</a> to log in again."