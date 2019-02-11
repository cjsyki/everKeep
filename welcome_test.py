#!/usr/bin/python
print "Content-Type: text/html\n"

import cgi, cgitb, os

temp = open("current user.csv", "r")
users_logged_in = temp.readlines()
temp.close()

cgitb.enable()

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
    if check_current_user()[0] == "No":#len(current_user) == 0:
        return "You must <a href=\"main.py\">log in</a> first to continue."
    else:
        current_user = check_current_user()[1]
        user_directory = os.getcwd() + "/users/" + current_user
        list_contents = os.listdir(user_directory)
        newRow = 0
        string = "Current user: " + current_user + "<table>"
        for element in list_contents:#for each file
            if newRow == 0:
                string += "<tr>"
            string += """<td> <input type="text" name="note" value="%s" readonly>
        <br>
        <button type="submit" formaction="editNote.py">Edit Note</button><br>
        <br>
        <button type="submit" formaction="download.py">Download Note</button>
        <br>
        <br>
        <button type="submit" formaction="deleteNote.py" onclick="return confirm('Really delete this note? (NOTE: THIS IS IRREVERSIBLE)')">Delete Note</button>\n
        <br>
        <br>
        <button type="submit" formaction="beginNote.py">Send Note</button>""" %(element)
            newRow += 1
            if newRow == 3:
                string += "</tr>"
                newRow = 0
        string += """</form>
        <br>
        <a href="changePass.py">Change your password</a>
        <br>
        <a href=\"loggedOut.py\"> Log out </a>\n
        </html>"""
        return string
    
print """<!DOCTYPE html>
<html>"""
print stuff()