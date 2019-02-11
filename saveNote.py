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

def save_note(current_user):
    queries = cgi.FieldStorage()
    try:
        note_title = queries["name"].value
    except:
        return "No title was entered. Click <a href=\"javascript:history.back()\">here</a> to go back."
    if ("/" in note_title) or ("\\" in note_title) or (":" in note_title) or ("<" in note_title) or (">" in note_title) or ("\"" in note_title) or ("|" in note_title) or ("?" in note_title):
        return "The title cannot contain any of the following: / \ : \" < > | ?. Click <a href=\"javascript:history.back()\">here</a> to go back."
    path = os.getcwd() + "/users/" + current_user
    if (note_title + ".txt" in os.listdir(path)):
        try:
            if queries["old title"].value == note_title:
                pass
            else:
                return "You cannot name your note title " + note_title + """. This is because a note already exists with that title. Click <a href="javascript:history.back()">here</a> to go back."""
        except:
            return "You cannot name your note title " + note_title + """. This is because a note already exists with that title. Click <a href="javascript:history.back()">here</a> to go back."""
    os.chdir("/home/students/2017/clevinjames.syki/public_html/proj/users/" + current_user)
    if "old title" in queries:
        os.remove(queries.getvalue("old title") + ".txt")
    note_title += ".txt"
    note_body = queries["main note"].value
    note = open(note_title, "w")
    note.write(note_body)
    note.close()
    return "Note saved! Click <a href=\"welcome.py\">here</a> to go back"


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
        return save_note(check_current_user()[1])
    
print stuff()