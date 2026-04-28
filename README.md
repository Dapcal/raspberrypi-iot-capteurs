# 🌍 Raspberry Pi IoT Monitoring System

## 📌 Description

Ce projet met en place un système IoT permettant de collecter, stocker et transmettre en temps réel des données environnementales depuis un microcontrôleur Arduino vers un Raspberry Pi, puis vers une plateforme cloud.

Les données mesurées sont :

* 🌬️ Oxygène
* 🫁 CO2
* 💧 Humidité
* 🌡️ Température

---

## 🧠 Architecture du systèmeI
Le système suit une architecture IoT en pipeline :

Capteurs → Arduino → Raspberry Pi → SQLite + JSONL → Internet (clé USB) →Cloud (ThingSpeak)

- Acquisition temps réel
- Double stockage (fiabilité)
- Transmission cloud
---

## ⚙️ Technologies utilisées

* Python 3
* Arduino (C/C++)
* SQLite3
* Serial Communication (USB)
* API REST (ThingSpeak)

---

## 🔌 Matériel utilisé

* Raspberry Pi
* Arduino
* Capteur d’oxygène (DFRobot)
* Capteur CO2
* Capteur DHT22 (température & humidité)
* Clé USB 3G/4G (connexion internet)

---

## 📡 Fonctionnement

1. L’Arduino lit les données des capteurs
2. Les données sont envoyées en format JSON via USB
3. Le Raspberry Pi :

   * Lit les données via le port série
   * Les stocke dans une base SQLite
   * Les envoie à ThingSpeak via HTTP

---

## 📂 Structure du projet

```bash
.
├── main.py        # Script principal Python
├── capteurs.db    # Base de données SQLite (générée automatiquement)
└── README.md      # Documentation
```

---

## 🚀 Installation

### 1. Cloner le projet

```bash
git clone https://github.com/Dapcal/raspberrypi-iot-capteurs.git
cd raspberrypi-iot-capteurs
```

---

### 2. Installer les dépendances

```bash
sudo apt update
sudo apt install python3 python3-pip -y
pip3 install pyserial requests
```

---

### 3. Configurer le port série

Modifier dans `main.py` :

```python
SERIAL_PORT = '/dev/ttyACM0'
```

---

## ▶️ Exécution

```bash
python3 arduino_pri.py
```

---

## ⚡ Lancement automatique au démarrage (systemd)

Créer le service :

```bash
sudo nano /etc/systemd/system/capteurs.service
```

Contenu :

```ini
[Unit]
Description=IoT Capteurs Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/raspberrypi-iot-capteurs/arduino_rpi.py
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
```

Activer :

```bash
sudo systemctl daemon-reload
sudo systemctl enable capteurs
sudo systemctl start capteurs
```

---

## 🌐 API utilisée

Les données sont envoyées vers ThingSpeak :

```bash
https://api.thingspeak.com/update?api_key=YOUR_API_KEY
```

---

## 📊 Exemple de données JSON

```json
{
  "oxygene": 20.5,
  "co2": 1400,
  "humidite": 65.2,
  "temperature": 27.3
}
```

---

## ⚠️ Problèmes courants

### Permission série

```bash
sudo usermod -a -G dialout $USER
reboot
```

### Port incorrect

```bash
ls /dev/tty*
```

---

## 🔐 Sécurité

* Ne pas exposer votre API Key publiquement
* Utiliser HTTPS pour les communications
* Restreindre les accès au Raspberry Pi

Ce système présente plusieurs risques :

- Communication série non chiffrée
- Injection de données JSON
- Exposition de la clé API

### Contre-mesures

- Validation stricte des données
- Utilisation de variables d’environnement (.env)
- Restriction des permissions Linux
- Utilisation de HTTPS

---

## 🚀 Améliorations possibles

* Bufferisation des données en cas de perte réseau
* Dashboard local (Grafana)
* Envoi via MQTT
* Multi-capteurs distribués (LoRa)

---


## 👨‍💻 Auteur

Projet réalisé par **Dapoba calixte Igor BICABA**

---

## 📜 Licence

Ce projet est open-source et libre d’utilisation à des fins éducatives.
