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
def insert_into_project(projectID, client, project_name, ames_total, start_frame, end_frame, completed):
    sql = "INSERT INTO project (projectID, client, project_name, ames_total, start_frame, end_frame, completed) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (projectID, client, project_name, ames_total, start_frame, end_frame, completed)
    sql_exe(sql,val)
    
        
def insert_into_workers(workerIP, available, current_project):
    sql = "INSERT INTO workers (workerIP, available, current_project) VALUES (%s, %s, %s)"
    val = (workerIP, available, current_project)
    sql_exe(sql,val)

def insert_into_render(frame_number, projectID):
    sql = "INSERT INTO workers (frame_number, projectID) VALUES (%s, %s)"
    val = (frame_number, projectID)
    sql_exe(sql,val)
        
def insert_into_performance(projectID, workerID, frames_total, time_total, start_time, end_time, worker1_avg_time, worker2_avg_time):
    sql = "INSERT INTO workers (projectID, workerID, frames_total, time_total, start_time, end_time, worker1_avg_time, worker2_avg_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    val = (projectID, workerID, frames_total, time_total, start_time, end_time, worker1_avg_time, worker2_avg_time)
    sql_exe(sql,val)

#Delete the row
def remove_from_project(projectID,):
    sql = "DELETE FROM project WHERE projectID = %s"
    val = (projectID,)  
    sql_exe(sql,val)

def remove_from_workers(projectID):
    sql = "DELETE FROM project WHERE projectID = %s"
    val = (projectID,)  
    sql_exe(sql,val)

def remove_from_render(projectID,):
    sql = "DELETE FROM project WHERE projectID = %s"
    val = (projectID,)  
    sql_exe(sql,val)

def remove_from_performance(projectID,):
    sql = "DELETE FROM performance WHERE projectID = %s"
    val = (projectID,)  
    sql_exe(sql,val)

#Reset auto-increment value
def reset_auto_increment(projectID,):       
    sql = "ALTER TABLE project AUTO_INCREMENT = %s"
    val = (projectID,)  
    sql_exe(sql,val)
        
        