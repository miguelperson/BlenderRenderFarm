import mysql.connector

def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="7323",
        database="renderdb"
    )

def sql_exe(sql,val):
    try:
        mydb = connect_to_db()
        mycursor = mydb.cursor()
        
        mycursor.execute(sql, val)
        
        mydb.commit()
        mycursor.close()
        mydb.close()
    except mysql.connector.Error as err:
        print("Error:", err)

#Insert new row
def insert_into_project(project_name, client, frames_total, start_frame, end_frame):
    sql = "INSERT INTO project (project_name, client, frames_total, start_frame, end_frame) VALUES (%s, %s, %s, %s, %s)"
    val = (project_name, client, frames_total, start_frame, end_frame)
    sql_exe(sql,val)
    
        
def insert_into_workers(worker, available, projectID):
    sql = "INSERT INTO workers (worker, available, projectID) VALUES (%s, %s, %s)"
    val = (worker, available, projectID)
    sql_exe(sql,val)

def insert_into_render(frame_number, projectID):
    sql = "INSERT INTO workers (frame_number, projectID) VALUES (%s, %s)"
    val = (frame_number, projectID)
    sql_exe(sql,val)
        
#Delete the row
def remove_from_project(projectID,):
    sql = "DELETE FROM project WHERE projectID = %s"
    val = (projectID,)  
    sql_exe(sql,val)

#Reset auto-increment value
def reset_auto_increment(projectID,):       
    sql = "ALTER TABLE project AUTO_INCREMENT = %s"
    val = (projectID,)  
    sql_exe(sql,val)
        
        