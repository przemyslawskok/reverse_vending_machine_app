

#include <WiFi.h>

#include <PubSubClient.h>

const char * ssid = "system"; //ZMIENIC na swoje
const char * password = "PROG#123"; //ZMIENIC na swoje 
const char * mqtt_server = "192.168.80.188"; //ZMIENIC na swoje
const char * deviceName = "esp-skrzydlata-licznik"; //poki co nie trzeba zmieniac 
const char * pinTopic = "system/skrzydlata/#"; //temat do odbioru wiadomosci
String newHostname = "esp-skrzydlata-licznik";
const int pin = 35;
int wartosc_czujnika = 0;
int licznik_pomocniczy = 0;
int licznik = 0;
extern EspClass ESP;

WiFiClient espClient;
PubSubClient client(espClient);


void ustawienieWifi() {
  delay(10);
  Serial.println();
  Serial.print("Laczenie z ");
  Serial.println("-------------");
  Serial.println(WiFi.getHostname());
  Serial.println(ssid);
   WiFi.hostname(newHostname.c_str());
  
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(20);
    Serial.print(".");
  } 
 
  Serial.println("");
  Serial.print("Polaczona z wifi.\nESP otrzymalo adres IP: ");
  Serial.println(WiFi.localIP());
}

void setup() {
  Serial.begin(115200);

  WiFi.hostname(newHostname.c_str());
  pinMode(pin, INPUT);
  pinMode(27, OUTPUT);
  digitalWrite(27,HIGH);
  ustawienieWifi(); //polaczenie z wifi
  delay(10);
  client.setServer(mqtt_server, 1883); //ustawienie serwera  mqtt
  client.connect(deviceName,deviceName, NULL  , NULL  ,2,true,"yes",false); //polaczenie z podana nazwa
 
}

void loop() {
  delay(20);

  if (WiFi.status() != WL_CONNECTED or client.connected() != 1)

  { 
    ESP.restart();
  }

  if (licznik == 100) {
    licznik = 0;
    
    client.publish("system/skrzydlata/liczniki/aktywna", "tak");
  } else {
    licznik += 1;
  }

  wartosc_czujnika = analogRead(pin);
  Serial.println(wartosc_czujnika);
  if (wartosc_czujnika < 4000) {
    licznik_pomocniczy += 1;
    if (licznik_pomocniczy == 10) {
      digitalWrite(27, HIGH);
      client.publish("system/skrzydlata/liczniki/impulsy", "1");
      delay(700);
    }
  } else {
    digitalWrite(27, LOW);
    licznik_pomocniczy = 0;
  }
}
