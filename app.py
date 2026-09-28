from flask import Flask, render_template
import os

app = Flask(__name__)

# Укажи в Render → Environment значение TELEGRAM_URL,
# например https://t.me/username_бота
TELEGRAM_URL = os.environ.get("TELEGRAM_URL", "https://t.me/")

@app.route("/")
def index():
    return render_template("index.html", telegram_url=TELEGRAM_URL)

@app.route("/robots.txt")
def robots():
    return "User-agent: *\nAllow: /\nSitemap: https://888lasers.ru/sitemap.xml\n", 200, {"Content-Type": "text/plain; charset=utf-8"}

@app.route("/sitemap.xml")
def sitemap():
    return """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://888lasers.ru/</loc></url>
</urlset>""", 200, {"Content-Type": "application/xml; charset=utf-8"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
