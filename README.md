# YOUR PROJECT TITLE


#### Description:
This project aims to make online memo, and aim to make memo's experience more fun

#### files used
- templates : our front end
  - used to store all html files
    - index.html
        - the main part of our project, it contains the welcome message with current statistics about the number of notes,images and videos that are also updated automatically, it also contains on the left region of the page the possible options that can be done like inserting a note, image or a video or viewing the saved notes or images or videos in the page
    - apology.html
        - contains the error handling message, some sort of errors like not typing the name or not typing the password or not typing the confirmatin of the password
          or typing all of them but the passwords don't match
    - login.html
        - enable the user to inter his own site,it requires that the user has alreeady registered with a valid name that didn't exist before registering, the page also handles some errors like not typing the username , password or typing it wrong. it also shows which typeof error the user has made with a messsage so that he knows what wrong did he do
          and if no errors occured then the user will be logged in to his main page
    - register.html
        - displays a form to the user, so he can register in our application, the page prompts the user for his name , the name must be inserted and it must be a new name that isn't already taken by another user, then it prompts him for the passsword and to confirm the password, the registration will be completed if no errors occured


- application.py: our backend
    - index(): the brain of our code, it enable the user to save notes, pictures and videos and make sure thay are entered with out any error
    - edit(): enable us to keep track of the user modifications to his notes by deleting them
    - remove_pic(): enable us to keep track of the user modifications to his pictures by deleting them
    - remove_vids():enable us to keep track of the user modifications to his videos by deleting them
    - register(): handles new users registering by asking the user to submit thier name, password and confirmation
    - login(): handles old users logging in
    - logout(): handles users logging out
    - errorhandler(e): gets called when there is a bug in the code


- helpers.py:
  -apology: contains the error handling function that displays a messege for the user contaning thair error it needs one argement
    - example of apology code
    '''
    def apology(message):
    return render_template("apology.html", msg = message)
    '''

-mymo.db: our database
    - users: to store users name and passwords
    - notes: to store users id,  note id and the actual note
    - pics: to store usersid, user's pics, and the acutual video
    - vids: to store userid,  usersvideos and the actual video

-requierments.txt: includes a list of required libraries for our application.


-static: is a directory of static files, like style.css and images used in our application

design choices:
we made all button the user can use on the left so it will be easier for him to access all content of the page, we also designed the logo of the web aplicationfrom scratch


