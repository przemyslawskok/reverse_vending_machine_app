

const int IN_PHOTO_HAND = PB1;
bool toggle_photo_hand = false; 

void setup() {
  Serial.begin(115200);
  // put your setup code here, to run once:
  pinMode(IN_PHOTO_HAND,INPUT_PULLUP);


  attachInterrupt(IN_PHOTO_HAND, change_sensor_state, CHANGE);  
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println(toggle_photo_hand);

}


void change_sensor_state()
{
  toggle_photo_hand = !toggle_photo_hand;
}