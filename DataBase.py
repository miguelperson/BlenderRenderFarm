import mysql.connector
#-m pip install mysql-connector-python
# Establish a connection to MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="7323",
    #database="renderdb" #comment when reate database and uncomment after
)

# Create a cursor object
mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE renderdb")
"""
mycursor.execute ("DROP DATABASE renderdb")
"""
"""
#----------------------------------------------------------------------------------1
#Create Database renderdb
mycursor.execute("CREATE DATABASE renderdb")

#----------------------------------------------------------------------------------2
#Create Teables
mycursor.execute("CREATE TABLE project (projectID INT AUTO_INCREMENT PRIMARY KEY, project_name VARCHAR(255), client VARCHAR(100), frames_total smallint UNSIGNED, start_frame smallint UNSIGNED, end_frame smallint UNSIGNED)")
mycursor.execute("CREATE TABLE workers (worker VARCHAR(100), available TINYINT(1), projectID INT, FOREIGN KEY (projectID) REFERENCES project(projectID))") #TINYINT(1)=true
mycursor.execute("CREATE TABLE render (frame_number smallint UNSIGNED, projectID INT, FOREIGN KEY (projectID) REFERENCES project(projectID))")
#----------------------------------------------------------------------------------
"""
#Hello everybody my name is Markiplier
"""
mycursor.execute("SHOW TABLES")s

for x in mycursor:
  print(x)

mycursor.execute("DESCRIBE render")
result = mycursor.fetchall()
for row in result:
    print(row)

"""
"""
mycursor.execute("SELECT * FROM project")

# Fetch all rows from the cursor
result = mycursor.fetchall()

# Print the fetched data
for row in result:
    print(row)


mydb.commit()
mydb.close()
"""