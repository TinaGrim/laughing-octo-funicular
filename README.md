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

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/TinaGrim/laughing-octo-funicular.git
   cd laughing-octo-funicular
2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
3. **Configure LDPlayer path**
   **Edit config.ini**
   ```bash
   git clone https://github.com/TinaGrim/laughing-octo-funicular.git
   [LDPlayer]
    path = C:\LDPlayer\LDPlayer9
    default_instance = leidian0
4. **Run the application**
   **GUI Mode:**
   ```bash
   python LD_Player_gui/main.py
   ```
   **CLI Mode:**
   ```bash
   python LD.py --help
## 📁 Project Structure
```text
laughing-octo-funicular/
├── 📂 LD_Player_gui/          # GUI application files
│   ├── main.py                 # GUI entry point
│   ├── style/                  # CSS stylesheets
│   └── Logo/                   # Application icons
├── 📂 server/                   # PHP backend
│   ├── index.php                # Main server file
│   └── chatBot.php              # Chatbot integration
├── 📂 test/                      # Test files
├── 🐍 LD.py                       # Core LDPlayer controller
├── ⚙️ config.ini                  # Configuration file
├── 📊 Data.txt                    # User/data storage
├── 📦 requirements.txt            # Python dependencies
├── 🔒 .gitignore                   # Git ignore rules
└── 📜 README.md                   # This file
```
## 🛠️ Configuration Options
**config.ini**
```ini
[LDPlayer]
path = C:\LDPlayer\LDPlayer9
instances = leidian0, leidian1
auto_start = true

[Automation]
delay = 2
retry_count = 3

[Server]
port = 8080
debug = false
```
**Data.txt Format**
```text
user1,config1,timestamp
user2,config2,timestamp
```
## 💻 Usage Examples
**Basic LDPlayer Control**
```python
from LD import LDPlayer

# Initialize controller
ld = LDPlayer(config_path='config.ini')

# Start an instance
ld.start_instance('leidian0')

# List all instances
instances = ld.list_instances()
print(instances)
```
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

**⭐ Star this repository if you find it useful!**
  
