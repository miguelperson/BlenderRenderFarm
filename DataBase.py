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


"""
#----------------------------------------------------------------------------------1
#Drop Database renderdb
mycursor.execute ("DROP DATABASE renderdb")
#Create Database renderdb
mycursor.execute("CREATE DATABASE renderdb")

#----------------------------------------------------------------------------------2

mysql
# Create Tables - Mikaela :) :)
"""

#mycursor.execute("CREATE TABLE project (projectID INT AUTO_INCREMENT PRIMARY KEY, client VARCHAR(255), project_name VARCHAR(255), ames_total smallint UNSIGNED, start_frame smallint UNSIGNED, end_frame smallint UNSIGNED, completed ENUM('1', '2', '3'))") 
#mycursor.execute("CREATE TABLE workers (workerIP VARCHAR(15), available TINYINT(1), current_project INT, FOREIGN KEY (current_project) REFERENCES project(projectID))")
#TINYINT(1) = true
#mycursor.execute("CREATE TABLE render (frame_number smallint UNSIGNED, projectID INT, FOREIGN KEY (projectID) REFERENCES project(projectID))")
#mycursor.execute("CREATE TABLE performance(projectID INT, project_name VARCHAR(255), workerIP VARCHAR(15), frames_total smallint UNSIGNED, time_total VARCHAR(100), start_time VARCHAR(100), end_time VARCHAR(100), worker1_avg_time VARCHAR(100), worker2_avg_time VARCHAR(100))")         

"""
#----------------------------------------------------------------------------------
"""

"""
#show all the tables in the renderdb database
mycursor.execute("SHOW TABLES")
for x in mycursor:
  print(x)

#describe the columns of the table (change the name to the table you want to DESCRIBE)
mycursor.execute("DESCRIBE performance")
result = mycursor.fetchall()
for row in result:
    print(row)
"""
"""
#Show the contents of the table (change the name of the to the table you want the data FROM)
mycursor.execute("SELECT * FROM performance")

# Fetch all rows from the cursor
result = mycursor.fetchall()

# Print the fetched data
for row in result:
    print(row)


mydb.commit()
mydb.close()
"""
"""
import random
from faker import Faker

# Initialize the Faker generator
fake = Faker()

# Function to generate a random IP address
def random_ip():
    return '.'.join([str(random.randint(0, 255)) for _ in range(4)])

# Function to generate a random time string
def random_time():
    return fake.date_time_between(start_date="-1y", end_date="now").isoformat(' ')

# Generate and insert data
for _ in range(10):
    projectID = random.randint(1, 100)
    project_name = fake.company()
    workerIP = random_ip()
    frames_total = random.randint(1, 500)
    time_total = f"{random.randint(1, 60)} minutes"
    start_time = random_time()
    end_time = random_time()
    worker1_avg_time = f"{random.randint(1, 30)} seconds"
    worker2_avg_time = f"{random.randint(1, 30)} seconds"

    # SQL command to insert data
    mycursor.execute(
        "INSERT INTO performance (projectID, project_name, workerIP, frames_total, time_total, start_time, end_time, worker1_avg_time, worker2_avg_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (projectID, project_name, workerIP, frames_total, time_total, start_time, end_time, worker1_avg_time, worker2_avg_time)
    )

# Commit changes and close the connection
mydb.commit()
mycursor.close()
mydb.close()

print("Data inserted successfully.")
"""