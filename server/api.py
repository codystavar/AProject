from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS, cross_origin
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
from flask_socketio import SocketIO, join_room, leave_room
import datetime
from TeamTssWebAppProject.database.repository import get_connection, get_email_and_password, connect, \
    create_user
from TeamTssWebAppProject.database.eventrepo import create_event

app = Flask("ProjectAppTss", template_folder='../client/', static_folder='../client/static/') 
# render_template attempts to find by default a folder named 'templates
# by redirecting the template_folder path, we can use the client folder instead
# also added a static folder for the js files
CORS(app)
socketio = SocketIO(app)


app.config["JWT_SECRET_KEY"] = "teamtsskey"  # Secret key has to be a lot more advanced and never an easy to guess word/string
jwt = JWTManager(app)

useremail = 0 # global variable used to remember the email of one user
currentuser = 0 # name of the user that "logged in", need to implement flask login or jwt to have a proper login system

DB_FILE = '../database/users.db'
redirectfile = '../client/eventCreatePage.html'

#Create user/Sign up
@app.route('/api/v1/users', methods=["POST"])
def users():
    user_details = request.json
    username = user_details.get("username", None)
    if username is None:
        error = {
            "error": "--Failed to create user. Username is none."
        }
        return error, 400
    try:
        conn = connect(DB_FILE)
        details = {
            "username": user_details.get("username", None),
            "first_name": user_details.get("firstName", None),
            "last_name": user_details.get("secondName", None),
            "email": user_details.get("email", None),
            "password": user_details.get("password", None)
        }
        create_user(conn, details)
        conn.close()
        return '', 200
    except Exception as e:
        error = {
            'error': {e}
        }
        return error, 500

#Sign in
@app.route('/api/v1/sign-in', methods=["POST"])
def sign_in():
    body = request.json
    email = body.get("email", None)
    password = body.get("password", None)
    
    if email is None:
        error = {
            "error": "--Please provide an email."
        }
        return error, 400
    

    if password is None:
        error = {
            "error": "--Please provide a password."
        }
        return error, 400

    try:
        conn = get_connection(DB_FILE)
        user = get_email_and_password(conn, email)
        if user and user["password"] == password:
            access_token = create_access_token(identity=email, fresh=datetime.timedelta(minutes=60))
            global useremail # sa adauge in varibila globala
            useremail = email
            print("User (email) logged in is:", email, "with access key:", access_token) # sa confirmam ca utilizatorul logat este cel corect
            return jsonify(access_token=access_token), 204
            
                     
        else:
            error = {
                "error": "--Failed to sign-in. Email or password are invalid."
            }
            return error, 401
    except Exception as e:
        error = {
            "error": f"--Failed to sign-in. {e}"
        }
        return error, 500

# Create events
@app.route('/api/v1/cevents', methods=["POST"])
def events():
    event_details = request.json
    title = event_details.get("title", None)
    if title == "":
        error = {
            "error": "--Failed to create event. Title is none."
        }
        return error, 400
    try:
        conn = connect(DB_FILE)
        eventuser = currentuser
        details = {
            "title": event_details.get("title", None),
            "user": currentuser,
            "startdate": event_details.get("startdate", None),
            "enddate": event_details.get("enddate", None)
        }
        create_event(conn, details)
        conn.close()
        return '', 200
    except Exception as e:
        error = {
            'error': {e}
        }
        return error, 500

# Get username from email
def getusername():
    conn = get_connection(DB_FILE)
    cur = conn.cursor()
    cur.execute(f"SELECT first_name, last_name FROM users WHERE email = '{useremail}'")
    global currentuser
    tup = cur.fetchone()
    currentuser = (f"{tup[0]} {tup[1]}")

# index
@app.route('/')
def indexpage():
    return render_template("index.html")
# signup
@app.route('/signup')
def signup():
    return render_template("signup.html")

# myprofile template
@app.route('/myprofile')
def my_profile():
    getusername()
    return render_template("myprofile.html", myprofilename = currentuser)

# events template
@app.route('/events')
def eventpage():
    return render_template("eventCreatePage.html", myprofilename = currentuser)

# chat login
@app.route('/chatlogin')
@cross_origin()
def home():
    return render_template("chatlogin.html")

# chat
@app.route('/chat')
@cross_origin()
def chat():
    username = request.args.get('username')
    room = request.args.get('room')

    if username and room:
        return render_template('chat.html', username=username, room=room)
    else:
        return redirect(url_for('home'))

# chat (send message)
@socketio.on('send_message')
def handle_send_message_event(data):
    app.logger.info("{} has sent message to the room {}: {}".format(data['username'],
                                                                    data['room'],
                                                                    data['message']))
    socketio.emit('receive_message', data, room=data['room'])

# chat (join room)
@socketio.on('join_room')
def handle_join_room_event(data):
    app.logger.info("{} has joined the room {}".format(data['username'], data['room']))
    join_room(data['room'])
    socketio.emit('join_room_announcement', data, room=data['room'])

# chat (leave room)
@socketio.on('leave_room')
def handle_leave_room_event(data):
    app.logger.info("{} has left the room {}".format(data['username'], data['room']))
    leave_room(data['room'])
    socketio.emit('leave_room_announcement', data, room=data['room'])


if __name__ == '__main__':
    app.run(port=3002, debug=True)
