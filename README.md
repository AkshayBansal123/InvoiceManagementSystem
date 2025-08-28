

# 🧾 AI-Powered Invoice Management System

An end-to-end project for **automated invoice processing** with:
- 📄 OCR (Tesseract + OpenCV)  
- 🤖 AI (Hugging Face pipelines for vendor/date/amount extraction & categorization)  
- ⚡ FastAPI backend with SQLite database  
- 🎨 React frontend for uploading & viewing invoices  

---

## 📂 Project Structure
project/
│── backend/
│ ├── main.py
│ ├── invoices.db (auto-created)
│ ├── requirements.txt
│ └── ...
│
│── frontend/
│ ├── src/
│ ├── public/
│ ├── package.json
│ └── ...
│
└── README.md

yaml
Copy code

---

## 🚀 Getting Started

### 🔹 Backend (FastAPI)
1. Navigate to backend:
   ```bash
   cd backend
Create a virtual environment (recommended):

bash
Copy code
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Make sure Tesseract OCR is installed:

Windows: Download here

Linux/macOS:

bash
Copy code
sudo apt-get install tesseract-ocr
Run the backend:

bash
Copy code
uvicorn main:app --reload
→ Runs at http://127.0.0.1:8000

🔹 Frontend (React)
Navigate to frontend:

bash
Copy code
cd frontend
Install dependencies:

bash
Copy code
npm install
Start the frontend:

bash
Copy code
npm start
→ Runs at http://localhost:3000

🌐 API Endpoints
Upload invoice
h
Copy code
POST /upload-invoice/
Uploads an invoice (image/PDF screenshot).

Extracts vendor, date, amount, category.

Stores in SQLite.

Get all invoices
http
Copy code
GET /invoices/
Returns all stored invoices.

Export invoices to CSV
http
Copy code
GET /export-csv/
Exports database records into invoices.csv.


📊 Example Response
{
  "message": "Invoice processed",
  "data": {
    "vendor": "Starbucks",
    "date": "2024-08-22",
    "amount": 12.50,
    "category": "Food"
  }
}
