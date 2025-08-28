




# from fastapi import FastAPI, UploadFile, File
# from fastapi.middleware.cors import CORSMiddleware
# import pytesseract
# from PIL import Image
# import re
# import io
# import sqlite3
# import csv
# import cv2
# import numpy as np

# app = FastAPI()

# # Allow React frontend
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# DB_FILE = "invoices.db"

# # Create DB if not exists
# def init_db():
#     conn = sqlite3.connect(DB_FILE)
#     c = conn.cursor()
#     c.execute('''CREATE TABLE IF NOT EXISTS invoices
#                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
#                   vendor TEXT,
#                   date TEXT,
#                   amount REAL,
#                   category TEXT)''')
#     conn.commit()
#     conn.close()

# init_db()

# # --- STEP 1: Preprocess invoice image ---
# def preprocess_image(image_bytes):
#     nparr = np.frombuffer(image_bytes, np.uint8)
#     img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

#     # Convert to grayscale
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#     # Thresholding (binarization)
#     _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

#     # Denoise (reduce speckles)
#     denoised = cv2.medianBlur(thresh, 3)

#     return denoised

# # --- STEP 2: Smarter regex extraction ---
# def parse_invoice_text(text: str):
#     # Vendor: look for "Vendor" or fallback to first word
#     vendor = re.search(r"(Vendor|From)[:\- ]+([A-Za-z0-9 &]+)", text, re.IGNORECASE)

#     # Dates: flexible formats like 12/05/2023 or 2023-05-12
#     date = re.search(r"(\d{2}[\/\-]\d{2}[\/\-]\d{4})", text)

#     # Amount: match "Amount Due", "Total Due", "Grand Total"
#     amount = re.search(
#     r"(Amounts Due|Amount Due|Total Due|Grand Total|Total)\s*[:\-]?\s*\$?(\d+(?:\.\d{2})?)",
#     text,
#     re.IGNORECASE
# )
   
#     return {
#         "vendor": vendor.group(2) if vendor else "Unknown",
#         "date": date.group(1) if date else "Unknown",
#         "amount": float(amount.group(2)) if amount else 0.0,
#         "category": "Uncategorized"  # TODO: later use AI/NLP for categories
#     }

# @app.post("/upload-invoice/")
# async def upload_invoice(file: UploadFile = File(...)):
#     # Preprocess image
#     image_bytes = await file.read()
#     processed_img = preprocess_image(image_bytes)

#     # OCR with Tesseract
#     text = pytesseract.image_to_string(processed_img, config="--oem 3 --psm 6")
#     data = parse_invoice_text(text)

#     # Save to DB
#     conn = sqlite3.connect(DB_FILE)
#     c = conn.cursor()
#     c.execute("INSERT INTO invoices (vendor,date,amount,category) VALUES (?,?,?,?)",
#               (data["vendor"], data["date"], data["amount"], data["category"]))
#     conn.commit()
#     conn.close()

#     return {"message": "Invoice processed", "data": data}

# @app.get("/invoices/")
# def get_invoices():
#     conn = sqlite3.connect(DB_FILE)
#     c = conn.cursor()
#     c.execute("SELECT * FROM invoices")
#     rows = c.fetchall()
#     conn.close()
#     return {"invoices": rows}

# @app.get("/export-csv/")
# def export_csv():
#     conn = sqlite3.connect(DB_FILE)
#     c = conn.cursor()
#     c.execute("SELECT * FROM invoices")
#     rows = c.fetchall()
#     conn.close()

#     with open("invoices.csv", "w", newline="") as f:
#         writer = csv.writer(f)
#         writer.writerow(["ID", "Vendor", "Date", "Amount", "Category"])
#         writer.writerows(rows)

#     return {"message": "Exported to invoices.csv"}





# from fastapi import FastAPI, UploadFile, File
# from fastapi.middleware.cors import CORSMiddleware
# import pytesseract
# from PIL import Image
# import re
# import sqlite3
# import csv
# import cv2
# import numpy as np
# import re

# app = FastAPI()

# # Allow React frontend
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# DB_FILE = "invoices.db"

