# 🔐 ZapVault

A secure, minimal, and self-destructing file-sharing platform built using Flask. ZapVault lets you upload files that can be downloaded **via a unique link or QR code** — valid only until the expiry time set by the uploader. Ideal for quick, confidential transfers with full control over who downloads and when.

---

## 🚀 Features

- 📁 Upload any file and set an expiry time (1 minute to 1 day)
- 🔗 Get a unique **download link**
- 📱 Auto-generated **QR code** for scanning and sharing
- ⏳ Self-destructing downloads after expiry or multiple downloads
- 📊 Admin dashboard with download analytics
- ✅ Fully **responsive** across devices (desktop, mobile, tablet)
- 🔐 Session-based authentication
- 🌐 Preview-ready via **Ngrok** or deployable to any hosting platform

---

## 📂 Tech Stack

### 🧠 Languages & Runtime
- **Python 3.11+**

### 🧰 Frameworks & Libraries
- **Flask** – lightweight backend framework
- **Werkzeug** – for secure file handling
- **Jinja2** – HTML templating (used via Flask)

### 📦 Python Packages
- `qrcode` – generate scannable QR codes  
- `pytz` – timezone support (UTC ↔ IST)  
- `uuid` – secure random file ID generation  
- `sqlite3` – simple lightweight database  
- `os`, `datetime`, `urllib.parse`, `secrets` – stdlib modules

### 💾 Database
- **SQLite** – used for storing users, file metadata, and download logs

### 🎨 Frontend
- **HTML5**, **CSS3**, **Responsive Web Design**
- **Google Fonts** – Inter, Segoe UI
- **Custom Themed Stylesheets** for:
  - Login/Register
  - Upload Page
  - Success Page
  - Admin Dashboard

### 🧱 Project Structure
ZapVault/
├── run.py
├── zapvault/
│ ├── init.py
│ ├── models/
│ ├── routes/
│ ├── utils/
│ ├── static/
│ │ ├── css/
│ │ └── qrs/
│ └── templates/ (optional if using render_template)
├── uploads/
└── zapvault.db


### 🌍 Deployment & Dev Tools
- **Ngrok** – to expose local server for public access
- **GitHub** – version control and collaboration

---

## 🔧 How to Run Locally

1. **Clone the repository**
   ```bash
   git clone https://github.com/itsprt07/ZapVault.git
   cd ZapVault

2. **Install required packages**
  pip install -r requirements.txt

3. **Run the application**
  python run.py

4. **Expose public URL with Ngrok**
  ngrok http 5000

5. **🔒 Security Notes**
  All download links and QR codes are tokenized and time-bound

  Files are automatically invalidated after expiry

  User sessions are securely managed using Flask sessions

6. **📄 License** 
   MIT License © itsprt07

**🙌 Acknowledgements**
Flask Documentation

Ngrok for seamless local tunneling

QRCode library for Python

Your 💪 relentless motivation 🚀  


