#include <WiFi.h>
#include <PubSubClient.h>

const char* ssid = "linksys"; //ZMIENIC na swoje
const char* password = ""; //ZMIENIC na swoje 
const char* mqtt_server = "51.83.134.60"; //ZMIENIC na swoje
const char* deviceName = "asdjklvzjhgvxsdfcxdvc"; //poki co nie trzeba zmieniac 
const char* pinTopic = "system/nowa/#"; //temat do odbioru wiadomosci
const int pin = 35;
int wartosc_czujnika=0;
int licznik_pomocniczy=0;
int licznik=0;




WiFiClient espClient;
PubSubClient client(espClient);


int czujnik_read()
{
  int wartosc=analogRead(pin);
  return wartosc;

}
void odbiorWiadomosci(String temat, byte* zawartosc, unsigned int dlugosc)
{
    Serial.println();
}
void ustawienieWifi()
{
  delay(5000);
  Serial.println();
  Serial.print("Laczenie z ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Polaczona z wifi.\nESP otrzymalo adres IP: ");
  Serial.println(WiFi.localIP());
}

void setup() {
  Serial.begin(115200);
  
  ustawienieWifi(); //polaczenie z wifi
  delay(10000);
  client.setServer(mqtt_server, 1883); //ustawienie serwera  mqtt
  client.connect(deviceName); //polaczenie z podana nazwa
  client.subscribe(pinTopic); //ustawienie nasluchiwania w podanym temacie
  client.setCallback(odbiorWiadomosci); //ustawienie funkcji do odbioru wiadomosci
}

void loop() {
  if (licznik==100)
  {
  licznik=0;
  client.publish("system/nowa/liczniki/aktywna","tak");
  }
  else
  {
  licznik+=1;  
  }
  delay(20);
  
  if (WiFi.status() != WL_CONNECTED)
  
  {
  WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
      WiFi.begin(ssid, password);
    delay(5000);
    Serial.print(".");
    if (WiFi.status()==WL_CONNECTED)
    {
       client.setServer(mqtt_server, 1883); //ustawienie serwera  mqtt
  client.connect(deviceName); //polaczenie z podana nazwa
  client.subscribe(pinTopic); //ustawienie nasluchiwania w podanym temacie
  client.setCallback(odbiorWiadomosci); //ustawienie funkcji do odbioru wiadomosci
      }    
  }
  }
  Serial.println(WiFi.status());
  delay(20);
 
  int wartosc_czujnika=czujnik_read();
  char buffer[5];
  sprintf(buffer,"%d", wartosc_czujnika);
  client.publish("czujnik",buffer);
  if (wartosc_czujnika==0)
  { 
    licznik_pomocniczy+=1;
    if (licznik_pomocniczy==10)
    {
      client.publish("system/nowa/liczniki/impulsy","1");
      delay(700);
    }
  }
  else
  {
    licznik_pomocniczy=0;
  }
}