# # Create DB if not exists
# def init_db():
#     conn = sqlite3.connect(DB_FILE)
#     c = conn.cursor()
#     c.execute('''CREATE TABLE IF NOT EXISTS invoices
#                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
#                   vendor TEXT,
#                   date TEXT,
#                   amount REAL,
#                   category TEXT)''')
#     conn.commit()
#     conn.close()

# init_db()

# # --- STEP 1: Preprocess invoice image ---
# def preprocess_image(image_bytes):
#     nparr = np.frombuffer(image_bytes, np.uint8)
#     img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

#     # Convert to grayscale
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#     # Thresholding (binarization)
#     _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

#     # Denoise (reduce speckles)
#     denoised = cv2.medianBlur(thresh, 3)

#     return denoised

# # --- STEP 2: Smarter token-based extraction ---
# def parse_invoice_text(text: str):
#     words = text.split()
#     n = len(words)

#     vendor, date, amount = "Unknown", "Unknown", 0.0

#     for i, word in enumerate(words):
#         # --- Vendor ---
#         if word.lower() in ["vendor", "from", "supplier", "billed", "seller"]:
#             if i + 1 < n and words[i+1].strip():
#                 vendor = words[i+1]

#         # --- Date ---
#         if "date" in word.lower():
#             if i + 1 < n and re.match(r"\d{2}[\/\-]\d{2}[\/\-]\d{4}", words[i+1]):
#                 date = words[i+1]

#         # --- Amount ---
#         if word.lower() in ["total", "amount", "due", "grand", "balance", "payable"]:
#             candidates = []
#             for j in range(1, 6):
#                 if i+j < n:
#                     token = words[i+j].replace("$", "").replace(",", "")
                    
#                     # If OCR split 700 and .00 into two tokens
#                     if re.match(r"^\d+$", token) and (i+j+1 < n and re.match(r"^\.\d{2}$", words[i+j+1])):
#                         token = token + words[i+j+1]  # merge into 700.00
                    
#                     if re.match(r"^\d+(\.\d{2})?$", token):
#                         candidates.append(float(token))
            
#             # Pick the largest number (usually the invoice total)
#             if candidates:
#                 amount = max(candidates)
#                 break

#     return {
#         "vendor": vendor,
#         "date": date,
#         "amount": amount,
#         "category": "Uncategorized"  # later: AI categorization
#     }

            

#     return {
#         "vendor": vendor,
#         "date": date,
#         "amount": amount,
#         "category": "Uncategorized"  # later: AI categorization
#     }

# # --- STEP 3: API Endpoints ---
# @app.post("/upload-invoice/")
# async def upload_invoice(file: UploadFile = File(...)):
#     # Preprocess image
#     image_bytes = await file.read()
#     processed_img = preprocess_image(image_bytes)

#     # OCR with Tesseract
#     text = pytesseract.image_to_string(processed_img, config="--oem 3 --psm 6")
#     data = parse_invoice_text(text)

#     # Save to DB
#     conn = sqlite3.connect(DB_FILE)
#     c = conn.cursor()
#     c.execute("INSERT INTO invoices (vendor,date,amount,category) VALUES (?,?,?,?)",
#               (data["vendor"], data["date"], data["amount"], data["category"]))
#     conn.commit()
#     conn.close()

#     return {"message": "Invoice processed", "data": data}

# @app.get("/invoices/")
# def get_invoices():
#     conn = sqlite3.connect(DB_FILE)
#     c = conn.cursor()
#     c.execute("SELECT * FROM invoices")
#     rows = c.fetchall()
#     conn.close()
#     return {"invoices": rows}

# @app.get("/export-csv/")
# def export_csv():
#     conn = sqlite3.connect(DB_FILE)
#     c = conn.cursor()
#     c.execute("SELECT * FROM invoices")
#     rows = c.fetchall()
#     conn.close()

#     with open("invoices.csv", "w", newline="") as f:
#         writer = csv.writer(f)
#         writer.writerow(["ID", "Vendor", "Date", "Amount", "Category"])
#         writer.writerows(rows)

#     return {"message": "Exported to invoices.csv"}





# from fastapi import FastAPI, UploadFile, File
# from fastapi.middleware.cors import CORSMiddleware
# import pytesseract
# from PIL import Image
# import sqlite3
# import csv
# import cv2
# import numpy as np
# import re
# from io import BytesIO

