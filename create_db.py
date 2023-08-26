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


cur.execute("CREATE TABLE IF NOT EXISTS transactions ("
            "from_user_id VARCHAR(30), "
            "from_username VARCHAR(50), "
            "to_user_id VARCHAR(30), "
            "to_username VARCHAR(50), "
            "chat_id VARCHAR(100),"
            "amount FLOAT,"
            "date_updated VARCHAR(20),"
            "has_paid INTEGER"
            ")")
