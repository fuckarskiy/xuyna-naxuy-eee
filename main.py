from flask import Flask, request, render_template_string
import re
import requests

# ----------------- FLASK APP -----------------
app = Flask(__name__)

# ----------------- LOAD HTML/CSS -----------------
with open("index.html", encoding="utf-8") as f:
    HTML = f.read()

with open("style.css", encoding="utf-8") as f:
    CSS = f.read()

# ----------------- HEADERS AND TIMEOUT -----------------
HEADERS = {
    "User-Agent": "Arskiy-OSINT/1.0"
}
TIMEOUT = 5

# ----------------- DETECT TARGET -----------------
def detect_target(q):
    if re.fullmatch(r"\+?\d{7,15}", q):
        return "PHONE"
    if re.fullmatch(r"[a-zA-Z0-9_.]{3,32}", q):
        return "USERNAME"
    return "UNKNOWN"

# ----------------- CHECK ACCOUNT -----------------
def check_exists(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        return r.status_code == 200
    except:
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
        results[name] = {
            "url": url,
            "exists": check_exists(url)
        }
    return results

# ----------------- ROUTES -----------------
@app.route("/", methods=["GET", "POST"])
def index():
    report = None
    target = None

    if request.method == "POST":
        query = request.form["query"].strip()
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
    app.run()
