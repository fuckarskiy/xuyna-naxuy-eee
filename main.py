from flask import Flask, request, render_template_string
import requests

# ----------------- FLASK -----------------
app = Flask(__name__)

# ----------------- ROUTE -----------------
@app.route("/", methods=["GET", "POST"])
def index():
    # Минимальный HTML прямо внутри функции
    html = """
    <html>
    <head><title>ARSKIY OSINT</title></head>
    <body>
        <h1>ARSKIY OSINT</h1>
        <form method="post">
            <input name="query" placeholder="Username" required>
            <button>Analyze</button>
        </form>
        {% if report %}
            <table border="1">
                <tr><th>Platform</th><th>Status</th><th>Link</th></tr>
                {% for platform, data in report.items() %}
                <tr>
                    <td>{{ platform }}</td>
                    <td>{{ 'FOUND' if data.exists else 'NOT FOUND' }}</td>
                    <td><a href="{{ data.url }}" target="_blank">open</a></td>
                </tr>
                {% endfor %}
            </table>
        {% endif %}
    </body>
    </html>
    """

    # Инициализация переменных
    report = {}

    if request.method == "POST":
        query = request.form.get("query", "").strip()
        if query:
            # Словарь платформ
            platforms = {
                "Telegram": f"https://t.me/{query}",
                "GitHub": f"https://github.com/{query}",
                "TikTok": f"https://www.tiktok.com/@{query}"
            }

            # Проверяем существование аккаунта
            for platform_name, url in platforms.items():
                try:
                    r = requests.get(url, headers={"User-Agent": "Arskiy-OSINT"}, timeout=5)
                    exists = r.status_code == 200
                except requests.RequestException:
                    exists = False
                report[platform_name] = {"url": url, "exists": exists}

    return render_template_string(html, report=report)

# ----------------- RUN -----------------
if name == "__main__":
    app.run(host="0.0.0.0", port=5000)
