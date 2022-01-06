import sqlite3

dbfile = "users.db"

def create_event(conn, event_details):
    value_keys = ",".join(event_details.keys())
    values = [event_details[k] for k, v in event_details.items()]
    n_values = ",".join(["?"] * len(values))
    query = f"insert into events ({value_keys}) values ({n_values})"
    try:
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()
        print("..Event created successfully...")
    except sqlite3.IntegrityError as ie:
        print(f"--Failed to create event due to constraints not met. Error: {ie}.")
        raise ValueError(ie)
    except Exception as e:
        print(f"--Failed to insert new event. Error: {e}.")
        raise e
