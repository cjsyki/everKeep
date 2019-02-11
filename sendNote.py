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
%s has been sent to %s!
<br>
Click <a href="welcome.py">here</a> to go back
</html>
"""

def send_note(current_user):
    queries = cgi.FieldStorage()
    if "recipient" not in queries:
        return "No user inputted. Click <a href=\"javascript:history.back()\">here</a> to go back."
    note = queries.getvalue("note") + ".txt"
    recL = queries.getvalue("recipient").strip(",").split(",")
    path = os.getcwd() + "/users"
    os.chdir(path)
    L = os.listdir(path)
    for rec in recL[:]:
        if rec not in L:
            return "The user %s doesn't exist. Click <a href=\"javascript:history.back()\">here</a> to go back." %(rec)
        if rec == current_user:
            return "You cannot send a note to your own account. Click <a href=\"javascript:history.back()\">here</a> to go back." 
    for rec in recL:
        shutil.copy2( (path + "/" + current_user + "/" + note), (path + "/" + rec + "/" + note) )
    rec = ", ".join(recL)
    return "Note has been sent to the following: %s. Click <a href=\"welcome.py\">here</a> to go back" %(rec)
    

def stuff():   
    if check_current_user()[0] == "No":
        return "You must <a href=\"main.py\">log in</a> first to continue."
    return send_note(check_current_user()[1])


print stuff()