import cv2
import face_recognition
import mysql.connector
import serial
import pickle
import schedule
import time
from datetime import datetime, timedelta
from db_connection import conn, cursor
import openpyxl
import os



print("\n\n\t\t\t\tAttendance Marker")

try:
    ser = serial.Serial('COM6', 9600, timeout=1)
    time.sleep(2)
except serial.SerialException as e:
    print(f"Error initializing serial communication: {e}")
    exit()

video_capture = cv2.VideoCapture(0)
if not video_capture.isOpened():
    print("Error accessing the camera. Check your camera setup.")
    exit()

print("\n\n\t\t\tSystem is ready. Waiting for Scanning\n\n\n")



def read_last_day_from_file():
    """Reads the last day value from a text file."""
    try:
        with open("last_day.txt", "r") as file:
            return int(file.read().strip())
    except FileNotFoundError:
        return 1

def write_last_day_to_file(day):
    """Writes the current day value to a text file."""
    with open("last_day.txt", "w") as file:
        file.write(str(day))



# for real time implement use this

'''

PERIOD_TIMINGS = [
    ("09:00", "09:10"),
    ("09:55", "10:05"),
    ("11:05", "11:15"),
    ("12:00", "12:10"),
    ("02:00", "02:10"),
    ("02:55", "03:05"),
    ("03:50", "04:00"),
]

'''

# for debugging use this

now = datetime.now()
print(now)

# Define period and break durations
PERIOD_DURATION = timedelta(seconds=15)
BREAK_DURATION = timedelta(seconds=10)

# Generate timings
PERIOD_TIMINGS = [
    (now.strftime("%H:%M:%S"), (now := now + PERIOD_DURATION).strftime("%H:%M:%S")),
    ((now := now + BREAK_DURATION).strftime("%H:%M:%S"), (now := now + PERIOD_DURATION).strftime("%H:%M:%S")),
    ((now := now + BREAK_DURATION).strftime("%H:%M:%S"), (now := now + PERIOD_DURATION).strftime("%H:%M:%S")),
    ((now := now + BREAK_DURATION).strftime("%H:%M:%S"), (now := now + PERIOD_DURATION).strftime("%H:%M:%S")),
    ((now := now + BREAK_DURATION).strftime("%H:%M:%S"), (now := now + PERIOD_DURATION).strftime("%H:%M:%S")),
    ((now := now + BREAK_DURATION).strftime("%H:%M:%S"), (now := now + PERIOD_DURATION).strftime("%H:%M:%S")),
    ((now := now + BREAK_DURATION).strftime("%H:%M:%S"), (now := now + PERIOD_DURATION).strftime("%H:%M:%S")),
]




# use in real im plementation for minutes



# def get_current_period():
#     now = datetime.now().time()
#     for idx, (start, end) in enumerate(PERIOD_TIMINGS):
#         start_time = datetime.strptime(start, "%H:%M").time()
#         end_time = datetime.strptime(end, "%H:%M").time()
#         if start_time <= now <= end_time:
#             return idx + 1
#     return None




# for debugging use this


def get_current_period():
    now = datetime.now().time()  # Current time with seconds
    for idx, (start, end) in enumerate(PERIOD_TIMINGS):
        start_time = datetime.strptime(start, "%H:%M:%S").time()  # Include seconds
        end_time = datetime.strptime(end, "%H:%M:%S").time()  # Include seconds
        if start_time <= now <= end_time:
            return idx + 1  # Return 1-based index of the current period
    return None  # If no period matches




def send_feedback(name, rfid_data, status):
    message = f"{name},{rfid_data},{status}!"
    ser.write(message.encode())
    print("\n")
    # print(f"\n\tSent to LCD: {message}\n\n")
    print("-x" * 59)

def send_feedback1(rfid_data, message, status):
    feedback = f"{rfid_data},{message},{status}"
    ser.write(feedback.encode())
    print("\n")
    # print(f"\n\tSent to LCD: {feedback}\n\n")

    print("-x" * 59)

def send_feedback2(rfid_data, message, status):
    feedback = f"{rfid_data},{message},{status}"
    ser.write(feedback.encode())
   
    # print(f"\n\tSent to LCD: {feedback}\n\n")





days = read_last_day_from_file()


