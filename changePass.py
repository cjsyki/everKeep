#!/usr/bin/python
print "Content-Type: text/html\n"
print ""

import cgi, cgitb, os

cgitb.enable()

temp = open("users.csv", "r")
CSVusers = temp.readlines()
temp.close()

temp = open("current user.csv", "r")
users_logged_in = temp.readlines()
temp.close()

##Converts the csv to a list with sublists of each line
def convertCSV(file):
    d = []
    for element in file:
        d += [element.strip().split(",")]
    return d

##First half of the form (the title)
first_half = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Everkeep</title>
<link rel="icon" type="image/png" href="images/Everkeep without text.png">
<h1> Change your password </h1>
</head>
<body>
"""

##Second half of the form (the text fields and stuff)
second_half = """<form method="post">
<input type="password" name="current password" placeholder="Current password here">
<br><br>
<input type="password" name="new password" placeholder="New password here">
<br><br>
<input type="password" name="retype password" placeholder="Retype new password here">
<br><br>
<button type="submit">Change Password!</button>
</form>
<br>
<a href="welcome.py">Go back</a>!
</body>
</html>"""

##The page user sees after password changed
welcome = first_half + """<p>
Password changed! Click <a href="welcome.py">here</a> to go back
</p>
</body>
</html>
"""

##Checks if every character in a word is a letter/number 
##(returns True if there's a non-letter or number)
def contains_symbols(y):
    for char in y:
        if not(("a" <= char <= "z") or ("A" <= char <= "Z") or (48 <= ord(char) <= 57)):
            return True
    return False

def check_current_user():
    d = []
    for element in users_logged_in:
        d += [element.strip().split(",")]
    for element in d:
        if len(element) == 1:
            continue
        user, IP_Address = element[0], element[1]
        if os.environ["REMOTE_ADDR"] == IP_Address:
            return ["Yes", user]
    return ["No"]

##The main function
##REMEMBER: [ [user, pass, firstTIme], [user, pass, firstTime], [user, NEW_PASS, firstTime] ]
def change_password(current_user):
    d = cgi.FieldStorage()
    string = first_half
    users = convertCSV(CSVusers)
    if ("current password" not in d) or ("new password" not in d) or ("retype password" not in d):
        return string + "No password(s) was/were entered. Please try again." + second_half
    for user_pass_firstTime in users:#for each username/pass in CSV file
            password, username = user_pass_firstTime[1], user_pass_firstTime[0]
            if username == current_user:
                if password != d.getvalue("current password"):
                    string += "The current password you entered did not match. Please try again."
                    break
                if d.getvalue("new password") != d.getvalue("retype password"):
                    string += "The passwords you entered did not match. Please try again."
                    break
                if d.getvalue("new password") == password:
                    string += "The new password cannot match your current password. Please try again."
                    break
                if contains_symbols(d.getvalue("new password")) or contains_symbols(d.getvalue("retype password")):
                    string += "Password contained symbols (anything not a letter nor number is considered a symbol)"
                    break
    else:
        newCSV = ""
        for user_pass_firstTime in users:
            username, password, firstTime = user_pass_firstTime[0], user_pass_firstTime[1], user_pass_firstTime[2]
            if (current_user == username):
                user_pass_firstTime[1] = d.getvalue("retype password")
            newCSV += username + "," + user_pass_firstTime[1] + "," + firstTime + "\n"
        temp = open("users.csv", "w")
        temp.write(newCSV)
        temp.close()
        return welcome
    string += second_half
    return string
                        
def stuff():
    if check_current_user()[0] == "No":#len(current_user) == 0:
        return "You must <a href=\"main.py\">log in</a> first to continue."
    else:
        return change_password(check_current_user()[1])
    
print stuff()