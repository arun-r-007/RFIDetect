#include <SPI.h>
#include <MFRC522.h>
#include <LiquidCrystal.h>

#define SS_PIN 10  
#define RST_PIN 9  
MFRC522 mfrc522(SS_PIN, RST_PIN); 

#define BUZZER_PIN 6  

bool messageDisplayed = false;

LiquidCrystal lcd(8, 7, 5, 4, 3, 2); 

void setup() {
  Serial.begin(9600);  
  SPI.begin();         
  mfrc522.PCD_Init();  

  pinMode(BUZZER_PIN, OUTPUT);   

  lcd.begin(16, 2);  

  lcd.print("Attendance");
  lcd.setCursor(0, 1);
  lcd.print("          Marker");
  
  delay(2000); 
  lcd.clear();  
  delay(50); 
}




void loop() {

  if (Serial.available()) {
    String message = Serial.readString();  


    int firstComma = message.indexOf(',');
    int secondComma = message.indexOf(',', firstComma + 1);
    
    if (firstComma > 0 && secondComma > firstComma) {
      String name = message.substring(0, firstComma);
      String roll_no = message.substring(firstComma + 1, secondComma);
      String status = message.substring(secondComma + 1);
      

      if (status == " Roll No" || status == " !!!!" || status == " Time"|| status == " NULL !!" ) {
          
          tone(BUZZER_PIN, 400, 500); 
      } else {
          
          tone(BUZZER_PIN, 1000, 500); 
      }

      

      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print(name);       

      lcd.setCursor(0, 1); 
      lcd.print(roll_no); 
      lcd.print(",");
      lcd.print(status);

      delay(3000);
      
      noTone(BUZZER_PIN); 
      messageDisplayed = false;
      lcd.clear();

    }
  }

  if (!messageDisplayed) {
    lcd.clear();
    lcd.print("Welcome...");
    messageDisplayed = true; 
  }


  if (mfrc522.PICC_IsNewCardPresent()) {  
    if (mfrc522.PICC_ReadCardSerial()) {  

      String content = "";
      for (byte i = 0; i < mfrc522.uid.size; i++) {
        content += String(mfrc522.uid.uidByte[i], HEX);  
      }
      content.toUpperCase();


      Serial.print("UID tag: ");
      Serial.println(content);
      
      String validUIDs[] = {"633CCAE4", "12345678", "87654321"};
      bool isValid = false;

      for (String uid : validUIDs) {
        if (content == uid) {
          isValid = true;
          break;
        }
      }
      messageDisplayed = false;
    }
  }
}
