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
    cursor.execute('select name, post, like, dislike, ID_post from post')
    posts = cursor.fetchall()
    return posts
#like
def like(conn, id):
    cursor = conn.cursor()
    cursor.execute(f'select like from post where ID_post = {id}')
    likes = cursor.fetchone()
    like = likes[0]+1
    query = f"update post set like = {like} where ID_post = {id}"
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        print("..Post successfully liked...")
        return
    except sqlite3.IntegrityError as ie:
        print(f"--Failed to like post due to constraints not met. Error: {ie}.")
        raise ValueError(ie)
    except Exception as e:
        print(f"--Failed to like. Error: {e}.")
        raise e
#like
def dislike(conn, id):
    cursor = conn.cursor()
    cursor.execute(f'select dislike from post where ID_post = {id}')
    dislikes = cursor.fetchone()
    dislike = dislikes[0]+1
    query = f"update post set dislike = {dislike} where ID_post = {id}"
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        print("..Post successfully disliked...")
        return
    except sqlite3.IntegrityError as ie:
        print(f"--Failed to dislike post due to constraints not met. Error: {ie}.")
        raise ValueError(ie)
    except Exception as e:
        print(f"--Failed to dislike. Error: {e}.")
        raise e