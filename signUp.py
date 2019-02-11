#!/usr/bin/python
print "Content-Type: text/html\n"
print ""

import cgi, cgitb, os

cgitb.enable()

temp = open("users.csv", "r")
CSVusers = temp.readlines()
temp.close()

temp = open("users.csv", "r")
store_current_Users = temp.read()
temp.close()

##Converts the CSV file into a list with sublists as usernames/passwords
def convertCSV(file):
    d = []
    for element in file:
        d += [element.strip().split(",")]
    return d

##Checks if every character in a word is a letter/number 
##(returns True if there's a non-letter or number)
def contains_symbols(y):
    for char in y:
        #print char
        if not(("a" <= char <= "z") or ("A" <= char <= "Z") or (48 <= ord(char) <= 57)):
            return True
    return False

success = """<!DOCTYPE html>
<html>
    <link rel="stylesheet" href="css/main.css">
    <head>
        <title>
            Everkeep
        </title>
        <h1>
            Your account was successfully created!!
        </h1>
        <link rel="icon" type="image/png" href="images/Everkeep without text.png">
    </head>
    <body>
        Click <a href="main.py">here</a> to login.
    </body>
</html>"""

first_half_signup = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Everkeep</title>
<link rel="icon" type="image/png" href="images/Everkeep without text.png">
</head>
<link type="text/css" rel="stylesheet" href="css/main.css">

<h1>Sign up</h1>

<body><br><br>"""

second_half_signup = """<form method="post">
            <p>
                Enter your desired username and password:
                <br><br>
                <input type="text" name="username" placeholder="Username" required>
                <input type="password" name="password" placeholder="Password" required>
                <input type="password" name="confirm password" placeholder="Confirm Password" required>
            </p>
            <p>
                <button type="submit">Sign up!</button>
            </p>
            Have an account? Login <a href="main.py">here</a>
        </form>
    </body>
</html>"""
##The main function
def stuff():
    d = cgi.FieldStorage()
    string = first_half_signup
    users = convertCSV(CSVusers)
    for user_pass in users:
        if "username" not in d or "password" not in d:#if theres nothing entered, end the for loop (when page first loads)
            string += "Note: The username cannot contain <strong>commas</strong>, and the password cannot contain <strong>anything not a letter or number (including spaces)</strong>"
            break
        elif user_pass[0] == d.getvalue("username"):#if a username matches one from the CSV file iteration, return error
            string += "That username is already taken"
            break
        elif contains_symbols(d.getvalue("password")):#if the password contains any symbols, return error
            string += "Password contained symbols (anything not a letter nor number is considered a symbol)"
            break
        elif "," in d.getvalue("username"):
            string += "Username contained a comma(s)."
            break
        elif d.getvalue("password") != d.getvalue("confirm password"):
            string += "The passwords did not match. (Passwords are CaSe SeNsItIvE)"
            break
    else:#if the username and password passes all the preliminary tests
        username = d.getvalue("username")
        password = d.getvalue("password")
        temp = open("users.csv", "w")
        new_user_appended = (store_current_Users + username + "," + password + "," + str(True) + "\n")
        temp.write(new_user_appended)
        temp.close()
        os.chdir("/home/students/2017/clevinjames.syki/public_html/proj/users")
        os.mkdir(username, 0777)
        return success
    string += second_half_signup
    return string

print stuff()