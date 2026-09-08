#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>


// =====================================================
// WIFI CONFIGURATION
// =====================================================

const char* WIFI_SSID = "YOUR_WIFI_NAME";
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";


// =====================================================
// MQTT CONFIGURATION
// =====================================================

const char* MQTT_BROKER = "10.214.139.57";
const int MQTT_PORT = 1883;

const char* SENSOR_TOPIC = "mine/NODE_1/sensors";
const char* EVENT_TOPIC = "mine/NODE_1/events";

const char* HELMET_SOS_TOPIC =
    "mine/helmet/HELMET_01/sos";


// =====================================================
// NODE CONFIGURATION
// =====================================================

const char* NODE_ID = "NODE_1";


// =====================================================
// PIN CONFIGURATION
// DO NOT CHANGE
// =====================================================

#define MQ2_PIN       34
#define MQ7_PIN       35
#define VIBRATION_PIN 4

#define GREEN_LED     19
#define YELLOW_LED    21
#define RED_LED       22

#define BUZZER        23


// =====================================================
// THRESHOLDS
// =====================================================

#define GAS_ABNORMAL_THRESHOLD 600
#define GAS_CRITICAL_THRESHOLD 1000


// =====================================================
// TIMING
// =====================================================

unsigned long lastSensorPublish = 0;

const unsigned long SENSOR_INTERVAL = 1000;


// =====================================================
// HELMET SOS
// =====================================================

bool helmetSOS = false;
String helmetID = "";

unsigned long helmetSOSStartTime = 0;

const unsigned long HELMET_SOS_TIMEOUT = 15000;


// =====================================================
// MQTT
// =====================================================

WiFiClient espClient;
PubSubClient mqttClient(espClient);


// =====================================================
// CONNECT WIFI
// =====================================================

void connectWiFi()
{
    Serial.println();
    Serial.println("Connecting to WiFi...");

    WiFi.mode(WIFI_STA);

    WiFi.begin(
        WIFI_SSID,
        WIFI_PASSWORD
    );

    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(".");
    }

    Serial.println();
    Serial.println("WiFi connected");

    Serial.print("ESP32 IP: ");
    Serial.println(WiFi.localIP());
}


// =====================================================
// MQTT CALLBACK
// =====================================================

void mqttCallback(
    char* topic,
    byte* payload,
    unsigned int length
)
{
    String message;

    for (unsigned int i = 0; i < length; i++)
    {
        message += (char)payload[i];
    }

    Serial.println();
    Serial.println("MQTT MESSAGE RECEIVED");

    Serial.print("Topic: ");
    Serial.println(topic);

    Serial.print("Payload: ");
    Serial.println(message);


    // -------------------------------------------------
    // HELMET SOS
    // -------------------------------------------------

    if (String(topic) == HELMET_SOS_TOPIC)
    {
        JsonDocument doc;

        DeserializationError error =
            deserializeJson(doc, message);

        if (error)
        {
            Serial.println(
                "Helmet SOS JSON error"
            );

            return;
        }

        helmetSOS = true;

        helmetSOSStartTime = millis();

        if (doc["helmet_id"])
        {
            helmetID =
                doc["helmet_id"].as<String>();
        }
        else
        {
            helmetID = "HELMET_01";
        }

        Serial.println(
            "!!! HELMET SOS ACTIVE !!!"
        );

        Serial.print("Helmet ID: ");
        Serial.println(helmetID);
    }
}


// =====================================================
// CONNECT MQTT
// =====================================================

void connectMQTT()
{
    while (!mqttClient.connected())
    {
        Serial.println(
            "Connecting to MQTT broker..."
        );

        String clientID =
            String(NODE_ID) + "_" +
            String((uint32_t)ESP.getEfuseMac(), HEX);

        if (mqttClient.connect(clientID.c_str()))
        {
            Serial.println(
                "MQTT connected"
            );

            mqttClient.subscribe(
                HELMET_SOS_TOPIC
            );

            Serial.print(
                "Subscribed to: "
            );

            Serial.println(
                HELMET_SOS_TOPIC
            );
        }
        else
        {
            Serial.print(
                "MQTT connection failed, state: "
            );

            Serial.println(
                mqttClient.state()
            );

            delay(2000);
        }
    }
}


// =====================================================
// DETERMINE GAS STATUS
// =====================================================

String getStatusLevel(
    int mq2Value,
    int mq7Value,
    int vibrationValue
)
{
    if (
        mq2Value >= GAS_CRITICAL_THRESHOLD ||
        mq7Value >= GAS_CRITICAL_THRESHOLD ||
        vibrationValue == HIGH ||
        helmetSOS
    )
    {
        return "CRITICAL";
    }

    if (
        mq2Value >= GAS_ABNORMAL_THRESHOLD ||
        mq7Value >= GAS_ABNORMAL_THRESHOLD
    )
    {
        return "ABNORMAL";
    }

    return "NORMAL";
}


