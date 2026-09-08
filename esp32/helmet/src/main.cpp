/*
 * SMART MINE SAFETY SYSTEM
 * HELMET NODE - ESP8266
 *
 * Function:
 * - Connects to the mine Wi-Fi network
 * - Debounced SOS push button on D1 (GPIO5)
 * - Publishes SOS through MQTT
 * - Re-announces SOS while button is held
 *
 * MQTT:
 *   mine/helmet/HELMET_01/sos
 */


#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>


// =====================================================
// WIFI CONFIGURATION
// =====================================================

// IMPORTANT:
// Helmet and Node 1 must be connected to the same
// network for this MQTT architecture.

const char* WIFI_SSID =
    "YOUR_WIFI_NAME";

const char* WIFI_PASSWORD =
    "YOUR_WIFI_PASSWORD";


// =====================================================
// MQTT CONFIGURATION
// =====================================================

// Master laptop running Mosquitto

const char* MQTT_BROKER =
    "10.214.139.57";

const int MQTT_PORT =
    1883;


// =====================================================
// HELMET IDENTITY
// =====================================================

const char* HELMET_ID =
    "HELMET_01";

const char* WORKER_ID =
    "WORKER_01";


// =====================================================
// MQTT TOPIC
// =====================================================

const char* SOS_TOPIC =
    "mine/helmet/HELMET_01/sos";


// =====================================================
// PIN CONFIGURATION
// DO NOT CHANGE
// =====================================================

const int SOS_PIN =
    D1;       // GPIO5


// =====================================================
// DEBOUNCE / RESEND
// =====================================================

const unsigned long DEBOUNCE_MS =
    50;

const unsigned long RESEND_INTERVAL_MS =
    1000;


// =====================================================
// MQTT
// =====================================================

WiFiClient espClient;

PubSubClient mqttClient(
    espClient
);


// =====================================================
// BUTTON STATE
// =====================================================

int lastRawState =
    HIGH;

int stableState =
    HIGH;

unsigned long lastDebounceTime =
    0;

unsigned long lastSentTime =
    0;

bool sosLatched =
    false;


// =====================================================
// CONNECT TO WIFI
// =====================================================

void connectWiFi()
{
    Serial.println();

    Serial.println(
        "[HELMET] Connecting to WiFi..."
    );

    WiFi.mode(
        WIFI_STA
    );

    WiFi.begin(
        WIFI_SSID,
        WIFI_PASSWORD
    );


    unsigned long start =
        millis();


    while (
        WiFi.status() !=
        WL_CONNECTED
    )
    {
        delay(300);

        Serial.print(".");


        if (
            millis() - start >
            20000
        )
        {
            Serial.println();

            Serial.println(
                "[HELMET] WiFi timeout."
            );

            Serial.println(
                "[HELMET] Retrying..."
            );

            WiFi.disconnect();

            delay(500);

            WiFi.begin(
                WIFI_SSID,
                WIFI_PASSWORD
            );

            start =
                millis();
        }
    }


    Serial.println();

    Serial.println(
        "[HELMET] WiFi connected."
    );


    Serial.print(
        "[HELMET] IP: "
    );

    Serial.println(
        WiFi.localIP()
    );
}


// =====================================================
// CONNECT TO MQTT
// =====================================================

void connectMQTT()
{
    while (
        !mqttClient.connected()
    )
    {
        Serial.println();

        Serial.println(
            "[HELMET] Connecting to MQTT..."
        );


        String clientID =
            String(HELMET_ID) +
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
                "[HELMET] MQTT connected."
            );

            Serial.print(
                "[HELMET] MQTT broker: "
            );

            Serial.print(
                MQTT_BROKER
            );

            Serial.print(
                ":"
            );

            Serial.println(
                MQTT_PORT
            );
        }
        else
        {
            Serial.print(
                "[HELMET] MQTT connection failed. State: "
            );

            Serial.println(
                mqttClient.state()
            );

            delay(2000);
        }
    }
}


