from flask import Flask, request, render_template_string
import requests

# ----------------- FLASK APP -----------------
app = Flask(__name__)

# ----------------- LOAD HTML/CSS -----------------
try:
    with open("index.html", encoding="utf-8") as f:
        HTML = f.read()
    with open("style.css", encoding="utf-8") as f:
        CSS = f.read()
except FileNotFoundError:
    raise FileNotFoundError("index.html или style.css не найдены в корне проекта!")

# ----------------- HEADERS -----------------
HEADERS = {"User-Agent": "Arskiy-OSINT/1.0"}
TIMEOUT = 5

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
        "TikTok": f"https://www.tiktok.com/@{username}"
    }
    results = {}
    for name, url in platforms.items():
        results[name] = {
            "url": url,
            "exists": check_exists(url)
        }
    return results

# ----------------- ROUTE -----------------
@app.route("/", methods=["GET", "POST"])
def index():
    report = {}
    if request.method == "POST":
        query = request.form.get("query", "").strip()
        if query:
            report = username_osint(query)
    return render_template_string(HTML.replace("{{STYLE}}", CSS), report=report)

# ----------------- RUN APP -----------------
if name == "__main__":
    app.run(host="0.0.0.0", port=5000)
