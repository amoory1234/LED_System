void setup() {
  Serial.begin(9600);
  pinMode(2, OUTPUT);  
  pinMode(3, OUTPUT);  
  pinMode(4, OUTPUT);  
  pinMode(5, OUTPUT);  
}

void loop() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');

    digitalWrite(2, LOW);
    digitalWrite(3, LOW);
    digitalWrite(4, LOW);
    digitalWrite(5, LOW);

    if (command == "led1") {
      digitalWrite(2, HIGH);
    } else if (command == "led2") {
      digitalWrite(3, HIGH);
    } else if (command == "led3") {
      digitalWrite(4, HIGH);
    } else if (command == "led4") {
      digitalWrite(5, HIGH);
    } else if (command == "on") {
      digitalWrite(2, HIGH);
      digitalWrite(3, HIGH);
      digitalWrite(4, HIGH);
      digitalWrite(5, HIGH);
    }
 
  }
}
