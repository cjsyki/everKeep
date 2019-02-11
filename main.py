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

##Replaces True with False in the firstTime section of the CSV file
##so that if uesr logs on for the first time, it changes from true to false
def firstTime_change(user):
    users = convertCSV(CSVusers)
    combined_file = ""
    for user_pass_firstTime in users:
        if user_pass_firstTime[2] == "True" and user_pass_firstTime[0] == user:
            user_pass_firstTime[2] = "False"
            #print user_pass_firstTime
        combined_file += ",".join(user_pass_firstTime) + "\n"
    temp = open("users.csv", "w")
    temp.write(combined_file)
    temp.close()
    #print combined_file
    
##First half of the form (the title)
first_half_login = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Everkeep</title>
<link rel="icon" type="image/png" href="images/Everkeep without text.png">
</head>
<link type="text/css" rel="stylesheet" href="css/main.css">

<h1> Welcome to <br><img src="images/Everkeep text -- WHITE.png"> </h1>
"""

##Second half of the form (the text fields and stuff)
second_half_login = """<body>
    <p>
    <span>Login</span><br><br><form method="post">
    <input type="text" name="username" placeholder="Username" required>
    <input type="password" name="password" placeholder="Password" required>
    <br><br>
    <button type="submit">Log in</button> <br> <br> <br>
    Don't have an account? Sign up <a href="signUp.py">here</a>
    </p>
    <p>
    <a href="credits.html">Credits</a>
    </a>
</form>
</body>
</html>"""

##The page user sees upon FIRST login
tutorial = first_half_login + """
<body> 
    <p>
        Hello, and welcome to Everkeep! Please read this tutorial <strong>carefully</strong> so that you can make the best of your experience using Everkeep! Note: You will <strong><em>NOT BE ABLE TO VIEW THIS PAGE ONCE YOU LEAVE. READ ITS CONTENTS CAREFULLY</strong></em>
    </p>
    <p>
        In case you didn't know, Everkeep is a notetaking and archiving service. You can <strong>create, edit, and even download your own notes</strong>!
    </p>
    <h3> Creating a note </h3>
    <p>
        To get started on your first note, click on the drop-down menu in the User Options page, and select "CREATE NEW NOTE". Once it's chosen, click "Edit Note". You will be then taken to the note editor page. There, you can choose what your note title and note body will say. After your done creating your note, press the "Save Note" button, and the note will then be saved onto your username.
    </p>
    <h3> Editing a note </h3>
    <p>
        On the drop-down menu on the User Options page, find the note you want to edit and press it. Once it's chosen, click "Edit Note". You will be taken to the note editor page, where you can edit the note all you want. Once you are satisfied, click on the "Save Note" button, and your note will override the previous note.
    </p>
    <h3> Downloading a note </h3>
    <p>
        On the User Options page, find the note you wish to download on the drop-down menu, and select it. Once chosen, press the "Download Note" button. You will then be taken to a new page. It will prompt you to click on a link to download the note. Once you press "yes", the note will be downloaded to your computer (note: <strong>it will be downloaded with a .txt extension</strong>).
    </p>
    More to come!!!
    <br>
    Note: In order to remain logged in, <strong> <em>YOUR IP ADDRESS MUST BE CONSTANT THROUGHOUT YOUR VISIT. CHANGING YOUR IP ADDRESS WILL RESULT IN YOU BEING FORCED OUT OF THE WEBSITE!!</strong></em>
    <br>
    <a href="welcome.py">I'm done with this tutorial, take me to the main page!</a>
</body>        
"""

##The page user sees AFTER FIRST login
welcome = first_half_login + """
<body>
    <p>
        Welcome back, %s. <a href="welcome.py">Click here</a> to view the notes you currently have.
    </p>
</body>
"""

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
def stuff():
    if check_current_user()[0] == "Yes":
        return welcome %(check_current_user()[1])
    d = cgi.FieldStorage()
    string = first_half_login
    users = convertCSV(CSVusers)
    for user_pass_firstTime in users:#for each username/pass in CSV file
        if user_pass_firstTime[0] == d.getvalue("username") and user_pass_firstTime[1] == d.getvalue("password"):# if the fields match
            #temp = open("current user.txt", "w")
            #temp.write(user_pass_firstTime[0])
            #temp.close()
            temp = open("current user.csv", "a")
            temp.write(user_pass_firstTime[0] + "," + os.environ["REMOTE_ADDR"] + "\n")
            temp.close()
            if user_pass_firstTime[2] == "True":
                            firstTime_change(user_pass_firstTime[0])
                            return tutorial
            return welcome %(user_pass_firstTime[0])
    if "username" in d or "password" in d:
        string += "User doesn't exist or username and/or password doesn't match"
    string += second_half_login
    return string

print stuff()