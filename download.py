#!/usr/bin/python
print "Content-Type: text/html\n"
print ""

import cgi, cgitb, os
"""
temp = open("current user.txt", "r")

current_user = temp.read()

temp.close()

cgitb.enable()
"""
temp = open("current user.csv", "r")
users_logged_in = temp.readlines()
temp.close()

cgitb.enable()
##Either returns an error if user selectes "CREATE NEW NOTE", or provides a download link 
##allowing user to download the text file chosen at the welcome page
def print_note(current_user):
    queries = cgi.FieldStorage()
    if queries["note"].value == "create_note":
        return "You cannot download this, as it is not a note. Click <a href=\"welcome.py\">here</a> to go back."
    note_title = str(queries.getvalue("note"))
    os.chdir(os.getcwd() + "/users/" + current_user)
    temp = open(note_title, "r")
    note_body = str(temp.read())
    temp.close()
    os.chdir("/home/students/2017/clevinjames.syki/public_html/proj/temp")
    note = open(note_title, "w")
    note.write(note_body)
    note.close()
    form = """Click <a href="temp/""" + note_title + """" download>here</a> to download the note.
    <a href="welcome.py"> Go back</a> to the home page"""
    return form

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
    return print_note(check_current_user()[1])


print stuff()