def export_to_excel_and_clear():
    global days



    try:
        cursor.execute("SELECT * FROM Attendance")
        attendance_records = cursor.fetchall()

        file_name = "attendance_records.xlsx"


        if os.path.exists(file_name):
            wb = openpyxl.load_workbook(file_name)
            sheet = wb.active
        else:
            wb = openpyxl.Workbook()
            sheet = wb.active
            sheet.title = "Attendance Records"
            sheet.append([None])
            sheet.append([None])
            headers = ["Record ID", "Student Name", "Roll no", "Period", "Timestamp", "Status"]
            sheet.append(headers)

        sheet.append([None])
        sheet.append([None])
        sheet.append([f"DAY : {days}    [{now}]"])
        sheet.append([None])
        sheet.append([None])

        for record in attendance_records:
            sheet.append(record)

        wb.save(file_name)
        # print(f"\n\n\tAttendance records exported to {file_name}")

        try:
            cursor.execute("DROP TABLE IF EXISTS Attendance")
            # print("\n\n\tAttendance table dropped successfully.")

            # Recreate the Attendance table
            create_table_query = """
            CREATE TABLE Attendance (
                record_id INT AUTO_INCREMENT PRIMARY KEY,
                user_name VARCHAR(50) NOT NULL,
                rfid_tag VARCHAR(50) NOT NULL,
                period INT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                status VARCHAR(20) NOT NULL CHECK (status IN ('Present', 'Absent', 'Frozen'))
            )
            """
            cursor.execute(create_table_query)
            conn.commit()


        except Exception as e:
            print(f"Error resetting the Attendance table: {e}")


        days += 1
        write_last_day_to_file(days)

    except Exception as e:
        print(f"Error exporting data or clearing table: {e}")


# use in real implementation for minutes




# def check_end_of_day():

#     now = datetime.now().time()
#     last_period_end_time = datetime.strptime(PERIOD_TIMINGS[-1][1], "%H:%M").time()

#     if now > last_period_end_time:
#         print("\n\n\tEnd of the DAY Attendenced  clossed ")
#         export_to_excel_and_clear()





# for debugging use this



def check_end_of_day():
    now = datetime.now().time()  # Current time with seconds
    last_period_end_time = datetime.strptime(PERIOD_TIMINGS[-1][1], "%H:%M:%S").time()  # Include seconds

    if now > last_period_end_time:
        print("\n\n\tEnd of the DAY Attendance closed.")
        export_to_excel_and_clear()  # Call the function to export and clear data




i=1
cp=0



def mark_absent_if_not_scanned():
    global cp
    global i
    global now
    global PERIOD_TIMINGS


    """
    Marks all users as absent if they have not scanned their RFID during the current period.
    """
    current_period = get_current_period()


    if current_period :
        i=1
        cp=current_period
        return

    if current_period is None:

        if i==1:
            current_time = datetime.now()
            current_period=cp

            print("\n\n\t\t\t\tAbsentees")

            print(f"\n\tMarking absentees for Period {current_period} at {current_time.strftime('%H:%M:%S')}...\n\n")

            cursor.execute("SELECT user_id, name, rfid_tag FROM Users")
            users = cursor.fetchall()
            send_feedback2("Attendenced","clossed ", " !!!!")
            for user_id, user_name, rfid_tag in users:
                cursor.execute(
                    "SELECT timestamp FROM Attendance WHERE rfid_tag = %s AND period = %s",
                    (rfid_tag, current_period)
                )
                result = cursor.fetchone()
                if not result:
                    cursor.execute(
                        "INSERT INTO Attendance (user_name, rfid_tag, status, period, timestamp) VALUES (%s, %s, 'Absent', %s, %s)",
                        (user_name, rfid_tag, current_period, current_time)
                    )
                    conn.commit()
                    print(f"\tMarked {user_name} as absent for Period {current_period}.")




            print(f"\n\n\tAbsentees marked for Period {current_period}.")
            print("\n")
            print("-x" * 59)


            i=0

        if current_period==7:
            check_end_of_day()


            # for real time implement use this

            '''

            PERIOD_TIMINGS = [
                ("09:00", "09:10"),
                ("09:55", "10:05"),
                ("11:05", "11:15"),
                ("12:00", "12:10"),
                ("02:00", "02:10"),
                ("02:55", "03:05"),
                ("03:50", "04:00"),
            ]

            '''
            # for debugging use this


            now = datetime.now()

            # Define period and break durations
            PERIOD_DURATION = timedelta(seconds=15)
            BREAK_DURATION = timedelta(seconds=10)

            # Generate timings
            PERIOD_TIMINGS = [
                (now.strftime("%H:%M:%S"), (now := now + PERIOD_DURATION).strftime("%H:%M:%S")),
                ((now := now + BREAK_DURATION).strftime("%H:%M:%S"), (now := now + PERIOD_DURATION).strftime("%H:%M:%S")),
                ((now := now + BREAK_DURATION).strftime("%H:%M:%S"), (now := now + PERIOD_DURATION).strftime("%H:%M:%S")),
                ((now := now + BREAK_DURATION).strftime("%H:%M:%S"), (now := now + PERIOD_DURATION).strftime("%H:%M:%S")),
                ((now := now + BREAK_DURATION).strftime("%H:%M:%S"), (now := now + PERIOD_DURATION).strftime("%H:%M:%S")),
                ((now := now + BREAK_DURATION).strftime("%H:%M:%S"), (now := now + PERIOD_DURATION).strftime("%H:%M:%S")),
                ((now := now + BREAK_DURATION).strftime("%H:%M:%S"), (now := now + PERIOD_DURATION).strftime("%H:%M:%S")),
            ]





