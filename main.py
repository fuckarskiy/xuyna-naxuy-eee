from flask import Flask, request, render_template_string
import requests

# ----------------- FLASK -----------------
app = Flask(__name__)

# ----------------- ROUTE -----------------
@app.route("/", methods=["GET", "POST"])
def index():
    # HTML прямо в функции
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
                {% for platform, info in report.items() %}
                <tr>
                    <td>{{ platform }}</td>
                    <td>{{ 'FOUND' if info.exists else 'NOT FOUND' }}</td>
                    <td><a href="{{ info.url }}" target="_blank">open</a></td>
                </tr>
                {% endfor %}
            </table>
        {% endif %}
    </body>
    </html>
    """

    # Инициализируем report
    report = {}

    if request.method == "POST":
        query = request.form.get("query", "").strip()
        if query:
            # Словарь платформ
            platforms_dict = {
                "Telegram": f"https://t.me/{query}",
                "GitHub": f"https://github.com/{query}",
                "TikTok": f"https://www.tiktok.com/@{query}"
            }

            # Проверка аккаунтов
            for platform_key, url_value in platforms_dict.items():
                exists_flag = False
                try:
                    r = requests.get(url_value, headers={"User-Agent": "Arskiy-OSINT"}, timeout=5)
                    if r.status_code == 200:
                        exists_flag = True
                except requests.RequestException:
                    exists_flag = False
                report[platform_key] = {"url": url_value, "exists": exists_flag}

    return render_template_string(html, report=report)

# ----------------- RUN -----------------
if name == "__main__":
    app.run(host="0.0.0.0", port=5000)
