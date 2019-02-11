#!/usr/bin/python
print "Content-Type: text/html\n"
print ""

import cgi, cgitb, os
"""
temp = open("current user.txt", "r")

current_user = temp.read()

temp.close()
"""
temp = open("current user.csv", "r")
users_logged_in = temp.readlines()
temp.close()

cgitb.enable()

##Deletes the note (if its not a note, returns error)
def delete_note(current_user):
    queries = cgi.FieldStorage()
    if queries["note"].value == "create_note":
        return "You cannot delete this, as it is not a note. Click <a href=\"welcome.py\">here</a> to go back."
    note_title = str(queries.getvalue("note"))
    os.chdir(os.getcwd() + "/users/" + current_user)
    os.remove(note_title)
    return """Note deleted. Click <a href="welcome.py">here</a> to go back."""

def check_current_user():
    d = []
    for element in users_logged_in:
        d += [element.strip().split(",")]
    for element in d:
        user, IP_Address = element[0], element[1]
        if os.environ["REMOTE_ADDR"] == IP_Address:
            return ["Yes", user]
    return ["No"]
    
def stuff():   
    if check_current_user()[0] == "No":
        return "You must <a href=\"main.py\">log in</a> first to continue."
    return delete_note(check_current_user()[1])


print stuff()