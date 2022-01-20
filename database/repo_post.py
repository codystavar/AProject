import sqlite3

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
#create post
def create_post(conn, post_details):
    value_keys = ",".join(post_details.keys())
    values = [post_details[k] for k, v in post_details.items()]
    n_values = ",".join(["?"] * len(values))
    query = f"insert into post ({value_keys}) values ({n_values})"
    try:
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()
        print("..Post created successfully...")
    except sqlite3.IntegrityError as ie:
        print(f"--Failed to create post due to constraints not met. Error: {ie}.")
        raise ValueError(ie)
    except Exception as e:
        print(f"--Failed to insert new post. Error: {e}.")
        raise e

#get posts
def get_posts(conn):
    cursor = conn.cursor()
    cursor.execute('select name, post from post')
    posts = cursor.fetchall()
    return posts