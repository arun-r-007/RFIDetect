# Smart Attendance System Using RFID and Facial Recognition

This repository contains the implementation of a **Smart Attendance System** that combines RFID technology and facial recognition to provide an efficient and secure way to mark attendance. The project utilizes Arduino Uno, an RFID module, a JHD 162A LCD, and a laptop camera for facial recognition, with data stored locally in a database.

## Features
- **RFID-Based Authentication**: Uses RFID tags for user identification.
- **Facial Recognition**: Verifies the user's identity using a laptop camera.
- **Attendance Logging**: Stores attendance data in a local database.
- **LCD Display**: Provides real-time feedback to the user.
- **Arduino Integration**: Processes RFID input and communicates with the LCD module.

## Components
1. **Arduino Uno**: The microcontroller for handling RFID input and controlling the LCD display.
2. **RFID Module (RC522)**: Reads RFID tags for user identification.
3. **LCD Module (JHD 162A)**: Displays system status and messages.
4. **Laptop Camera**: Captures images for facial recognition.
5. **Breadboard and Jumper Wires**: For circuit connections.
6. **Power Supply/Adapter**: Powers the Arduino and other components.
7. **Local Database**: Stores user and attendance data.


## Hardware Setup
### 1. Arduino to LCD Connection
The JHD 162A LCD module is connected to the Arduino Uno as follows:
- **RS (Register Select)**: Connected to Arduino digital pin 12.
- **E (Enable)**: Connected to Arduino digital pin 11.
- **D4-D7 (Data Pins)**: Connected to Arduino digital pins 5, 4, 3, and 2, respectively.
- **VCC and GND**: Connected to 5V and GND on the Arduino.
- **Contrast Adjustment**: A potentiometer is used to adjust the contrast of the LCD.

### 2. Arduino to RFID Module (RC522) Connection
The RFID module is connected to the Arduino Uno via SPI protocol:
- **SDA**: Connected to Arduino digital pin 10.
- **SCK**: Connected to Arduino digital pin 13.
- **MOSI**: Connected to Arduino digital pin 11.
- **MISO**: Connected to Arduino digital pin 12.
- **IRQ**: Not used (can remain unconnected).
- **GND**: Connected to Arduino GND.
- **3.3V**: Connected to Arduino 3.3V pin.

### 3. Database and Camera
- **Laptop Camera**: Captures user images for facial recognition.
- **Local Database**: Stores user details, attendance logs, and RFID tag mappings.

## Software Requirements
- **Arduino IDE**: For programming the Arduino Uno.
- **Python**: For implementing facial recognition and database operations.
- **Libraries**:
  - `MFRC522`: For RFID communication.
  - `LiquidCrystal`: For controlling the LCD module.
  - `OpenCV`: For facial recognition.
  - `SQLite3`: For managing the local database.

## How It Works
1. The user scans their RFID tag.
2. The Arduino reads the tag data and displays a prompt on the LCD.
3. The system triggers the laptop camera to capture the user's face.
4. Facial recognition is performed to verify the user.
5. If the RFID and facial recognition match, attendance is marked in the database.
6. The LCD displays a success message, and the system is ready for the next user.

## Future Enhancements
- Integration with cloud-based databases for centralized data storage.
- Mobile application for real-time attendance monitoring.
- Improved facial recognition algorithms for enhanced accuracy.


---

### Additional Notes
- Ensure that all components are connected securely before powering the system.
- Install all necessary libraries in both the Arduino IDE and Python environment before running the code.






# Read every Comment Lines clearly and  carefully 
