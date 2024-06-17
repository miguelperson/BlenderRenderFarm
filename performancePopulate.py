import mysql.connector
from mysql.connector import Error
import random
from datetime import datetime, timedelta


# Function to generate random data and populate the performance table
def populate_performance_table(num_entries):
    try:
        # Connect to MySQL database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="7323",
            database="renderdb"
        )

        # Create a cursor object
        mycursor = mydb.cursor()

        # Generate and insert random data
        for _ in range(num_entries):
            projectID = random.randint(1, 100)
            project_name = f"Project_{projectID}"
            workerIP = f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}"
            frames_total = random.randint(500, 2000)
            time_total = f"{random.randint(1, 24)} hours {random.randint(0, 59)} minutes"
            start_time = datetime.now() - timedelta(days=random.randint(1, 30))
            end_time = start_time + timedelta(hours=random.randint(1, 12))
            worker1_avg_time = f"{random.randint(1, 5)} hours {random.randint(0, 59)} minutes"
            worker2_avg_time = f"{random.randint(1, 5)} hours {random.randint(0, 59)} minutes"

            # SQL query to insert random data into the performance table
            sql = "INSERT INTO performance (projectID, project_name, workerIP, frames_total, time_total, \
                   start_time, end_time, worker1_avg_time, worker2_avg_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

            # Define the values to be inserted
            values = (projectID, project_name, workerIP, frames_total, time_total,
                      start_time, end_time, worker1_avg_time, worker2_avg_time)

            # Execute the query
            mycursor.execute(sql, values)

        # Commit changes to the database
        mydb.commit()

        print(f"{num_entries} records inserted successfully into performance table.")

    except Error as e:
        print(f"Error inserting data into MySQL table: {e}")

    finally:
        # Close cursor and database connection
        if mycursor:
            mycursor.close()
        if mydb:
            mydb.close()


# Example usage:
if __name__ == "__main__":
    populate_performance_table(10)  # Inserting 10 random records into the performance table
