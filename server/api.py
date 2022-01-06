from flask import Flask, request
from flask_cors import CORS

from TeamTssWebAppProject.database.repository import get_connection, get_email_and_password, connect, \
    create_user

app = Flask("Login|Signup")
CORS(app)

DB_FILE = '../database/users.db'

# Create user/Sign up
@app.route('/api/v1/users', methods=["POST"])
def users():
    user_details = request.json
    username = user_details.get("username", None)
    if username is "":
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

# Sign in
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
            return '', 204
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


if __name__ == "__main__":
    app.run(port=3002, debug=True)