# # Hugging Face
# from transformers import pipeline

# app = FastAPI()

# # Allow React frontend
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# DB_FILE = "invoices.db"

# # Create DB if not exists
# def init_db():
#     conn = sqlite3.connect(DB_FILE)
#     c = conn.cursor()
#     c.execute('''CREATE TABLE IF NOT EXISTS invoices
#                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
#                   vendor TEXT,
#                   date TEXT,
#                   amount REAL,
#                   category TEXT)''')
#     conn.commit()
#     conn.close()

# init_db()

# # --- STEP 1: Preprocess invoice image ---
# def preprocess_image(image_bytes):
#     nparr = np.frombuffer(image_bytes, np.uint8)
#     img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

#     # Convert to grayscale
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#     # Thresholding (binarization)
#     _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

#     # Denoise (reduce speckles)
#     denoised = cv2.medianBlur(thresh, 3)

#     return denoised

# # --- STEP 2: Hugging Face NER extraction ---
# ner_pipeline = pipeline("ner", model="dslim/bert-base-NER", grouped_entities=True)

# def parse_invoice_text_with_hf(text: str):
#     entities = ner_pipeline(text)

#     vendor, date, amount = "Unknown", "Unknown", 0.0

#     # Use Hugging Face NER
#     for ent in entities:
#         label = ent["entity_group"]
#         value = ent["word"]

#         if label == "ORG" and vendor == "Unknown":
#             vendor = value
#         elif label == "DATE" and date == "Unknown":
#             date = value
#         elif label in ["MONEY", "CARDINAL"]:
#             cleaned = value.replace("$", "").replace(",", "")
#             if re.match(r"^\d+(\.\d+)?$", cleaned):
#                 num = float(cleaned)
#                 if num > amount:
#                     amount = num

#     # --- Regex fallback ---
#     if vendor == "Unknown":
#         match = re.search(r"(Vendor|From|Supplier|Billed|Seller)[:\s]+([A-Za-z0-9&\.\- ]+)", text, re.IGNORECASE)
#         if match:
#             vendor = match.group(2).strip()

#     if date == "Unknown":
#         match = re.search(r"\b\d{2}[\/\-]\d{2}[\/\-]\d{4}\b", text)  # e.g. 12/05/2025
#         if match:
#             date = match.group(0)

#     if amount == 0.0:
#         match = re.findall(r"\d+\.\d{2}", text)  # find all decimal numbers
#         if match:
#             amount = max(map(float, match))  # assume largest is total

#     return {
#         "vendor": vendor,
#         "date": date,
#         "amount": amount,
#         "category": "Uncategorized"  # later: AI categorization
#     }

# # --- STEP 3: API Endpoints ---
# @app.post("/upload-invoice/")
# async def upload_invoice(file: UploadFile = File(...)):
#     # Preprocess image
#     image_bytes = await file.read()
#     processed_img = preprocess_image(image_bytes)

#     # OCR with Tesseract
#     text = pytesseract.image_to_string(processed_img, config="--oem 3 --psm 6")

#     # Hugging Face + Regex parsing
#     data = parse_invoice_text_with_hf(text)

#     # Save to DB
#     conn = sqlite3.connect(DB_FILE)
#     c = conn.cursor()
#     c.execute("INSERT INTO invoices (vendor,date,amount,category) VALUES (?,?,?,?)",
#               (data["vendor"], data["date"], data["amount"], data["category"]))
#     conn.commit()
#     conn.close()

#     return {"message": "Invoice processed", "data": data}

# @app.get("/invoices/")
# def get_invoices():
#     conn = sqlite3.connect(DB_FILE)
#     c = conn.cursor()
#     c.execute("SELECT * FROM invoices")
#     rows = c.fetchall()
#     conn.close()
#     return {"invoices": rows}

# @app.get("/export-csv/")
# def export_csv():
#     conn = sqlite3.connect(DB_FILE)
#     c = conn.cursor()
#     c.execute("SELECT * FROM invoices")
#     rows = c.fetchall()
#     conn.close()

#     with open("invoices.csv", "w", newline="") as f:
#         writer = csv.writer(f)
#         writer.writerow(["ID", "Vendor", "Date", "Amount", "Category"])
#         writer.writerows(rows)

