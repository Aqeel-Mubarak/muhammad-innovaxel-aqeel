# muhammad-innovaxel-aqeel
# URL Shortener (Flask + MySQL + Svelte)

A simple URL shortener with a **Flask backend** (MySQL database) and **Svelte frontend**.

---

## **Features**
✅ Shorten long URLs
✅ Retrieve original URL from short code
✅ Update an existing short URL
✅ Delete a short URL
✅ Track access count statistics
✅ Simple Svelte.js frontend

---

## **Tech Stack**
- **Backend:** Flask, MySQL
- **Frontend:** Svelte.js

---

## **1️⃣ Setup Backend (Flask + MySQL)**

### **Install Dependencies**
```bash
cd backend
pip install -r requirements.txt
```

### **Create MySQL Database**
```sql
CREATE DATABASE url_shortener;
USE url_shortener;

CREATE TABLE urls (
    id INT AUTO_INCREMENT PRIMARY KEY,
    url TEXT NOT NULL,
    short_code VARCHAR(10) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    access_count INT DEFAULT 0
);
```

### **Run Flask Server**
```bash
cd backend
python main.py
```
**Backend runs on:** `http://127.0.0.1:5000/`

---

## **2️⃣ Setup Frontend (Svelte.js)**

### **Install Svelte**
```bash
cd frontend
npm install
```


### **Run Svelte Server**
```bash
npm run dev
```
**Frontend runs on:** `http://localhost:5173/`

---
🚀 **Contributions welcome!**

