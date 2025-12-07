#include <ESP8266WiFi.h>        
#include <ESP8266WebServer.h>   
#include <DNSServer.h>          // Necesaria para que WiFiManager pueda redirigir al usuario
#include <ESP8266mDNS.h>        // Viene integrada para usar nombres (.local)
#include <WiFiManager.h>        // gestiona la conexión


// CONFIGURACION: 

ESP8266WebServer server(80); //set port 80 (http)

// pines para el ESP-01:
const int PIN_ROJO = 0;  
const int PIN_VERDE = 2; 

// AJUSTE DE COLOR 
const int MAX_RED_PWM = 1023;
const int MAX_GREEN_PWM = 600; //mejoro la transicion

// FUNCION PARA CONTROL MANUAL
void handleManual() {
    if (server.hasArg("r") && server.hasArg("g")) {
        int r = server.arg("r").toInt();
        int g = server.arg("g").toInt();
        // Limitar por seguridad
        r = constrain(r, 0, 1023);
        g = constrain(g, 0, 1023);
        
        analogWrite(PIN_ROJO, r);
        analogWrite(PIN_VERDE, g);
        server.send(200, "text/plain", "Manual OK");
    } else {
        server.send(400, "text/plain", "Faltan datos");
    }
}

void setHealthColor(int hp) {
    int targetR, targetG;

    if (hp > 50) {
        targetG = MAX_GREEN_PWM; 
        //50% rojo al max (amarillo). En 100% rojo 0 (Verde)
        targetR = map(hp, 50, 100, MAX_RED_PWM, 0);
        
    } else {
        targetR = MAX_RED_PWM;
        if (hp <= 10) {
             // Si es 10% o menos rojo puro
            targetG = 0;
        } else {
            // Al 11% empieza a subir el verde.
            targetG = map(hp, 10, 50, 0, MAX_GREEN_PWM);
        }
    }
    analogWrite(PIN_ROJO, targetR);
    analogWrite(PIN_VERDE, targetG);
}

void handleHealth() {
    if (server.hasArg("percent")) {
        int hp = server.arg("percent").toInt();
        hp = constrain(hp, 0, 100); 
        setHealthColor(hp);
        server.send(200, "text/plain", "OK");
    } else {
        server.send(400, "text/plain", "Falta parametro percent");
    }
}

void setup() {
    analogWriteRange(1023);

    pinMode(PIN_ROJO, OUTPUT);
    pinMode(PIN_VERDE, OUTPUT);
    
    // Init apagados
    analogWrite(PIN_ROJO, 0);
    analogWrite(PIN_VERDE, 0);

    // Init WiFiManager
    WiFiManager wifiManager;

    // - Intenta conectarse al último WiFi guardado.
    // - Si falla, crea una red llamada "WoWRGB".
    // - En wowrgb.local configuras la red y le das la clave
    // - Si conecta, guarda la clave y se reinicia.
  
    if (!wifiManager.autoConnect("WoWRGB")) {
        ESP.reset();
        delay(2000); //para darle tiempo a que ejecuta el reset
    }

    // Init mDNS
    // Servicio que responde a "wowrgb.local"
    MDNS.begin("WoWRGB");
    
    server.on("/health", handleHealth);
    
    // RUTA MANUAL
    server.on("/manual", handleManual);
    //------------------------------------
    
    server.begin();
}

void loop() {
    MDNS.update(); // Procesa las peticiones .local en ejecucion
    server.handleClient();
}