#     return {"message": "Exported to invoices.csv"}










# from fastapi import FastAPI, UploadFile, File
# from fastapi.middleware.cors import CORSMiddleware
# import pytesseract
# from PIL import Image
# import sqlite3
# import csv
# import cv2
# import numpy as np
# import re
# from io import BytesIO
# from transformers import pipeline

# app = FastAPI()

# # Allow React frontend
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# DB_FILE = "invoices.db"

# # Create DB if not exists
# def init_db():
#     conn = sqlite3.connect(DB_FILE)
#     c = conn.cursor()
#     c.execute('''CREATE TABLE IF NOT EXISTS invoices
#                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
#                   vendor TEXT,
#                   date TEXT,
#                   amount REAL,
#                   category TEXT)''')
#     conn.commit()
#     conn.close()

# init_db()

# # --- STEP 1: Preprocess invoice image ---
# def preprocess_image(image_bytes):
#     nparr = np.frombuffer(image_bytes, np.uint8)
#     img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
#     denoised = cv2.medianBlur(thresh, 3)
#     return denoised

# # --- STEP 2: Hugging Face Invoice QA model ---
# invoice_qa = pipeline(
#     "document-question-answering",
#      model="impira/layoutlm-invoices"
# )

# # --- FIXED: Flexible amount extractor ---
# def extract_amount(text):
#     if not text:
#         return 0.0
#     # Keep only digits, commas, periods
#     cleaned = re.sub(r"[^\d.,]", " ", text)
#     cleaned = cleaned.replace(",", "")  # remove 3,450 → 3450
#     matches = re.findall(r"\d+(?:\.\d+)?", cleaned)

#     if not matches:
#         return 0.0

#     numbers = [float(m) for m in matches]
#     return max(numbers)  # pick the largest (likely total)

# def parse_invoice_text_with_hf(image):
#     vendor, date, amount = "Unknown", "Unknown", 0.0

#     # Ask questions to the model
#     vendor_ans = invoice_qa(image=image, question="Who is the vendor?")
#     date_ans = invoice_qa(image=image, question="What is the invoice date?")
#     amount_ans = invoice_qa(image=image, question="What is the total amount?")

#     if vendor_ans and len(vendor_ans) > 0:
#         vendor = vendor_ans[0]["answer"]

#     if date_ans and len(date_ans) > 0:
#         date = date_ans[0]["answer"]

#     if amount_ans and len(amount_ans) > 0:
#         amount = extract_amount(amount_ans[0]["answer"])

#     return {
#         "vendor": vendor,
#         "date": date,
#         "amount": amount,
#         "category": "Uncategorized"
#     }

# # --- STEP 3: API Endpoints ---
# @app.post("/upload-invoice/")
# async def upload_invoice(file: UploadFile = File(...)):
#     image_bytes = await file.read()
#     processed_img = preprocess_image(image_bytes)

#     # OCR text (fallback)
#     text = pytesseract.image_to_string(processed_img, config="--oem 3 --psm 6")

#     # Run invoice model
#     img = Image.open(BytesIO(image_bytes))
#     data = parse_invoice_text_with_hf(img)

#     # Save to DB
#     conn = sqlite3.connect(DB_FILE)
#     c = conn.cursor()
#     c.execute("INSERT INTO invoices (vendor,date,amount,category) VALUES (?,?,?,?)",
#               (data["vendor"], data["date"], data["amount"], data["category"]))
#     conn.commit()
#     conn.close()

#     return {"message": "Invoice processed", "data": data}

# @app.get("/invoices/")
# def get_invoices():
#     conn = sqlite3.connect(DB_FILE)
#     c = conn.cursor()
#     c.execute("SELECT * FROM invoices")
#     rows = c.fetchall()
#     conn.close()
#     return {"invoices": rows}

# @app.get("/export-csv/")
# def export_csv():
#     conn = sqlite3.connect(DB_FILE)
#     c = conn.cursor()
#     c.execute("SELECT * FROM invoices")
#     rows = c.fetchall()
#     conn.close()

#     with open("invoices.csv", "w", newline="") as f:
#         writer = csv.writer(f)
#         writer.writerow(["ID", "Vendor", "Date", "Amount", "Category"])
#         writer.writerows(rows)

