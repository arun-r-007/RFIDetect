import mysql.connector

try:
    
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="xxxxxx",            #password  
        auth_plugin='mysql_native_password', 
        database="attendance_system"
    )

    
    
    cursor = conn.cursor()

except mysql.connector.Error as err:
    print(f"Error: {err}")
    cursor = None
    conn = None


