import oracledb

def create_connection():
    user = "your_username"
    password = "your_password"
    dsn = "your_dsn"
    try:
        connection = oracledb.connect(user=user, password=password, dsn=dsn)
        print("Connection successful.")
        return connection
    except oracledb.Error as e:
        print(f"Error connecting to Oracle Database: {e}")
        raise