// =====================================================
// SEND SOS
// =====================================================

void sendSOS()
{
    JsonDocument doc;


    doc["helmet_id"] =
        HELMET_ID;

    doc["worker_id"] =
        WORKER_ID;

    doc["node_id"] =
        "NODE_1";

    doc["sos"] =
        true;

    doc["timestamp"] =
        millis();


    String payload;


    serializeJson(
        doc,
        payload
    );


    bool published =
        mqttClient.publish(
            SOS_TOPIC,
            payload.c_str()
        );


    if (published)
    {
        Serial.println();

        Serial.println(
            "================================"
        );

        Serial.println(
            "[HELMET] !!! SOS SENT !!!"
        );

        Serial.print(
            "[HELMET] Helmet ID: "
        );

        Serial.println(
            HELMET_ID
        );

        Serial.print(
            "[HELMET] Worker ID: "
        );

        Serial.println(
            WORKER_ID
        );

        Serial.print(
            "[HELMET] Topic: "
        );

        Serial.println(
            SOS_TOPIC
        );

        Serial.print(
            "[HELMET] Payload: "
        );

        Serial.println(
            payload
        );

        Serial.println(
            "================================"
        );
    }
    else
    {
        Serial.println(
            "[HELMET] ERROR: SOS publish failed."
        );
    }
}


// =====================================================
// SETUP
// =====================================================

void setup()
{
    Serial.begin(
        115200
    );

    delay(200);


    Serial.println();

    Serial.println(
        "================================"
    );

    Serial.println(
        "SMART MINE SAFETY SYSTEM"
    );

    Serial.println(
        "HELMET NODE"
    );

    Serial.println(
        "================================"
    );


    // -------------------------------------------------
    // SOS BUTTON
    // -------------------------------------------------

    pinMode(
        SOS_PIN,
        INPUT_PULLUP
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


    mqttClient.setBufferSize(
        512
    );


    connectMQTT();


    Serial.println();

    Serial.println(
        "[HELMET] Ready."
    );

    Serial.println(
        "[HELMET] Press SOS button to send emergency alert."
    );
}


// =====================================================
// LOOP
// =====================================================

void loop()
{
    // -------------------------------------------------
    // WIFI CHECK
    // -------------------------------------------------

    if (
        WiFi.status() !=
        WL_CONNECTED
    )
    {
        connectWiFi();
    }


    // -------------------------------------------------
    // MQTT CHECK
    // -------------------------------------------------

    if (
        !mqttClient.connected()
    )
    {
        connectMQTT();
    }


    mqttClient.loop();


    // -------------------------------------------------
    // READ BUTTON
    // -------------------------------------------------

    int reading =
        digitalRead(
            SOS_PIN
        );


    // -------------------------------------------------
    // DEBOUNCE
    // -------------------------------------------------

    if (
        reading !=
        lastRawState
    )
    {
        lastDebounceTime =
            millis();
    }


    if (
        millis() -
        lastDebounceTime >
        DEBOUNCE_MS
    )
    {
        if (
            reading !=
            stableState
        )
        {
            stableState =
                reading;


            // -----------------------------------------
            // BUTTON PRESSED
            // -----------------------------------------

            if (
                stableState ==
                LOW
            )
            {
                sosLatched =
                    true;


                sendSOS();


                lastSentTime =
                    millis();
            }


            // -----------------------------------------
            // BUTTON RELEASED
            // -----------------------------------------

            else
            {
                sosLatched =
                    false;


                Serial.println(
                    "[HELMET] SOS button released."
                );
            }
        }
    }


    // -------------------------------------------------
    // RESEND WHILE BUTTON HELD
    // -------------------------------------------------

    if (
        sosLatched &&
        millis() -
        lastSentTime >=
        RESEND_INTERVAL_MS
    )
    {
        sendSOS();

        lastSentTime =
            millis();
    }


    lastRawState =
        reading;


    delay(10);
}