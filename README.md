# RFIDetect – Smart Attendance System Using RFID & Facial Recognition

**RFIDetect** is a hybrid smart attendance system that integrates **RFID technology** and **Facial Recognition** for secure, contactless, and automated attendance marking. Developed using **Arduino Uno**, **RFID RC522 Module**, **JHD 162A LCD**, and a **laptop camera**, the system ensures accurate user identification with real-time feedback and local database logging.

---

## Features

* **RFID-Based Authentication** – Efficient identification using RFID tags
* **Facial Recognition** – Validates the user identity via camera
* **Attendance Logging** – Stores attendance records in a local SQLite database
* **LCD Feedback** – Real-time messages during the authentication process
* **Arduino Integration** – Handles sensor input and LCD output operations

---

## Components

| Component             | Description                          |
| --------------------- | ------------------------------------ |
| Arduino Uno           | Controls RFID and LCD modules        |
| RFID Module (RC522)   | Reads RFID tag data                  |
| LCD Module (JHD 162A) | Displays messages and system prompts |
| Laptop Camera         | Captures and verifies user faces     |
| Breadboard & Wires    | For connecting circuit components    |
| Power Supply/Adapter  | Provides power to the hardware       |
| SQLite Database       | Stores user and attendance records   |

---

## Hardware Setup

### 1. LCD to Arduino Wiring

* RS → Pin 12
* E → Pin 11
* D4–D7 → Pins 5, 4, 3, 2
* VCC/GND → 5V/GND
* Potentiometer connected to adjust LCD contrast

### 2. RFID Module (RC522) to Arduino (via SPI)

* SDA → Pin 10
* SCK → Pin 13
* MOSI → Pin 11
* MISO → Pin 12
* 3.3V/GND → Arduino 3.3V/GND
* IRQ → Not connected

### 3. Laptop Camera + Database

* Camera is used to capture user face
* Facial recognition is performed and matched against stored image mappings in SQLite

---

## Software Requirements

Install the following tools and libraries:

* **Arduino IDE** for programming the microcontroller
* **Python 3.x** for facial recognition and database operations

### Python Libraries:

* `MFRC522` – For RFID communication
* `LiquidCrystal` – For controlling the LCD
* `OpenCV` – For face detection and recognition
* `SQLite3` – For local database operations

---

## Workflow Overview

1. The user scans their RFID tag.
2. The LCD prompts the user to look at the camera.
3. The camera captures the face and verifies it against the database.
4. If the face matches the RFID identity, attendance is recorded.
5. LCD displays success or denial based on match result.
6. System resets for the next user.

---

## Sample Logic Flow

```
[Scan RFID] ---> [Face Detected] ---> [Match Check]
                                      |--> Yes --> Attendance Recorded
                                      |--> No  --> Access Denied
```

---

## Demo Screenshot

![Demo Image](https://github.com/user-attachments/assets/c1b604a9-1d28-4b13-b716-4ec3ea3a1669)

---

## Future Enhancements

* Integration with a cloud database for centralized access
* Real-time attendance tracking via mobile application
* Enhanced face recognition with deep learning models
* User roles and access-level-based dashboards (Admin, Staff, etc.)

---

## Notes

* Ensure all hardware is connected correctly before powering on.
* All required libraries must be installed in both Arduino IDE and Python environment.



# Read every Comment Lines clearly and carefully 