schedule.every(1).second.do(mark_absent_if_not_scanned)




rfid_last_processed = {}



while True:
    try:
        schedule.run_pending()

        rfid_data = None

        if ser.in_waiting > 0:
            rfid_data = ser.readline().decode('utf-8').strip().replace("UID tag: ", "")
            current_time = time.time()
            if rfid_data in rfid_last_processed and current_time - rfid_last_processed[rfid_data] < 2:
                continue

            rfid_last_processed[rfid_data] = current_time

            print(f"\n\n\tStudent Roll No: {rfid_data}")

            if not rfid_data:
                continue

            cursor.execute("SELECT user_id, name, face_encoding FROM Users WHERE rfid_tag = %s", (rfid_data,))
            result = cursor.fetchone()

            if result:
                user_id, user_name, face_encoding_data = result
                print(f"\n\n\tStudent Name: {user_name}")

                current_period = get_current_period()
                if current_period is None:
                    h=datetime.now()
                    print(f"\n\n\tCurrent Time {h}  Not within any period's attendance Time .\n")
                    send_feedback1(rfid_data, "Invalid", " Time")

                    continue

                cursor.execute(
                    "SELECT timestamp FROM Attendance WHERE rfid_tag = %s AND period = %s",
                    (rfid_data, current_period)
                )

                attendance_result = cursor.fetchone()
                if attendance_result:
                    print(f"\n\n\tAttendance already marked for {user_name} in Period {current_period}.\n")
                    send_feedback(user_name, rfid_data, "Marked")
                    continue

                if face_encoding_data:
                    try:
                        face_encoding = pickle.loads(face_encoding_data)
                    except pickle.UnpicklingError as e:
                        print(f"Error unpickling face encoding: {e}")
                else:
                    print("No face encoding data found.")


            else:
                print("\n\n\tStudent roll number does not belong to this class.\n")
                send_feedback1(rfid_data, "Invalid", " Roll No")
                continue




            ret, frame = video_capture.read()
            if not ret:
                print("\n\n\tFailed to capture frame. Exiting...")
                break

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            recognized = False

            for (top, right, bottom, left), current_face_encoding in zip(face_locations, face_encodings):
                face_distances = face_recognition.face_distance([face_encoding], current_face_encoding)
                match = face_distances[0] < 0.4

                if match:
                    label = f"Match Found: {user_name}"
                    color = (0, 255, 0)
                    cursor.execute(
                        "INSERT INTO Attendance (user_name, rfid_tag, status, period, timestamp) VALUES (%s, %s, 'Present', %s, %s)",
                        (user_name, rfid_data, current_period, datetime.now())
                    )
                    conn.commit()
                    print(f"\n\n\tAttendance marked for {user_name} in Period {current_period}\n")
                    send_feedback(user_name, rfid_data, "Present")
                    recognized = True

                    cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(frame, label, (left + 6, bottom - 6), font, 0.5, color, 1)

                    cv2.imshow("Face Recognition", frame)
                    cv2.waitKey(1000)
                    cv2.destroyAllWindows()

                    break

                if not recognized:

                    label = "No Match"
                    color = (0, 0, 255)
                    print(f"\n\n\tFace not recognized for {user_name} ({rfid_data}). Attendance NOT marked.\n")
                    send_feedback(user_name, rfid_data, " NULL !")

                    cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(frame, label, (left + 6, bottom - 6), font, 0.5, color, 1)

                    cv2.imshow("Face Recognition", frame)
                    cv2.waitKey(1000)
                    cv2.destroyAllWindows()

                    break



    except Exception as e:
        print(f"Error: {e}")



video_capture.release()
ser.close()
conn.close()
cv2.destroyAllWindows()
