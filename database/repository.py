import sqlite3

dbfile = ("users.db")

def connect(db_filename):
    try:
        conn = sqlite3.connect(db_filename)
        print("..SQLite connection established...")
    except ValueError as ve:
        print(f"--Invalid values provided. Error: {ve}.")
        raise ve
    except Exception as e:
        print(f"--Failed to connect to {db_filename}. Error: {e}.")
        raise e
    return conn

def get_connection(dbfile):
    try:
        conn = sqlite3.connect(dbfile)
        return conn
    except Exception as e:
        raise Exception(f"--Failed to connect to {dbfile}. Error: {e}.")


def get_email_and_password(conn, email=None):
    query = f"""select email, password from users where email='{email}'"""
    try:
        cursor = conn.cursor()
        user = list(cursor.execute(query))
        if len(user):
            # user = user[0]
            user = {
                "email": user[0][0],
                "password": user[0][1]
            }
        return user
    except Exception as e:
        raise Exception(f"--Failed to extract email and password for user = {email}. Error: {e}.")


def create_user(conn, user_details):
    value_keys = ",".join(user_details.keys())
    values = [user_details[k] for k, v in user_details.items()]
    n_values = ",".join(["?"] * len(values))
    query = f"insert into users ({value_keys}) values ({n_values})"
    try:
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()
        print("..User created successfully...")
    except sqlite3.IntegrityError as ie:
        print(f"--Failed to create user due to constraints not met. Error: {ie}.")
        raise ValueError(ie)
    except Exception as e:
        print(f"--Failed to insert new users. Error: {e}.")
        raise e
