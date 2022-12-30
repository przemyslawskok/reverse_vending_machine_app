#include <WiFi.h>
#include <PubSubClient.h>

const char* ssid = "progresja_gora"; //ZMIENIC na swoje
const char* password = "Test12345"; //ZMIENIC na swoje
const char* mqtt_server = "51.83.134.60"; //ZMIENIC na swoje
const char* deviceName = "asdjklvzxasdfcxdvc"; //poki co nie trzeba zmieniac
//ale przy wiekszej ilosci urzaden kazde musi miec swoja nazwe

const char* startMessageTopic = "esp32"; //temat do wyslania wiadomosci
const char* pinTopic = "system/nowa/#"; //temat do odbioru wiadomosci
const int ledPin = 27; //numer pinu diody, ZMIENIC JESLI TRZEBA
const int pin = 34;
int wartosc_czujnika = 0;
int licznik = 0;
int licznik_pomocniczy = 0;


WiFiClient espClient;
PubSubClient client(espClient);


int czujnik_read()
{
  int wartosc = analogRead(pin);
  return wartosc;
}
void reconnect()
{
  bool ctd = false;
  //funkcja jest wywolywana jesli utracono polaczenie z serwerem
  Serial.println("Rozlaczono!");
  while (!ctd)
  {
    Serial.print("Laczenie z serwerem...");
    if (client.connect(deviceName))
    {
      ctd = true;
      Serial.println("Polaczono!");
    }
    else
    {
      Serial.print(".");
      delay(1000);
    }
  }
}

void odbiorWiadomosci(String temat, byte* zawartosc, unsigned int dlugosc)
{
  if (temat == "system/nowa/liczniki/reset_s")
  {
    Serial.println("RESET");
    licznik = 0;
    client.publish("system/nowa/liczniki/reset", "ok");
  }
  if (temat == "system/nowa/liczniki/czy_aktywna")
  {
    Serial.println("czy_aktywna");
    client.publish("system/nowa/liczniki/aktywna", "tak");
  }

}

void ustawienieWifi()
{
  delay(10);
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
  pinMode(pin, INPUT);
  delay(1000);
  ustawienieWifi(); //polaczenie z wifi
  delay(1000);
  client.setServer(mqtt_server, 1883); //ustawienie serwera  mqtt
  client.connect(deviceName); //polaczenie z podana nazwa
  client.subscribe(pinTopic); //ustawienie nasluchiwania w podanym temacie
  client.setCallback(odbiorWiadomosci); //ustawienie funkcji do odbioru wiadomosci
  client.publish(startMessageTopic, "Hello from ESP32"); //wyslanie pierwszej wiadomosci
  attachInterrupt(digitalPinToInterrupt(pin), zlicz,HIGH);
}



void loop() {
delay(20);
client.publish("czujnik", "jestem");
  int wartosc_czujnika = czujnik_read();
  char buffer[5];
  sprintf(buffer, "%d", wartosc_czujnika);
  client.publish("czujnik", buffer);
  if (wartosc_czujnika == 4095)
  {
    licznik_pomocniczy += 1;
    if (licznik_pomocniczy == 10)
    {
      licznik += 1;
      char buffer[5];
      sprintf(buffer, "%d", licznik);
      client.publish("system/nowa/liczniki/impulsy", buffer);
      client.publish("system/nowa/liczniki/suma", buffer);
      delay(700);
    }
  }
  else
  {
    licznik_pomocniczy = 0;
  }









  if (!client.connected()) //jesli klient zostal rozlaczony
  {
    reconnect(); //polacz ponownie
  }
  if (!client.loop())
    client.connect(deviceName); //upewnienie sie, ze klient jest stale podlaczony
}





void zlicz()
{
  
  if (wartosc_czujnika == 4095)
  {
    licznik_pomocniczy += 1;
  }
  else
  {
    licznik_pomocniczy = 0;
  }
}

void przerwanie()
{
  Serial.println("PRZERWANIE");
}
