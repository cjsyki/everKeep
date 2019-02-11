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
def create_note():
    form = """<!DOCTYPE html>
    <html>
    <script type="text/javascript" src="js/tinymce.min.js"></script>
<script type="text/javascript">
tinymce.init({
    selector: "textarea",
    plugins: [
        "advlist autolink lists link image charmap print preview anchor",
        "searchreplace visualblocks code fullscreen",
        "insertdatetime media table contextmenu paste"
    ],
    toolbar: "insertfile undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image"
});
</script>

<h1>NOTE: We <strong>HIGHLY</strong> suggest that if you want to add links and/or pictures to your note, use a short URL! Use <a href="http://goo.gl/" target="_blank">this link</a> to shorten your long URL!!</h1>
<form method="post" action="saveNote.py">
    <input type="text" name="name" size="90" maxlength="100" placeholder="Title goes here...">
    <textarea name="main note" style="width:100%"></textarea>
    <button type="submit" formaction="welcome.py" onclick="return confirm('Really leave without saving?')">Go back</button>
    <input type="submit" value="Save note">
</form>
</html>"""
    return form

def edit_note(note_name, current_user):
    os.chdir(os.getcwd() + "/users/" + current_user)
    temp = open(note_name, "r")
    note = temp.read()
    temp.close()
    form = """<!DOCTYPE html>
    <html>
    <script type="text/javascript" src="js/tinymce.min.js"></script>
<script type="text/javascript">
tinymce.init({
    selector: "textarea",
    plugins: [
        "advlist autolink lists link image charmap print preview anchor",
        "searchreplace visualblocks code fullscreen",
        "insertdatetime media table contextmenu paste"
    ],
    toolbar: "insertfile undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image"
});
</script>


<h1>NOTE: We <strong>HIGHLY</strong> suggest that if you want to add links and/or pictures to your note, use a short URL! Use <a href="http://goo.gl/" target="_blank">this link</a> to shorten your long URL!!</h1>
<form method="post" action="saveNote.py">
    <input type="text" name="name" size="90" maxlength="100" placeholder="Title goes here..." value=\"""" + note_name[:-4] + """\">
    <textarea name="main note" style="width:100%">""" + note + """</textarea>
    <button type="submit" formaction="welcome.py" onclick="return confirm('Really leave without saving?')">Go back</button>
    <input type="submit" value="Save note">
    <input type="hidden" name="old title" value=\"""" + note_name[:-4] + """\">
</form>
</html>"""
    return form
    
def note_check(current_user):
    query = cgi.FieldStorage()
    if query["note"].value == "create_note":
        return create_note()
    return edit_note(query["note"].value, current_user)

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
        return note_check(check_current_user()[1])
    
print stuff()