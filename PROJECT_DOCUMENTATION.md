# Documentation complète du projet **Robot Sensor Server**

---

## 1️⃣ Introduction
Ce projet fournit une petite application web basée sur **Flask** et **Flask‑Socket.IO** qui :

* lit les données d’un capteur inertiel **MPU‑6050** (accélération, gyroscope, température) via I²C,
* diffuse ces mesures en temps réel à travers une connexion WebSocket à un navigateur,
* expose une interface HTML/JS simple pour visualiser les données, et
* prépare le terrain pour ajouter ultérieurement des commandes de contrôle (ex. moteurs).

L’ensemble peut être déployé sur un Raspberry Pi (ou tout autre SBC Linux) et est automatisé via le script `deploy.bat` qui copie les fichiers sur le Pi avec **WinSCP**.

---

## 2️⃣ Architecture du code
```
repo/
│
├─ Robot/
│   ├─ __init__.py
│   ├─ server.py          ← serveur Flask + Socket.IO
│   └─ sensors/
│       └─ gyro.py        ← wrapper du MPU‑6050
│
├─ Interface/
│   ├─ templates/
│   │   └─ index.html     ← page HTML affichant les données
│   └─ static/
│       ├─ *.css
│       └─ *.js
│
├─ deploy.bat            ← script de déploiement Windows → Pi
├─ requirements.txt      ← dépendances Python
└─ README.md             ← (cette documentation)
```

* **`Robot/sensors/gyro.py`**
  - Initialise le capteur (`mpu6050`), gère l’absence du matériel avec un warning, expose `get_data()` qui renvoie un dictionnaire ou `None`.  
* **`Robot/server.py`**
  - Crée l’application Flask, initialise Socket.IO, gère les connexions WebSocket.  
  - Pour chaque client, démarre un thread (`_gyro_stream`) qui interroge le capteur à **20 Hz** (`GYRO_SAMPLE_RATE = 0.05 s`) et transmet les données via l’événement `"gyro"`.  
  - Un endpoint `"command"` est prévu pour de futures actions (ex. moteurs).  
* **`Interface/`**
  - Contient les assets front‑end : page HTML (`index.html`), styles CSS, scripts JavaScript qui se connectent à Socket.IO, reçoivent les évènements `"gyro"` et les affichent.  
* **`deploy.bat`**
  - Lit les variables d’environnement depuis `.env`.  
  - Utilise **WinSCP** pour copier les scripts Python, templates et assets vers le répertoire `/home/enzon/` du Pi.

---

## 3️⃣ Prérequis
| Élément | Version minimale | Pourquoi |
|---------|------------------|----------|
| Python | 3.9+ | Compatibilité avec `mpu6050‑python` et `flask‑socketio`. |
| pip | 21.0+ | Gestion des dépendances. |
| Flask | 2.2+ | Serveur web. |
| Flask‑SocketIO | 5.3+ | WebSocket sur Flask. |
| mpu6050‑python | 1.0+ | Interface I²C avec le MPU‑6050. |
| WinSCP (déploiement) | 5.0+ | Copie sécurisée des fichiers depuis Windows. |
| Raspberry Pi (ou autre Linux) | Raspbian Bullseye ou supérieur | Hébergement du serveur. |

---

## 4️⃣ Installation (développement local)
```bash
# 1. Cloner le dépôt
git clone https://github.com/<votre‑organisation>/robot-sensor-server.git
cd robot-sensor-server

# 2. Créer un environnement virtuel
python -m venv .venv
# sous Windows
.venv\Scripts\activate
# sous Linux/macOS
source .venv/bin/activate

# 3. Installer les dépendances
pip install -r requirements.txt
```
> **Astuce** : si vous n’avez pas de capteur MPU‑6050 branché, le module `gyro.py` renvoie `None` et le serveur démarre quand même, ce qui permet de tester l’UI sans matériel.

---

## 5️⃣ Configuration
### 5.1 Variables d’environnement
| Variable | Exemple | Description |
|----------|---------|-------------|
| `HOST` | `0.0.0.0` | Adresse IP sur laquelle le serveur écoute. |
| `PORT` | `5000` | Port TCP du serveur. |
| `GYRO_SAMPLE_RATE` | `0.05` | Intervalle de lecture du capteur (en secondes). |
| `PI_USER`, `PI_PASS`, `PI_IP` | `pi`, `mypassword`, `192.168.1.42` | Utilisées par `deploy.bat` pour le transfert SFTP. |

