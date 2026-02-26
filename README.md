# 🐙 Laughing Octo Funicular

[![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)](.python-version)
[![PHP Version](https://img.shields.io/badge/PHP-7.x-777BB4.svg)](chatBot.php)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 📋 Overview

A powerful automation and control tool for **LDPlayer Android emulator** with both GUI and command-line interfaces. This project enables seamless management of multiple LDPlayer instances, configuration handling, and automated interactions within the Android environment.

## ✨ Key Features

### 🎮 LDPlayer Management
- Start, stop, and control multiple LDPlayer instances
- Instance configuration and monitoring
- Automated emulator interactions

### 🖥️ Dual Interface
- **GUI Mode** (`LD_Player_gui/`): User-friendly graphical interface for easy control
- **CLI Mode** (`LD.py`): Command-line interface for scripting and automation

### ⚙️ Configuration System
- Centralized settings via `config.ini`
- Customizable LDPlayer paths and options
- Persistent data storage (`Data.txt`)

### 🌐 Web Integration
- PHP backend (`server/`) for remote control
- API endpoints for external automation
- Chatbot functionality (`chatBot.php`)

## 🚀 Quick Start

### Prerequisites
- **Python 3.x** ([Download](https://www.python.org/downloads/))
- **LDPlayer** ([Download](https://www.ldplayer.net/))
- **PHP 7.x** (for web features)

### Install

```bash
git clone https://github.com/TinaGrim/laughing-octo-funicular.git
cd laughing-octo-funicular
pip install -r requirements.txt
```

### Configure

Edit `config.ini` and set your LDPlayer installation path:

```ini
[LDPlayer]
path = C:\LDPlayer\LDPlayer9
```

### Run

```bash
python LD.py
```

The GUI window opens and the Flask server starts automatically at `http://127.0.0.1:5000`.

---
## 📁 Project Structure

```
laughing-octo-funicular/
│
├── LD.py                       # 🚀 Entry point — BobPrimeApp (QMainWindow + Flask)
├── config.ini                  # ⚙️  Application settings
├── Data.txt                    # 📊 Generated user/account data
├── requirements.txt            # 📦 Python dependencies
├── chatBot.php                 # 💬 PHP chatbot backend
├── .env                        # 🔑 Tokens (TOKEN1–TOKEN7) — not committed
│
├── LD_Player/                  # Core automation package
│   ├── __init__.py             #    Exports: LDPlayer, option, Activity, Threader
│   ├── Main.py                 #    LDPlayer class — open, stop, resume, process
│   ├── Option.py               #    ADB/Appium helpers, identity generation
│   ├── Drivers.py              #    LDPlayerRemote — automated action sequences
│   └── MyThread.py             #    Threader utility
│
├── LD_Player_gui/              # GUI tab modules (PySide6)
│   ├── Active.py               #    Automation actions configuration
│   ├── Devices.py              #    Emulator instance & hardware settings
│   ├── Manage.py               #    Account/page management
│   └── Auto_Post.py            #    Scheduled posting
│
├── server/                     # Flask web layer
│   ├── server_routes.py        #    Blueprint routes & API logic
│   ├── index.html              #    Dashboard home
│   ├── DevicesList.html        #    Device list view
│   ├── LDActivity.html         #    Activity monitor
│   ├── Order.html              #    Order page
│   └── schedule.html           #    Schedule page
│
├── style/                      # Styling
│   ├── style.qss               #    Qt stylesheet for the desktop GUI
│   ├── style.css               #    Web dashboard CSS
│   └── DevicesList.css         #    Device list page CSS
│
├── Logo/                       # App icons (play, pause, logo, etc.)
└── test/                       # Unit tests
    └── test_proxy.py           #    Proxy & activity tests
```

---
## ⚙️ Configuration

All settings live in `config.ini` and are read/written by the GUI automatically.

```ini
[LDPlayer]
path = C:\LDPlayer\LDPlayer9       # LDPlayer install directory
instances = leidian0, leidian1      # Default instances
auto_start = true

[Devices]
LD_loc = C:\LDPlayer\LDPlayer9     # Also configurable from GUI
number_of_active_ld = 2
wait_after_ld_boot = 30
arangement_count = 3                # Grid columns for window arrangement
cpu_count = 2
hardware_acceleration = true

[Automation]
delay = 2
retry_count = 3

[Server]
port = 8080
debug = false
```

---

**Data.txt Format**
```text
user1,config1,timestamp
user2,config2,timestamp
```
## 💻 Usage

### Programmatic Control

```python
from LD_Player import LDPlayer, option

# List currently running emulators via ADB
running_ids = option.current_ld_ids()
print("Running:", running_ids)       # e.g. [1, 2]

# Get LDPlayer instance names
names = option.current_ld_names()
print("Names:", names)               # e.g. ["LDPlayer-1", "LDPlayer-2"]
```

### Automation Flow (simplified)

```python
from LD_Player import option

bot = option(Number=[1, 2, 3])

# 1. Open emulators
bot.Open_LD()

# 2. Wait for devices to boot
for id in bot.number:
    bot.wait_for_ldplayer_device(id)

# 3. Setup Appium and configure each instance
bot.Full_setup()

# 4. Launch remote drivers for automated actions
bot.Remote_Driver()
```

---
**GUI Mode Shortcuts**
- Ctrl+S: Save configuration
- Ctrl+R: Refresh instances
- F5: Start selected instance
- F6: Stop selected instance
## 🌐 API Endpoints

| Endpoint | Method | Description | Status |
|----------|--------|-------------|--------|
| `/api/instances` | `GET` | 📋 List all running LDPlayer instances | ![Active](https://img.shields.io/badge/status-active-brightgreen) |
| `/api/start/{id}` | `POST` | ▶️ Start a specific LDPlayer instance | ![Active](https://img.shields.io/badge/status-active-brightgreen) |
| `/api/stop/{id}` | `POST` | ⏹️ Stop a specific LDPlayer instance | ![Active](https://img.shields.io/badge/status-active-brightgreen) |
| `/api/restart/{id}` | `POST` | 🔄 Restart a specific LDPlayer instance | ![Beta](https://img.shields.io/badge/status-beta-yellow) |
| `/api/config` | `GET` | ⚙️ Retrieve current configuration | ![Active](https://img.shields.io/badge/status-active-brightgreen) |
| `/api/config` | `POST` | ✏️ Update configuration settings | ![Active](https://img.shields.io/badge/status-active-brightgreen) |
| `/api/automation/run` | `POST` | 🤖 Execute automation script | ![Beta](https://img.shields.io/badge/status-beta-yellow) |
| `/api/data` | `GET` | 📊 Retrieve stored data | ![Active](https://img.shields.io/badge/status-active-brightgreen) |
| `/api/chatbot/message` | `POST` | 💬 Send message to chatbot | ![New](https://img.shields.io/badge/status-new-blue) |
## 📝 Requirements

### Python Packages
- tkinter
- configparser
- requests
- pillow

### System Requirements
- Windows 7/8/10/11
- 4GB RAM minimum
- 500MB free disk space
- LDPlayer installed

## 🔧 Troubleshooting

### Common Issues

**LDPlayer path not found**
- Verify LDPlayer installation
- Check path in `config.ini`
- Use forward slashes or double backslashes

**GUI won't start**
- Install tkinter: `pip install tk`
- Check Python version compatibility

**Permission errors**
- Run as administrator
- Check file permissions for `Data.txt`

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📬 Contact

Project Link: [https://github.com/TinaGrim/laughing-octo-funicular](https://github.com/TinaGrim/laughing-octo-funicular)

---
### Languages

```
Python ███████████████████████░░  91%
PHP    ██░░░░░░░░░░░░░░░░░░░░░░   6%
CSS    █░░░░░░░░░░░░░░░░░░░░░░░   2%
HTML   █░░░░░░░░░░░░░░░░░░░░░░░   1%
```

---

**⭐ Star this repository if you find it useful!**
  