#     return {"message": "Exported to invoices.csv"}





# from fastapi import FastAPI, UploadFile, File
# from fastapi.middleware.cors import CORSMiddleware
# import pytesseract
# from PIL import Image
# import sqlite3
# import csv
# import cv2
# import numpy as np
# import re
# from io import BytesIO
# from transformers import pipeline

# app = FastAPI()

# # Allow React frontend
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# DB_FILE = "invoices.db"

# # Create DB if not exists
# def init_db():
#     conn = sqlite3.connect(DB_FILE)
#     c = conn.cursor()
#     c.execute('''CREATE TABLE IF NOT EXISTS invoices
#                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
#                   vendor TEXT,
#                   date TEXT,
#                   amount REAL,
#                   category TEXT)''')
#     conn.commit()
#     conn.close()

# init_db()

# # --- STEP 1: Preprocess invoice image ---
# def preprocess_image(image_bytes):
#     nparr = np.frombuffer(image_bytes, np.uint8)
#     img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
#     denoised = cv2.medianBlur(thresh, 3)
#     return denoised

# # --- STEP 2: Hugging Face Invoice QA model ---
# invoice_qa = pipeline(
#     "document-question-answering",
#     model="impira/layoutlm-invoices"
# )

# # Hugging Face NER for item extraction
# ner_pipeline = pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")

# # --- STEP 3: Category mapping ---
# VENDOR_CATEGORY_MAP = {
#     "Uber": "Transport",
#     "Lyft": "Transport",
#     "Adobe": "Software",
#     "Microsoft": "Software",
#     "Amazon": "Supplies",
#     "Walmart": "Supplies",
#     "Starbucks": "Food",
#     "McDonalds": "Food",
#     "Dominos": "Food",
#     "Dropbox": "Software",
#     "Google": "Software"
# }

# ITEM_KEYWORDS = {
#     "subscription": "Software",
#     "license": "Software",
#     "hosting": "Software",
#     "cloud": "Software",
#     "Software Development":"Software",
#     "coffee": "Food",
#     "burger": "Food",
#     "pizza": "Food",
#     "ride": "Transport",
#     "taxi": "Transport",
#     "fuel": "Transport",
#     "notebook": "Supplies",
#     "pen": "Supplies",
#     "paper": "Supplies"
# }

# # --- Flexible amount extractor ---
# def extract_amount(text):
#     if not text:
#         return 0.0
#     cleaned = re.sub(r"[^\d.,]", " ", text)
#     cleaned = cleaned.replace(",", "")
#     matches = re.findall(r"\d+(?:\.\d+)?", cleaned)
#     if not matches:
#         return 0.0
#     numbers = [float(m) for m in matches]
#     return max(numbers)

# # --- Category detection ---
# def categorize_invoice(vendor, ocr_text):
#     # Vendor-based categorization
#     for known_vendor, category in VENDOR_CATEGORY_MAP.items():
#         if known_vendor.lower() in vendor.lower():
#             return category

#     # Item-based categorization (NER + keywords)
#     entities = ner_pipeline(ocr_text)
#     for ent in entities:
#         word = ent["word"].lower()
#         for keyword, category in ITEM_KEYWORDS.items():
#             if keyword in word:
#                 return category

#     # Default
#     return "Uncategorized"

# # --- Invoice parser ---
# def parse_invoice_text_with_hf(image, ocr_text):
#     vendor, date, amount = "Unknown", "Unknown", 0.0

#     vendor_ans = invoice_qa(image=image, question="Who is the vendor?")
#     date_ans = invoice_qa(image=image, question="What is the invoice date?")
#     amount_ans = invoice_qa(image=image, question="What is the total amount?")

#     if vendor_ans and len(vendor_ans) > 0:
#         vendor = vendor_ans[0]["answer"]

#     if date_ans and len(date_ans) > 0:
#         date = date_ans[0]["answer"]

#     if amount_ans and len(amount_ans) > 0:
#         amount = extract_amount(amount_ans[0]["answer"])

#     # Auto categorization
#     category = categorize_invoice(vendor, ocr_text)

#     return {
#         "vendor": vendor,
#         "date": date,
#         "amount": amount,
#         "category": category
#     }

