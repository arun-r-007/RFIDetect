import face_recognition
import mysql.connector
import pickle
from db_connection import conn, cursor

def register_user(rfid_tag, name, face_image_path):
    try:
        
        image = face_recognition.load_image_file(face_image_path)
        face_encodings = face_recognition.face_encodings(image)

        if len(face_encodings) == 0:
            print("No face detected in the image. Please provide a clear image.")
            return
        
        face_encoding = face_encodings[0]  
        
        
        serialized_face_encoding = pickle.dumps(face_encoding)

        
        cursor.execute("INSERT INTO Users (name, rfid_tag, face_encoding) VALUES (%s, %s, %s)",
                       (name, rfid_tag, serialized_face_encoding))
        conn.commit()
        print(f"User {name} registered successfully!")

    except mysql.connector.Error as db_err:
        print(f"Database error during user registration: {db_err}")
    except Exception as e:
        print(f"Unexpected error during user registration: {e}")


#  register_user('RFID tag no', 'name', 'photo.jpg')

register_user('12ad34', 'name', 'photo.jpg')

