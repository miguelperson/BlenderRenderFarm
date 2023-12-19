import mysql.connector
#-m pip install mysql-connector-python
# Establish a connection to MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="7323",
    database="renderdb" #comment when reate database and uncomment after
)

# Create a cursor object
mycursor = mydb.cursor()
#----------------------------------------------------------------------------------1
# Create Database renderdb
#mycursor.execute("CREATE DATABASE renderdb")

#----------------------------------------------------------------------------------2
#Create Teables
#mycursor.execute("CREATE TABLE project (projectID INT AUTO_INCREMENT PRIMARY KEY, project_name VARCHAR(255), client VARCHAR(100), frames_total smallint UNSIGNED, start_frame smallint UNSIGNED, end_frame smallint UNSIGNED)")
#----------------------------------------------------------------------------------
mycursor.execute("DESCRIBE project")
result = mycursor.fetchall()
for row in result:
    print(row)

mycursor.execute("SHOW TABLES")