# # --- API Endpoints ---
# @app.post("/upload-invoice/")
# async def upload_invoice(file: UploadFile = File(...)):
#     image_bytes = await file.read()
#     processed_img = preprocess_image(image_bytes)

#     # OCR fallback text
#     ocr_text = pytesseract.image_to_string(processed_img, config="--oem 3 --psm 6")

#     # Run invoice model
#     img = Image.open(BytesIO(image_bytes))
#     data = parse_invoice_text_with_hf(img, ocr_text)

#     # Save to DB
#     conn = sqlite3.connect(DB_FILE)
#     c = conn.cursor()
#     c.execute("INSERT INTO invoices (vendor,date,amount,category) VALUES (?,?,?,?)",
#               (data["vendor"], data["date"], data["amount"], data["category"]))
#     conn.commit()
#     conn.close()

#     return {"message": "Invoice processed", "data": data}

# @app.get("/invoices/")
# def get_invoices():
#     conn = sqlite3.connect(DB_FILE)
#     c = conn.cursor()
#     c.execute("SELECT * FROM invoices")
#     rows = c.fetchall()
#     conn.close()
#     return {"invoices": rows}

# @app.get("/export-csv/")
# def export_csv():
#     conn = sqlite3.connect(DB_FILE)
#     c = conn.cursor()
#     c.execute("SELECT * FROM invoices")
#     rows = c.fetchall()
#     conn.close()

#     with open("invoices.csv", "w", newline="") as f:
#         writer = csv.writer(f)
#         writer.writerow(["ID", "Vendor", "Date", "Amount", "Category"])
#         writer.writerows(rows)

#     return {"message": "Exported to invoices.csv"}










from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pytesseract
from PIL import Image
import sqlite3
import csv
import cv2
import numpy as np
import re
from io import BytesIO
from transformers import pipeline
from difflib import get_close_matches
import os

app = FastAPI()

# CORS (React etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- DB ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "invoices.db")

