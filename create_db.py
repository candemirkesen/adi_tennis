import mysql.connector
import pandas as pd

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="tennis_scores"
)

my_cursor = mydb.cursor()

# my_cursor.execute("CREATE DATABASE tennis_scores")

# my_cursor.execute("SHOW DATABASES")

# my_cursor.execute("CREATE TABLE scores (id INT AUTO_INCREMENT PRIMARY KEY, player VARCHAR(255), score INT)")

# my_cursor.execute("SELECT * FROM scores")

# my_cursor.execute("DROP TABLE scores")

# my_cursor.execute("CREATE TABLE scores (id INT AUTO_INCREMENT PRIMARY KEY, player VARCHAR(255), score INT)")


# my_cursor.execute("SHOW TABLES")
# for x in my_cursor:
#     print(x)

# df = pd.read_csv('scores.csv')

# for i in range(len(df)):
#     player_name = df.Player[i]
#     player_score = df.Score[i]
#     sql_command = "INSERT INTO scores (player, score) VALUES('" + player_name + "'," +  str(player_score) + ")"
#     my_cursor.execute(sql_command)

# my_cursor.execute("COMMIT")


# my_cursor.execute("INSERT INTO scores (player, score) VALUES('can', 800)")
# my_cursor.execute("INSERT INTO scores (player, score) VALUES('uraz', 800)")

my_cursor.execute("SELECT * FROM scores WHERE player = 'Can'")
# my_cursor.execute("SELECT * FROM scores WHERE player = 'Burak'")



for x in my_cursor:
    print(x)

my_cursor.execute("SELECT * FROM scores WHERE player like 'B%'")
for x in my_cursor:
    print(x)


