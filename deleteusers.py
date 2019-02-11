#!/usr/bin/python
print "Content-Type: text/html\n"

import os, cgitb, shutil

cgitb.enable()

def delete():
    path = "/home/students/2017/clevinjames.syki/public_html/project/"
    usersL = os.listdir(path + "users")
    for user in usersL:
        if user == ".zip":
            continue
        if user == "master":
            continue
        shutil.rmtree(path + "users/" + user)
    temp = open("users.csv", "w")
    temp.write("master,cjsyki,True\n")
    temp.close()
    tempL = os.listdir(path + "temp")
    for temp_file in tempL:
        os.remove(path + "temp/" + temp_file)
    temp = open("current user.csv", "w")
temp.write("")
    temp.close()
    return "Users deleted"
        
print delete()