#!/usr/bin/python
print "Content-Type: text/html\n"
print ""

import cgi, cgitb, os, shutil #shutil --> high level file functions, copying a file and moving it

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

html = """<!DOCTYPE html>
<html>
Who do you want to send %s to?
<br>
Note: To send to multiple users, enter a username FOLLOWED BY A COMMA (NO SPACES after the comma)
<form method="post">
    <input type="text" name="recipient" placeholder="Enter a username">
    <button type="submit" formaction="sendNote.py" onclick="return confirm('Are you sure you want to send the note?)">Send Note</button>
    <input type="hidden" name="note" value="%s">
</form>
<br>
Click <a href="welcome.py">here</a> to go back
</html>
"""

def begin_note(current_user):
    queries = cgi.FieldStorage()
    note = str(queries.getvalue("note"))
    if note == "create_note":
        return "This is not a note. Click <a href=\"welcome.py\">here</a> to go back."
    note = str(note[:-4])#exclude the .txt extension
    return html %(note, note)    
    

def stuff():   
    if check_current_user()[0] == "No":
        return "You must <a href=\"main.py\">log in</a> first to continue."
    return begin_note(check_current_user()[1])


print stuff()