Ces variables peuvent être placées dans un fichier `.env` à la racine :
```
HOST=0.0.0.0
PORT=5000
GYRO_SAMPLE_RATE=0.05
```
### 5.2 Logs
Le module `logging` est déjà configuré ; vous pouvez ajuster le niveau global via la variable d’environnement `PYTHONLOGLEVEL` (`DEBUG`, `INFO`, `WARNING`, …).

---

## 6️⃣ Lancement de l’application
```bash
# Depuis la racine du projet
python -m Robot.server
```
Le serveur démarre alors sur `http://<IP‑du‑Pi>:5000/`. Ouvrez ce lien dans un navigateur ; vous devriez voir les valeurs du gyroscope qui se mettent à jour toutes les 0,05 s.

---

## 7️⃣ Déploiement sur le Raspberry Pi
1. **Préparez le fichier `.env`** avec les identifiants SFTP.  
2. **Exécutez le script** (à partir d’un terminal Windows) :
```cmd
deploy.bat
```
Le script :
* lit chaque ligne de `.env`,
* se connecte à `sftp://PI_USER:PI_PASS@PI_IP/`,
* transfère `ultrasond.py`, `Robot/server.py`, `Robot/sensors/*.py` ainsi que les dossiers `templates` et `static`.
> **Note** : le script utilise le chemin absolu `C:\raspb\Repo\…`. Si votre dépôt se trouve ailleurs, mettez‑à‑jour les chemins dans `deploy.bat`.

---

## 8️⃣ Extensibilité (prochaines étapes)
| Feature | Description | Implémentation suggérée |
|---------|-------------|------------------------|
| **Contrôle des moteurs** | Recevoir les actions (`forward`, `backward`, etc.) depuis le front‑end et piloter des GPIO | Ajouter une couche `robotics/motor.py` qui expose `set_speed(action, speed)`. Dans `server.py`, décoder le champ `action` et appeler la fonction. |
| **Authentification WebSocket** | Restreindre l’accès aux données du capteur | Utiliser le paramètre `auth` de `@socketio.on('connect')` et vérifier un token JWT. |
| **Tests unitaires** | Vérifier la logique du capteur et du serveur | `pytest` + `pytest‑asyncio`. Mock du capteur avec `unittest.mock`. |
| **Dockerisation** | Simplifier le déploiement sur n’importe quel matériel | Créer un `Dockerfile` qui expose le port 5000, copie le code, installe les dépendances, lance `python -m Robot.server`. |
| **CI/CD** | Lancer les tests et le build à chaque push | GitHub Actions : `python -m pip install -r requirements.txt && pytest`. |
| **Dashboard UI** | Graphiques temps réel (charts) | Intégrer Chart.js ou D3.js dans `index.html` pour afficher l’accélération/gyroscope sous forme de courbes. |

---

## 9️⃣ Bonnes pratiques de développement
* **Séparer la logique matérielle** (capteur, moteurs) du serveur web ; cela facilite le test et la portabilité.
* **Utiliser des variables d’environnement** pour toute configuration sensible (identifiants, ports).
* **Limiter CORS** à l’URL de votre tableau de bord plutôt que `*`.
* **Ne jamais exécuter le serveur en mode `debug` en production**.
* **Versionner le fichier `.env.example`** (sans valeurs réelles) pour guider les nouveaux développeurs.

---

## 🔟 Licence & contributions
* **Licence** : MIT (voir le fichier `LICENSE`).
* **Contributions** :
  1. Fork du dépôt.
  2. Créez une branche `feature/<nom‑feature>` ou `bugfix/<nom‑bug>`.
  3. Testez vos changements (`pytest`).
  4. Ouvrez une pull request décrivant clairement le problème résolu ou la fonctionnalité ajoutée.

---

# 📄 Conversion en PDF
Le fichier `PROJECT_DOCUMENTATION.md` que vous venez de créer peut être converti en PDF avec des outils courants :
```bash
# Exemple avec pandoc (à installer si besoin)
brew install pandoc   # macOS
sudo apt-get install pandoc   # Debian/Ubuntu

pandoc PROJECT_DOCUMENTATION.md -o PROJECT_DOCUMENTATION.pdf
```
Vous pouvez aussi ouvrir le markdown dans VS Code et utiliser l’extension **Markdown PDF** ou copier‑coller le texte dans un traitement de texte (Word, Google Docs) puis exporter en PDF.

---

### 🎯 Résultat
Vous avez maintenant une documentation exhaustive, prête à être partagée et, après conversion, à distribuer sous forme de PDF. N’hésitez pas à me demander d’ajouter une section spécifique ou de détailler un point technique.
