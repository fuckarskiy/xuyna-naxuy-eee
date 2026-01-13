from flask import Flask, request, render_template_string
import re
import requests
import os

# ----------------- FLASK APP -----------------
app = Flask(__name__)

# ----------------- LOAD HTML/CSS -----------------
HTML_FILE = "index.html"
CSS_FILE = "style.css"

if not os.path.exists(HTML_FILE) or not os.path.exists(CSS_FILE):
    raise FileNotFoundError("index.html или style.css не найдены в корне проекта!")

with open(HTML_FILE, encoding="utf-8") as f:
    HTML = f.read()

with open(CSS_FILE, encoding="utf-8") as f:
    CSS = f.read()

# ----------------- HEADERS AND TIMEOUT -----------------
HEADERS = {
    "User-Agent": "Arskiy-OSINT/1.0"
}
TIMEOUT = 5

# ----------------- DETECT TARGET -----------------
def detect_target(query):
    if re.fullmatch(r"\+?\d{7,15}", query):
        return "PHONE"
    if re.fullmatch(r"[a-zA-Z0-9_.]{3,32}", query):
        return "USERNAME"
    return "UNKNOWN"

# ----------------- CHECK ACCOUNT -----------------
def check_exists(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        return r.status_code == 200
    except requests.RequestException:
        return False

# ----------------- USERNAME OSINT -----------------
def username_osint(username):
    platforms = {
        "Telegram": f"https://t.me/{username}",
        "GitHub": f"https://github.com/{username}",
        "TikTok": f"https://www.tiktok.com/@{username}",
        "Instagram": f"https://www.instagram.com/{username}/",
        "Reddit": f"https://www.reddit.com/user/{username}"
    }

    results = {}
    for name, url in platforms.items():
        exists = check_exists(url)
        results[name] = {
            "url": url,
            "exists": exists
        }
    return results

# ----------------- ROUTES -----------------
@app.route("/", methods=["GET", "POST"])
def index():
    report = {}
    target = None

    if request.method == "POST":
        query = request.form.get("query", "").strip()
        target = detect_target(query)

        if target == "USERNAME":
            report = username_osint(query)
        else:
            report = {}

    return render_template_string(
        HTML.replace("{{STYLE}}", CSS),
        report=report,
        target=target
    )

# ----------------- RUN APP -----------------
if name == "__main__":
    app.run(host="0.0.0.0", port=5000)