def get_conn():
    # Slightly more robust SQLite config
    conn = sqlite3.connect(DB_FILE, timeout=10)
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS invoices
           (id INTEGER PRIMARY KEY AUTOINCREMENT,
            vendor TEXT,
            date TEXT,
            amount REAL,
            category TEXT)"""
    )
    conn.commit()
    conn.close()

init_db()

# ---------- Image Preprocessing ----------
def preprocess_image(image_bytes):
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # adaptive threshold is often better across varying backgrounds
    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 10
    )
    denoised = cv2.medianBlur(thresh, 3)
    return denoised

# ---------- Hugging Face Pipelines ----------
# Doc-QA model (invoice-oriented)
invoice_qa = pipeline("document-question-answering", model="impira/layoutlm-invoices")

# Zero-shot classifier for category fallback
zero_shot = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# ---------- Categorization Data ----------
VENDOR_CATEGORY_MAP = {
    "Uber": "Transport",
    "Lyft": "Transport",
    "Ola": "Transport",
    "Adobe": "Software",
    "Microsoft": "Software",
    "Google": "Software",
    "Dropbox": "Software",
    "Amazon": "Supplies",
    "Amazon.com": "Supplies",
    "Walmart": "Supplies",
    "Starbucks": "Food",
    "Starbucks Coffee": "Food",
    "McDonalds": "Food",
    "Dominos": "Food",
    "Swiggy": "Food",
    "Zomato": "Food",
}

ITEM_KEYWORDS = {
    # software / cloud
    r"\b(subscription|license|saas|hosting|cloud|compute|storage)\b": "Software",
    # food
    r"\b(coffee|latte|burger|pizza|meal|lunch|dinner|beverage)\b": "Food",
    # transport
    r"\b(ride|taxi|cab|trip|fare|fuel|toll|parking)\b": "Transport",
    # supplies
    r"\b(notebook|pen|paper|staples|stationery|marker|printer|toner)\b": "Supplies",
}

ZERO_SHOT_LABELS = ["Food", "Transport", "Software", "Supplies", "Other"]

# ---------- Helpers ----------
def extract_amount(text: str) -> float:
    """Extract the most likely total from a text span."""
    if not text:
        return 0.0
    t = re.sub(r"[^\d.,\-]", " ", text)         # keep digits, signs, separators
    t = t.replace(",", "")                      # normalize thousand separators
    # capture numbers like 123, -123, 123.45, -123.45
    matches = re.findall(r"-?\d+(?:\.\d+)?", t)
    if not matches:
        return 0.0
    # some totals appear multiple times; pick largest absolute positive
    nums = [abs(float(m)) for m in matches]
    return max(nums) if nums else 0.0

def fuzzy_vendor_match(vendor: str):
    """Return category via fuzzy match against known vendors."""
    if not vendor or vendor == "Unknown":
        return None
    vendor_clean = vendor.lower().strip()
    known_names = [v.lower() for v in VENDOR_CATEGORY_MAP.keys()]
    best = get_close_matches(vendor_clean, known_names, n=1, cutoff=0.6)
    if not best:
        # also try partial tokens (e.g., "Starbucks Coffee" → "Starbucks")
        tokens = [tok for tok in re.split(r"[^a-z0-9]+", vendor_clean) if tok]
        for t in tokens:
            best = get_close_matches(t, known_names, n=1, cutoff=0.8)
            if best:
                break
    if best:
        # map back to original key to fetch category
        for k, v in VENDOR_CATEGORY_MAP.items():
            if k.lower() == best[0]:
                return v
    return None

def regex_keyword_category(ocr_text: str):
    """Return first category whose regex is found in OCR text."""
    text = (ocr_text or "").lower()
    for pattern, cat in ITEM_KEYWORDS.items():
        if re.search(pattern, text):
            return cat
    return None

def ai_categorize(ocr_text: str):
    """Zero-shot classification fallback."""
    text = ocr_text or ""
    if not text.strip():
        return "Other"
    res = zero_shot(text, candidate_labels=ZERO_SHOT_LABELS, multi_label=False)
    return res["labels"][0] if res and "labels" in res and res["labels"] else "Other"

def categorize_invoice(vendor: str, ocr_text: str) -> str:
    # 1) vendor (fuzzy)
    cat = fuzzy_vendor_match(vendor)
    if cat:
        return cat
    # 2) regex keywords over OCR text
    cat = regex_keyword_category(ocr_text)
    if cat:
        return cat
    # 3) zero-shot fallback
    return ai_categorize(ocr_text)

def parse_invoice_text_with_hf(image, ocr_text: str):
    vendor, date, amount = "Unknown", "Unknown", 0.0

    # Ask targeted questions
    vendor_ans = invoice_qa(image=image, question="Who is the vendor?")
    date_ans = invoice_qa(image=image, question="What is the invoice date?")
    amount_ans = invoice_qa(image=image, question="What is the total amount?")

    if vendor_ans:
        vendor = vendor_ans[0].get("answer", vendor)
    if date_ans:
        date = date_ans[0].get("answer", date)
    if amount_ans:
        amount = extract_amount(amount_ans[0].get("answer", ""))

    category = categorize_invoice(vendor, ocr_text)

    return {
        "vendor": vendor,
        "date": date,
        "amount": amount,
        "category": category
    }

# ---------- API ----------
@app.post("/upload-invoice/")
async def upload_invoice(file: UploadFile = File(...)):
    image_bytes = await file.read()
    processed_img = preprocess_image(image_bytes)

    # OCR text (for categorization + fallback)
    ocr_text = pytesseract.image_to_string(processed_img, config="--oem 3 --psm 6")

    # Run invoice model on the original image (PIL)
    img = Image.open(BytesIO(image_bytes))
    data = parse_invoice_text_with_hf(img, ocr_text)

    # Save to DB
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "INSERT INTO invoices (vendor, date, amount, category) VALUES (?, ?, ?, ?)",
        (data["vendor"], data["date"], data["amount"], data["category"])
    )
    conn.commit()
    conn.close()

    return {"message": "Invoice processed", "data": data}

@app.get("/invoices/")
def get_invoices():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM invoices")
    rows = c.fetchall()
    conn.close()
    return {"invoices": rows}

@app.get("/export-csv/")
def export_csv():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM invoices")
    rows = c.fetchall()
    conn.close()

    csv_path = os.path.join(BASE_DIR, "invoices.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Vendor", "Date", "Amount", "Category"])
        writer.writerows(rows)

    return {"message": "Exported to invoices.csv", "path": csv_path}
