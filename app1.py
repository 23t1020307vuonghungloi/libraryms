from flask import Flask, render_template, request
from datetime import date

app = Flask(__name__)

# Dữ liệu bài viết mẫu
POSTS = ["Bài viết 1", "Bài viết 2", "Bài viết 3"]

# 1. Biến toàn cục dùng ở mọi template
@app.context_processor
def inject_globals():
    return {
        "site_name": "MiniBlog",
        "current_year": date.today().year,
        "post_count": len(POSTS),
    }

# 2. Hàm hỗ trợ kiểm tra active menu dùng ở mọi template
@app.context_processor
def inject_helpers():
    def is_active(endpoint):
        return "active" if request.endpoint == endpoint else ""
    return {"is_active": is_active}

# --- Routes ---
@app.route("/")
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/hello/<name>")
def hello(name):
    return render_template("hello.html", name=name, skills=["Python", "Flask"])

if __name__ == "__main__":
    app.run(debug=True)