from datetime import timedelta
from flask import (
    Flask,
    flash,
    redirect,
    render_template_string,
    request,
    session,
    url_for,
)

app = Flask(__name__)
app.secret_key = "secret_key_demo"  # Khóa bí mật session
app.permanent_session_lifetime = timedelta(days=7)  # Cookie có Expires 7 ngày khi chọn "Ghi nhớ"

# 1. Khai báo danh sách người dùng (đúng theo yêu cầu)
USERS = {"admin": "admin123", "an": "an123456"}

# 2. Template HTML chuẩn với Menu dùng chung ở tất cả các trang
BASE_LAYOUT = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        * { box-sizing: border-box; font-family: Arial, sans-serif; }
        body { margin: 0; padding: 0; background-color: #f4f6f9; color: #333; }
        
        /* Thanh Menu / Header */
        .navbar { background: #007bff; padding: 12px 24px; display: flex; justify-content: space-between; align-items: center; color: white; }
        .navbar a { color: white; text-decoration: none; margin-right: 15px; font-weight: bold; }
        .navbar a:hover { text-decoration: underline; }
        .navbar .user-info { display: flex; align-items: center; gap: 12px; }
        .btn-logout { background: #dc3545; color: white; border: none; padding: 6px 14px; border-radius: 4px; cursor: pointer; font-size: 14px; }
        .btn-logout:hover { background: #bd2130; }

        /* Khung nội dung chính */
        .container { max-width: 480px; margin: 40px auto; background: white; padding: 25px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .form-group { margin-bottom: 15px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: bold; }
        .form-group input[type="text"], .form-group input[type="password"] { width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px; }
        .btn-submit { width: 100%; padding: 10px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; }
        .btn-submit:hover { background: #0056b3; }

        /* Thông báo Flash */
        .flash-messages { margin-bottom: 15px; }
        .flash { padding: 10px 14px; border-radius: 4px; font-size: 14px; margin-bottom: 8px; }
        .flash.success { background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .flash.error { background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
    </style>
</head>
<body>
    <!-- Thanh menu xuất hiện ở mọi trang -->
    <nav class="navbar">
        <div>
            <a href="{{ url_for('index') }}">Trang chủ</a>
            {% if session.get('user') %}
                <a href="{{ url_for('profile') }}">Trang cá nhân</a>
            {% endif %}
        </div>
        <div class="user-info">
            {% if session.get('user') %}
                <span>Xin chào {{ session['user'] }}</span>
                <form action="{{ url_for('logout') }}" method="POST" style="display: inline;">
                    <button type="submit" class="btn-logout">Đăng xuất</button>
                </form>
            {% else %}
                <a href="{{ url_for('login') }}">Đăng nhập</a>
            {% endif %}
        </div>
    </nav>

    <div class="container">
        <!-- Thông báo Flash -->
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                <div class="flash-messages">
                    {% for category, message in messages %}
                        <div class="flash {{ category }}">{{ message }}</div>
                    {% endfor %}
                </div>
            {% endif %}
        {% endwith %}

        {{ content | safe }}
    </div>
</body>
</html>
"""

# Nội dung cho từng trang
LOGIN_CONTENT = """
<h2>Đăng Nhập</h2>
<form method="POST" action="{{ url_for('login') }}">
    <div class="form-group">
        <label for="username">Tên đăng nhập:</label>
        <input type="text" id="username" name="username" value="{{ username }}" autocomplete="off">
    </div>
    <div class="form-group">
        <label for="password">Mật khẩu:</label>
        <input type="password" id="password" name="password">
    </div>
    <div class="form-group">
        <label>
            <input type="checkbox" name="remember"> Ghi nhớ đăng nhập
        </label>
    </div>
    <button type="submit" class="btn-submit">Đăng nhập</button>
</form>
"""

INDEX_CONTENT = """
<h1>Trang Chủ</h1>
{% if session.get('user') %}
    <p>Chào mừng bạn <strong>{{ session['user'] }}</strong> đến với hệ thống!</p>
{% else %}
    <p>Bạn chưa đăng nhập vào hệ thống.</p>
{% endif %}
"""

PROFILE_CONTENT = """
<h1>Trang Cá Nhân (Profile)</h1>
<p><strong>Tài khoản:</strong> {{ session['user'] }}</p>
<p>Nội dung chỉ dành riêng cho người dùng đã đăng nhập.</p>
"""


# 3. Các Route xử lý logic đúng yêu cầu đề bài
@app.route("/")
def index():
    html = BASE_LAYOUT.replace("{{ title }}", "Trang Chủ").replace("{{ content | safe }}", INDEX_CONTENT)
    return render_template_string(html)


@app.route("/login", methods=["GET", "POST"])
def login():
    # Đã đăng nhập -> vào /login sẽ tự động chuyển hướng về /
    if "user" in session:
        return redirect(url_for("index"))

    username = ""
    if request.method == "POST":
        # Dùng .strip() để tự động xóa khoảng trắng đầu/cuối của tên đăng nhập
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        remember = request.form.get("remember")

        # Phân biệt hoa/thường và kiểm tra tài khoản
        if username in USERS and USERS[username] == password:
            session["user"] = username
            if remember:
                session.permanent = True  # Lưu cookie đăng nhập (Expires 7 ngày)
            else:
                session.permanent = False

            flash(f"Đăng nhập thành công. Xin chào {username}!", category="success")
            return redirect(url_for("index"))
        else:
            # Nếu sai: flash lỗi, giữ tên đăng nhập, xóa mật khẩu
            flash("Sai tên đăng nhập hoặc mật khẩu", category="error")

    html = BASE_LAYOUT.replace("{{ title }}", "Đăng nhập").replace("{{ content | safe }}", LOGIN_CONTENT)
    return render_template_string(html, username=username)


@app.route("/profile")
def profile():
    # Vào /profile khi chưa đăng nhập -> về /login, flash "Vui lòng đăng nhập..."
    if "user" not in session:
        flash("Vui lòng đăng nhập...", category="error")
        return redirect(url_for("login"))

    html = BASE_LAYOUT.replace("{{ title }}", "Trang cá nhân").replace("{{ content | safe }}", PROFILE_CONTENT)
    return render_template_string(html)


@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user", None)
    session.clear()
    flash("Bạn đã đăng xuất.", category="success")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)