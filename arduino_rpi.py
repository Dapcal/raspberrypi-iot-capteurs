import serial
import json
import time
import sqlite3
import requests

# CONFIG
SERIAL_PORT = 'COM12' #'/dev/ttyUSB0'
BAUDRATE = 9600

API_KEY = "3038BJIQXJK2JR8M"
THINGSPEAK_URL = "https://api.thingspeak.com/update"

# Base de données
conn = sqlite3.connect('capteurs.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS mesures (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    oxygene REAL,
    co2 REAL,
    humidite REAL,
    temperature REAL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

conn.commit()

# Connexion série
ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)
time.sleep(2)

print("Lecture des données...")

while True:
    try:
        line = ser.readline().decode('utf-8').strip()

        if line:
            print("Reçu:", line)

            data = json.loads(line)

            oxygene = data["oxygene"]
            co2 = data["co2"]
            humidite = data["humidite"]
            temperature = data["temperature"]

            # 1. Sauvegarde DB
            cursor.execute('''
                INSERT INTO mesures (oxygene, co2, humidite, temperature)
                VALUES (?, ?, ?, ?)
            ''', (oxygene, co2, humidite, temperature))
            conn.commit()

            print("Données enregistrées")

            # 2. Envoi API
            params = {
                "api_key": API_KEY,
                "field1": oxygene,
                "field2": co2,
                "field3": humidite,
                "field4": temperature
            }

            response = requests.get(THINGSPEAK_URL, params=params)

            print("Envoyé à ThingSpeak:", response.status_code)

    except Exception as e:
        print("Erreur:", e)

    time.sleep(5)