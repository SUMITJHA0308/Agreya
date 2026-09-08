#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>


// =====================================================
// WIFI
// =====================================================

const char* WIFI_SSID = "YOUR_WIFI_NAME";
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";


// =====================================================
// MQTT
// =====================================================

const char* MQTT_BROKER = "10.214.139.57";
const int MQTT_PORT = 1883;

const char* SENSOR_TOPIC =
    "mine/NODE_2/sensors";

const char* EVENT_TOPIC =
    "mine/NODE_2/events";

const char* NODE_ID =
    "NODE_2";


// =====================================================
// PINS
// DO NOT CHANGE
// =====================================================

#define TRIG_PIN D1
#define ECHO_PIN D2

#define GREEN_LED D5
#define RED_LED D6


// =====================================================
// DISTANCE THRESHOLDS
// =====================================================

#define NORMAL_DISTANCE 18
#define CRITICAL_DISTANCE 15


// =====================================================
// MQTT
// =====================================================

WiFiClient espClient;

PubSubClient mqttClient(
    espClient
);


// =====================================================
// STATE
// =====================================================

String currentStatus =
    "GREEN";

bool yellowAlertSent =
    false;

bool roverCommandSent =
    false;


// =====================================================
// WIFI
// =====================================================

void connectWiFi()
{
    Serial.println();
    Serial.println(
        "Connecting to WiFi..."
    );

    WiFi.mode(
        WIFI_STA
    );

    WiFi.begin(
        WIFI_SSID,
        WIFI_PASSWORD
    );

    while (
        WiFi.status() !=
        WL_CONNECTED
    )
    {
        delay(500);
        Serial.print(".");
    }

    Serial.println();

    Serial.println(
        "WiFi connected"
    );

    Serial.print(
        "ESP8266 IP: "
    );

    Serial.println(
        WiFi.localIP()
    );
}


// =====================================================
// MQTT CONNECT
// =====================================================

void connectMQTT()
{
    while (
        !mqttClient.connected()
    )
    {
        Serial.println(
            "Connecting to MQTT broker..."
        );

        String clientID =
            String(NODE_ID) +
            "_" +
            String(
                ESP.getChipId(),
                HEX
            );

        if (
            mqttClient.connect(
                clientID.c_str()
            )
        )
        {
            Serial.println(
                "MQTT connected"
            );
        }
        else
        {
            Serial.print(
                "MQTT connection failed: "
            );

            Serial.println(
                mqttClient.state()
            );

            delay(2000);
        }
    }
}


// =====================================================
// READ HC-SR04
// =====================================================

float readDistance()
{
    digitalWrite(
        TRIG_PIN,
        LOW
    );

    delayMicroseconds(2);

    digitalWrite(
        TRIG_PIN,
        HIGH
    );

    delayMicroseconds(10);

    digitalWrite(
        TRIG_PIN,
        LOW
    );


    long duration =
        pulseIn(
            ECHO_PIN,
            HIGH,
            30000
        );


    if (duration == 0)
    {
        return -1;
    }


    float distance =
        duration * 0.0343 / 2.0;


    return distance;
}


// =====================================================
// SEND EVENT
// =====================================================

void sendEvent(
    const char* eventName,
    float distance
)
{
    JsonDocument doc;

    doc["node_id"] =
        NODE_ID;

    doc["event"] =
        eventName;

    doc["distance_cm"] =
        distance;


    String payload;

    serializeJson(
        doc,
        payload
    );


    mqttClient.publish(
        EVENT_TOPIC,
        payload.c_str()
    );


    Serial.println();

    Serial.print(
        "EVENT SENT: "
    );

    Serial.println(
        eventName
    );
}


// =====================================================
// SEND ROVER COMMAND
// =====================================================

void sendRoverCommand(
    float distance
)
{
    JsonDocument doc;

    doc["node_id"] =
        NODE_ID;

    doc["command"] =
        "start_rover";

    doc["distance_cm"] =
        distance;


    String payload;

    serializeJson(
        doc,
        payload
    );


    mqttClient.publish(
        EVENT_TOPIC,
        payload.c_str()
    );


    Serial.println();

    Serial.println(
        "ROVER START COMMAND SENT"
    );
}


