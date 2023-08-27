import mysql.connector

cnx = mysql.connector.connect(user="root",
                              password="admin",
                              host="localhost",
                              database="garupay")
cur = cnx.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS state_manager ("
            "user_id VARCHAR(30), "
            "chat_id VARCHAR(100),"
            "state INTEGER,"
            "UNIQUE (user_id, chat_id)"
            ")")


cur.execute("CREATE TABLE IF NOT EXISTS friends ("
            "name VARCHAR(50), "
            "username VARCHAR(50), "
            "chat_id VARCHAR(100),"
            "UNIQUE (name, username, chat_id)"
            ")")

cur.execute("CREATE TABLE IF NOT EXISTS transactions ("
            "from_user_id VARCHAR(20),"
            "to_user_id VARCHAR(20),"
            "chat_id VARCHAR(100),"
            "amount FLOAT,"
            "date_updated VARCHAR(20),"
            "has_paid INTEGER"
            ")")

cur.execute("CREATE TABLE IF NOT EXISTS users ("
            "username VARCHAR(50), "
            "user_id VARCHAR(50), "
            "email VARCHAR(50),"
            "UNIQUE (user_id) "
            ")")
