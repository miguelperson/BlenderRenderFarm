from manipulateDB import *

project_name = "MyProject"
client = "ClientA"
frames_total = 1000
start_frame = 1
end_frame = 1000

# Send gathered information to the database
insert_into_project(project_name, client, frames_total, start_frame, end_frame)