// =====================================================
// DETERMINE STATUS
// =====================================================

String determineStatus(
    float distance
)
{
    if (distance < 0)
    {
        return "GREEN";
    }

    if (
        distance <=
        CRITICAL_DISTANCE
    )
    {
        return "RED";
    }

    if (
        distance <=
        NORMAL_DISTANCE
    )
    {
        return "YELLOW";
    }

    return "GREEN";
}


// =====================================================
// UPDATE LEDs
// =====================================================

void updateLEDs(
    const String& status
)
{
    if (status == "GREEN")
    {
        digitalWrite(
            GREEN_LED,
            HIGH
        );

        digitalWrite(
            RED_LED,
            LOW
        );
    }

    else if (status == "YELLOW")
    {
        digitalWrite(
            GREEN_LED,
            LOW
        );

        digitalWrite(
            RED_LED,
            LOW
        );
    }

    else
    {
        digitalWrite(
            GREEN_LED,
            LOW
        );

        digitalWrite(
            RED_LED,
            HIGH
        );
    }
}


// =====================================================
// PUBLISH SENSOR DATA
// =====================================================

void publishSensorData(
    float distance,
    const String& status
)
{
    JsonDocument doc;

    doc["node_id"] =
        NODE_ID;

    doc["ultrasonic"] =
        distance;

    doc["status"] =
        status;


    String payload;

    serializeJson(
        doc,
        payload
    );


    mqttClient.publish(
        SENSOR_TOPIC,
        payload.c_str()
    );


    Serial.println();

    Serial.println(
        "SENSOR DATA PUBLISHED"
    );

    Serial.print(
        "Distance: "
    );

    Serial.print(
        distance
    );

    Serial.println(
        " cm"
    );

    Serial.print(
        "Status: "
    );

    Serial.println(
        status
    );
}


// =====================================================
// PROCESS NODE 2
// =====================================================

void processNode()
{
    float distance =
        readDistance();


    if (distance < 0)
    {
        Serial.println(
            "HC-SR04 reading failed"
        );

        return;
    }


    String status =
        determineStatus(
            distance
        );


    updateLEDs(
        status
    );


    // -------------------------------------------------
    // YELLOW ALERT
    // -------------------------------------------------

    if (
        status == "YELLOW" &&
        !yellowAlertSent
    )
    {
        sendEvent(
            "yellow_alert",
            distance
        );

        yellowAlertSent =
            true;
    }


    // -------------------------------------------------
    // RED / ROVER
    // -------------------------------------------------

    if (
        status == "RED" &&
        !roverCommandSent
    )
    {
        sendRoverCommand(
            distance
        );

        roverCommandSent =
            true;
    }


    // -------------------------------------------------
    // RECOVERY
    // -------------------------------------------------

    if (
        status == "GREEN"
    )
    {
        yellowAlertSent =
            false;

        roverCommandSent =
            false;
    }


    currentStatus =
        status;


    publishSensorData(
        distance,
        status
    );
}


// =====================================================
// SETUP
// =====================================================

void setup()
{
    Serial.begin(
        115200
    );

    delay(1000);


    Serial.println();

    Serial.println(
        "================================"
    );

    Serial.println(
        "SMART MINE SAFETY - NODE 2"
    );

    Serial.println(
        "================================"
    );


    pinMode(
        TRIG_PIN,
        OUTPUT
    );

    pinMode(
        ECHO_PIN,
        INPUT
    );

    pinMode(
        GREEN_LED,
        OUTPUT
    );

    pinMode(
        RED_LED,
        OUTPUT
    );


    digitalWrite(
        GREEN_LED,
        HIGH
    );

    digitalWrite(
        RED_LED,
        LOW
    );


    connectWiFi();


    mqttClient.setServer(
        MQTT_BROKER,
        MQTT_PORT
    );


    connectMQTT();
}


// =====================================================
// LOOP
// =====================================================

void loop()
{
    if (
        WiFi.status() !=
        WL_CONNECTED
    )
    {
        connectWiFi();
    }


    if (
        !mqttClient.connected()
    )
    {
        connectMQTT();
    }


    mqttClient.loop();


    processNode();


    delay(1000);
}