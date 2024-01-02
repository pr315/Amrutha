import sqlite3
from boxsdk import OAuth2, Client


def database_connection():
    conn = sqlite3.connect('credentials.db')
    return conn

def get_credentials():
    conn = database_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT client_id, access_token FROM boxcredentials ORDER BY id DESC LIMIT 1')
    result = cursor.fetchone()
    conn.close()
    return result 

def configure_box_auth():
    stored_credentials = get_credentials()
    if stored_credentials:
        stored_client_id, stored_access_token = stored_credentials
        oauth2 = OAuth2(
            client_id=stored_client_id,
            client_secret='',
            access_token=stored_access_token,
        )
        return Client(oauth2)
    else:
        return None
