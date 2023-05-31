import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, apology

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure python standard library to use SQLite database
con = SQL('sqlite:///mymo.db')

# Application's Routes
@app.route("/", methods=["GET", "POST"])
@login_required
def index():

    #gets executed when the user submit the note
    if request.method == "POST":

            insert_vid = request.form.get("vid")
            view_note = request.form.get("view_note")
            insert_note = request.form.get("note")
            insert_pic = request.form.get("picture")
            view_pic = request.form.get("view_pics")
            view_vid = request.form.get("view_vids")
            if view_note != None:
                # getting the note from the database
                user_id = session["user_id"]
                notes = con.execute("SELECT * FROM notes WHERE user_id = ?", user_id)
                return render_template("index.html",msg = "view_note",notes=notes)
            elif insert_note != None:
                note = request.form.get("note")

                #Ensures that the users enterd a note.
                if note == None:
                    return apology("must provide Note")

                #Ensures the users enterd bellow the max no. of char.
                if(len(note) > 4294967295):
                    return apology("note is far too long")

                #getting the registerd user id
                user_id = session["user_id"]

                #insert the note into the database
                con.execute("INSERT INTO notes(user_id, text) VALUES(?, ?)", user_id, note)
                # return render_template("index.html")
                notes = con.execute("SELECT * FROM notes WHERE user_id = ?", user_id)
                return render_template("index.html",msg = "view_note",notes=notes)
            elif view_pic != None:
                user_id = session["user_id"]
                pics = con.execute("SELECT * FROM pics WHERE user_id = ?", user_id)
                return render_template("index.html",msg = "view_pics",pics=pics)


            elif insert_pic != None:
                if(len(insert_pic) > 4294967295):
                    return apology("The Link Is Too long")

                user_id = session["user_id"]
                con.execute("INSERT INTO pics(user_id,link) VALUES(?,?)",user_id,insert_pic)
                pics = con.execute("SELECT * FROM pics WHERE user_id = ?", user_id)
                return render_template("index.html",msg = "view_pics",pics=pics)


            elif insert_vid != None:
                if(len(insert_vid) > 4294967295):
                    return apology("The Link Is Too long")

                user_id = session["user_id"]
                insert_vid = insert_vid.replace("watch?v=","embed/")
                con.execute("INSERT INTO vids(user_id,link) VALUES(?,?)",user_id,insert_vid)
                vids = con.execute("SELECT * FROM vids WHERE user_id = ?", user_id)
                return render_template("index.html",msg = "view_vids",vids=vids)
            elif view_vid != None:
                user_id = session["user_id"]
                vids = con.execute("SELECT * FROM vids WHERE user_id = ?", user_id)
                return render_template("index.html",msg = "view_vids",vids=vids)


    else:
        vid = request.args.get("insert_vids")
        pics = request.args.get("insert_pics")
        note = request.args.get("insert_note")
        if note != None:
            return render_template("index.html",msg="insert_note")
        elif pics != None:
            return render_template("index.html",msg="insert_pics")
        elif vid != None:
            return render_template("index.html",msg="insert_vid")

        count = con.execute("SELECT COUNT(*) FROM notes WHERE user_id = ?", session["user_id"])
        notes_counter = count[0]["COUNT(*)"]
        name = con.execute("SELECT username FROM users WHERE id = ?",session["user_id"])
        name = name[0]["username"]

        count = con.execute("SELECT COUNT(*) FROM pics WHERE user_id = ?", session["user_id"])
        pics_counter = count[0]["COUNT(*)"]

        count = con.execute("SELECT COUNT(*) FROM vids WHERE user_id = ?", session["user_id"])
        vids_counter = count[0]["COUNT(*)"]


        return render_template("index.html",notes_counter = notes_counter,name=name,msg="mainPage", pics_counter=pics_counter, vids_counter=vids_counter)




@app.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    #gets executed when we want to modify any note
    if request.method == "POST":
        Note_id = request.form.get("selected")
        con.execute("DELETE FROM notes WHERE id = ?", Note_id)
        user_id = session["user_id"]
        notes = con.execute("SELECT * FROM notes WHERE user_id = ?", user_id)
        return render_template("index.html",msg = "view_note",notes=notes)

    else:
        return apology("get zarta")

@app.route("/remove_pic", methods=["GET", "POST"])
@login_required
def remove_pic():
    if request.method == "POST":
        pic_id = request.form.get("selected")
        con.execute("DELETE FROM pics WHERE id = ?", pic_id)
        user_id = session["user_id"]
        pics = con.execute("SELECT * FROM pics WHERE user_id = ?", user_id)
        return render_template("index.html",msg = "view_pics",pics=pics)

@app.route("/remove_vids", methods=["GET", "POST"])
@login_required
def remove_vids():
    if request.method == "POST":
        vid_id = request.form.get("selected")
        con.execute("DELETE FROM vids WHERE id = ?", vid_id)
        user_id = session["user_id"]
        vids = con.execute("SELECT * FROM vids WHERE user_id = ?", user_id)
        return render_template("index.html",msg = "view_vids",vids=vids)



@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        if not request.form.get("username"):
            return apology("Please provide username!")
        #Ensure that the user name does'nt already exists.
        elif len(con.execute("SELECT * FROM users WHERE username =?",request.form.get("username") )):
            return apology("Name already exist")
        else:
            username = request.form.get("username")

        #Ensure password was submited
        if not request.form.get("password"):
            return apology("Please Provide Password!")
        else:
            password = request.form.get("password")

        #Ensure confirm was submited
        if not request.form.get("confirm"):
            return apology("Please re-write the password!")

        #Ensure password == confirm
        else:
            confirm = request.form.get("confirm")
            if password != confirm:
                return apology("passwords don't match!")
            else:
                id_primkey = con.execute("INSERT INTO users (username,hash) VALUES(?,?)",username, generate_password_hash(password) )
                # Remember which user has Reigsterd
                session["user_id"] = id_primkey

                #Redirect the user to home page
                return redirect("/login")



@app.route("/login", methods=["GET", "POST"])
def login():
    """ Log user in """

    # Forget any user_id
    session.clear()

    # gets executed when the user submit the form
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # Query database for username
        ''' اسم الداتا بيز الي انت حاطه غبي YA'''
        rows = con.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # Gets executed when the user reche route via GET(as by clicking a link or via redirect)
    return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")










def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return render_template("apology.html")

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)