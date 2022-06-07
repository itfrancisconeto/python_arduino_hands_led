char cmd;

void setup() {
  Serial.begin(9600);
  pinMode(3, OUTPUT);
  digitalWrite(3, LOW);
}

void loop() {
  cmd = Serial.read();
  if (cmd == 'l') 
  {
    digitalWrite(3, HIGH); 
  }
  else if (cmd == 'd') 
  {
    digitalWrite(3, LOW);
  }
}
