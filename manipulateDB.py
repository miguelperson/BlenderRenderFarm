import mysql.connector

def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="7323",
        database="renderdb"
    )

def insert_into_project(project_name, client, frames_total, start_frame, end_frame):
    try:
        mydb = connect_to_db()
        mycursor = mydb.cursor()
        
        sql = "INSERT INTO project (project_name, client, frames_total, start_frame, end_frame) VALUES (%s, %s, %s, %s, %s)"
        val = (project_name, client, frames_total, start_frame, end_frame)
        
        mycursor.execute(sql, val)
        
        mydb.commit()
        mycursor.close()
        mydb.close()
    except mysql.connector.Error as err:
        print("Error:", err)

def insert_into_workers(worker, available, projectID):
    try:
        mydb = connect_to_db()
        mycursor = mydb.cursor()
        
        sql = "INSERT INTO workers (worker, available, projectID) VALUES (%s, %s, %s)"
        val = (worker, available, projectID)
        
        mycursor.execute(sql, val)
        
        mydb.commit()
        mycursor.close()
        mydb.close()
    except mysql.connector.Error as err:
        print("Error:", err)

def insert_into_render(frame_number, projectID):
    try:
        mydb = connect_to_db()
        mycursor = mydb.cursor()
        
        sql = "INSERT INTO workers (frame_number, projectID) VALUES (%s, %s)"
        val = (frame_number, projectID)
        
        mycursor.execute(sql, val)
        
        mydb.commit()
        mycursor.close()
        mydb.close()
    except mysql.connector.Error as err:
        print("Error:", err)