// =====================================================
// LED + BUZZER CONTROL
// =====================================================

void updateIndicators(
    const String& statusLevel
)
{
    digitalWrite(
        GREEN_LED,
        LOW
    );

    digitalWrite(
        YELLOW_LED,
        LOW
    );

    digitalWrite(
        RED_LED,
        LOW
    );


    if (statusLevel == "NORMAL")
    {
        digitalWrite(
            GREEN_LED,
            HIGH
        );

        digitalWrite(
            BUZZER,
            LOW
        );
    }

    else if (statusLevel == "ABNORMAL")
    {
        digitalWrite(
            YELLOW_LED,
            HIGH
        );

        unsigned long currentMillis =
            millis();

        if (
            (currentMillis / 500) % 2 == 0
        )
        {
            digitalWrite(
                BUZZER,
                HIGH
            );
        }
        else
        {
            digitalWrite(
                BUZZER,
                LOW
            );
        }
    }

    else
    {
        digitalWrite(
            RED_LED,
            HIGH
        );

        unsigned long currentMillis =
            millis();

        if (
            (currentMillis / 100) % 2 == 0
        )
        {
            digitalWrite(
                BUZZER,
                HIGH
            );
        }
        else
        {
            digitalWrite(
                BUZZER,
                LOW
            );
        }
    }
}


// =====================================================
// PUBLISH SENSOR DATA
// =====================================================

void publishSensorData()
{
    int mq2Value =
        analogRead(MQ2_PIN);

    int mq7Value =
        analogRead(MQ7_PIN);

    int vibrationValue =
        digitalRead(VIBRATION_PIN);


    String statusLevel =
        getStatusLevel(
            mq2Value,
            mq7Value,
            vibrationValue
        );


    updateIndicators(
        statusLevel
    );


    // -------------------------------------------------
    // JSON
    // -------------------------------------------------

    JsonDocument doc;

    doc["node_id"] =
        NODE_ID;

    doc["mq2"] =
        mq2Value;

    doc["mq7"] =
        mq7Value;

    doc["vibration"] =
        vibrationValue;

    doc["status"] =
        statusLevel;


    // Helmet information

    doc["helmet_sos"] =
        helmetSOS;

    doc["helmet_id"] =
        helmetID;


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
        "MQ2: "
    );

    Serial.println(
        mq2Value
    );

    Serial.print(
        "MQ7: "
    );

    Serial.println(
        mq7Value
    );

    Serial.print(
        "Vibration: "
    );

    Serial.println(
        vibrationValue
    );

    Serial.print(
        "Status: "
    );

    Serial.println(
        statusLevel
    );
}


// =====================================================
// HELMET SOS TIMEOUT
// =====================================================

void checkHelmetSOS()
{
    if (!helmetSOS)
    {
        return;
    }

    if (
        millis() -
        helmetSOSStartTime >=
        HELMET_SOS_TIMEOUT
    )
    {
        helmetSOS = false;

        helmetID = "";

        Serial.println(
            "Helmet SOS cleared"
        );
    }
}


// =====================================================
// SETUP
// =====================================================

void setup()
{
    Serial.begin(115200);

    delay(1000);

    Serial.println();
    Serial.println(
        "================================"
    );

    Serial.println(
        "SMART MINE SAFETY - NODE 1"
    );

    Serial.println(
        "================================"
    );


    // -------------------------------------------------
    // PIN MODE
    // -------------------------------------------------

    pinMode(
        MQ2_PIN,
        INPUT
    );

    pinMode(
        MQ7_PIN,
        INPUT
    );

    pinMode(
        VIBRATION_PIN,
        INPUT
    );


    pinMode(
        GREEN_LED,
        OUTPUT
    );

    pinMode(
        YELLOW_LED,
        OUTPUT
    );

    pinMode(
        RED_LED,
        OUTPUT
    );

    pinMode(
        BUZZER,
        OUTPUT
    );


    // -------------------------------------------------
    // INITIAL STATE
    // -------------------------------------------------

    digitalWrite(
        GREEN_LED,
        HIGH
    );

    digitalWrite(
        YELLOW_LED,
        LOW
    );

    digitalWrite(
        RED_LED,
        LOW
    );

    digitalWrite(
        BUZZER,
        LOW
    );


    // -------------------------------------------------
    // WIFI
    // -------------------------------------------------

    connectWiFi();


    // -------------------------------------------------
    // MQTT
    // -------------------------------------------------

    mqttClient.setServer(
        MQTT_BROKER,
        MQTT_PORT
    );

    mqttClient.setCallback(
        mqttCallback
    );

    mqttClient.setBufferSize(
        1024
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


    checkHelmetSOS();


    // -------------------------------------------------
    // SENSOR PUBLISH
    // -------------------------------------------------

    if (
        millis() -
        lastSensorPublish >=
        SENSOR_INTERVAL
    )
    {
        lastSensorPublish =
            millis();

        publishSensorData();
    }


    delay(10);
}