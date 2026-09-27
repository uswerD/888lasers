from flask import Flask, render_template, request, jsonify
from pathlib import Path
import sqlite3
import os

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "orders.db"
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

def init_db():
    with sqlite3.connect(DB_PATH) as con:
        con.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            description TEXT NOT NULL,
            quantity TEXT,
            size TEXT,
            material TEXT,
            deadline TEXT,
            name TEXT,
            contact TEXT,
            file_name TEXT,
            status TEXT DEFAULT 'Новая'
        )
        """)
        con.commit()

@app.route("/")
def index():
    return render_template("index.html")

@app.post("/api/order")
def create_order():
    description = request.form.get("description", "").strip()
    if not description:
        return jsonify(ok=False, error="Опишите, что нужно изготовить."), 400

    data = {
        "description": description,
        "quantity": request.form.get("quantity", "").strip(),
        "size": request.form.get("size", "").strip(),
        "material": request.form.get("material", "").strip(),
        "deadline": request.form.get("deadline", "").strip(),
        "name": request.form.get("name", "").strip(),
        "contact": request.form.get("contact", "").strip(),
    }

    uploaded = request.files.get("file")
    file_name = ""
    if uploaded and uploaded.filename:
        safe_name = Path(uploaded.filename).name
        file_name = safe_name
        uploaded.save(UPLOAD_DIR / safe_name)

    with sqlite3.connect(DB_PATH) as con:
        cur = con.execute("""
            INSERT INTO orders
            (description, quantity, size, material, deadline, name, contact, file_name)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (*data.values(), file_name))
        order_id = cur.lastrowid
        con.commit()

    # Telegram подключим следующим этапом через BOT_TOKEN и ADMIN_CHAT_ID.
    return jsonify(ok=True, order_id=order_id)

init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
