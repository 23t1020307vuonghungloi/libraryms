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
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    Regexp,
    ValidationError,
)

app = Flask(__name__)
app.secret_key = "secret_key_demo"
app.permanent_session_lifetime = timedelta(days=7)

# Cấu hình dữ liệu người dùng (dùng chung cho Bài 4 & Bài 5)
USERS = {"admin": "admin123", "an": "an123456"}


# ================= FORMS (FLASK-WTF) =================
class RegisterForm(FlaskForm):
    username = StringField(
        "Tên đăng nhập",
        validators=[
            DataRequired(message="Vui lòng nhập tên đăng nhập."),
            Length(min=4, max=20, message="Độ dài từ 4 đến 20 ký tự."),
            Regexp(
                r"^[a-z0-9_]+$",
                message="Chỉ chứa chữ thường không dấu, số, _",
            ),
        ],
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Vui lòng nhập email."),
            Email(message="Email không đúng định dạng."),
        ],
    )
    password = PasswordField(
        "Mật khẩu",
        validators=[
            DataRequired(message="Vui lòng nhập mật khẩu."),
            Length(min=8, message="Mật khẩu tối thiểu 8 ký tự."),
        ],
    )
    confirm_password = PasswordField(
        "Nhập lại mật khẩu",
        validators=[
            DataRequired(message="Vui lòng nhập lại mật khẩu."),
            EqualTo("password", message="Mật khẩu nhập lại không khớp."),
        ],
    )
    agree = BooleanField(
        "Đồng ý với điều khoản",
        validators=[DataRequired(message="Bạn phải đồng ý với điều khoản.")],
    )
    submit = SubmitField("Đăng ký")

    # Kiểm tra trùng tên đăng nhập với USERS
    def validate_username(self, field):
        if field.data in USERS:
            raise ValidationError("Tên đăng nhập đã được sử dụng.")


# ================= JINJA TEMPLATE & MACRO =================
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
        
        .navbar { background: #007bff; padding: 12px 24px; display: flex; justify-content: space-between; align-items: center; color: white; }
        .navbar a { color: white; text-decoration: none; margin-right: 15px; font-weight: bold; }
        .navbar a:hover { text-decoration: underline; }
        .navbar .user-info { display: flex; align-items: center; gap: 12px; }
        
        .container { max-width: 480px; margin: 30px auto; background: white; padding: 25px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .form-group { margin-bottom: 15px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: bold; }
        .form-control { width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px; font-size: 14px; }
        
        .btn-submit { width: 100%; padding: 10px; background: #28a745; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; font-weight: bold; }
        .btn-submit:hover { background: #218838; }
        .btn-logout { background: #dc3545; color: white; border: none; padding: 6px 14px; border-radius: 4px; cursor: pointer; }
        
        .flash { padding: 10px 14px; border-radius: 4px; font-size: 14px; margin-bottom: 15px; }
        .flash.success { background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .flash.error { background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        
        .error-msg { color: #dc3545; font-size: 13px; margin-top: 4px; display: block; }
    </style>
</head>
<body>
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
                <a href="{{ url_for('register') }}">Đăng ký</a>
            {% endif %}
        </div>
    </nav>

    <div class="container">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="flash {{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}

        {{ content | safe }}
    </div>
</body>
</html>
"""

# Macro render_field rendering mỗi ô input trong đúng 1 dòng
REGISTER_PAGE_HTML = """
{% macro render_field(field) %}
    <div class="form-group">
        {% if field.type == 'BooleanField' %}
            <label style="font-weight: normal; cursor: pointer;">
                {{ field() }} {{ field.label.text }}
            </label>
        {% elif field.type == 'SubmitField' %}
            {{ field(class="btn-submit") }}
        {% else %}
            {{ field.label }}
            {{ field(class="form-control") }}
        {% endif %}
        
        {% if field.errors %}
            {% for error in field.errors %}
                <span class="error-msg">• {{ error }}</span>
            {% endfor %}
        {% endif %}
    </div>
{% endmacro %}

<h2>Đăng ký tài khoản</h2>
<form method="POST" action="{{ url_for('register') }}" novalidate>
    {{ form.hidden_tag() }}
    {{ render_field(form.username) }}
    {{ render_field(form.email) }}
    {{ render_field(form.password) }}
    {{ render_field(form.confirm_password) }}
    {{ render_field(form.agree) }}
    {{ render_field(form.submit) }}
</form>
"""

LOGIN_PAGE_HTML = """
<h2>Đăng Nhập</h2>
<form method="POST" action="{{ url_for('login') }}">
    <div class="form-group">
        <label for="username">Tên đăng nhập:</label>
        <input type="text" id="username" name="username" class="form-control" value="{{ username }}" autocomplete="off">
    </div>
    <div class="form-group">
        <label for="password">Mật khẩu:</label>
        <input type="password" id="password" name="password" class="form-control">
    </div>
    <div class="form-group">
        <label style="font-weight: normal;">
            <input type="checkbox" name="remember"> Ghi nhớ đăng nhập
        </label>
    </div>
    <button type="submit" class="btn-submit" style="background:#007bff;">Đăng nhập</button>
</form>
"""

INDEX_PAGE_HTML = """
<h1>Trang Chủ</h1>
{% if session.get('user') %}
    <p>Chào mừng <strong>{{ session['user'] }}</strong> quay trở lại!</p>
{% else %}
    <p>Bạn chưa đăng nhập. Vui lòng đăng nhập hoặc đăng ký tài khoản mới.</p>
{% endif %}
"""

PROFILE_PAGE_HTML = """
<h1>Trang Cá Nhân</h1>
<p><strong>Tài khoản:</strong> {{ session['user'] }}</p>
"""


# ================= ROUTES =================
@app.route("/")
def index():
    html = BASE_LAYOUT.replace("{{ title }}", "Trang Chủ").replace(
        "{{ content | safe }}", INDEX_PAGE_HTML
    )
    return render_template_string(html)


@app.route("/register", methods=["GET", "POST"])
def register():
    if "user" in session:
        return redirect(url_for("index"))

    form = RegisterForm()
    if form.validate_on_submit():
        # Thêm tài khoản mới vào USERS
        USERS[form.username.data] = form.password.data
        flash("Đăng ký thành công.", category="success")
        return redirect(url_for("login"))

    html = BASE_LAYOUT.replace("{{ title }}", "Đăng ký").replace(
        "{{ content | safe }}", REGISTER_PAGE_HTML
    )
    return render_template_string(html, form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if "user" in session:
        return redirect(url_for("index"))

    username = ""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        remember = request.form.get("remember")

        if username in USERS and USERS[username] == password:
            session["user"] = username
            session.permanent = True if remember else False
            flash(
                f"Đăng nhập thành công. Xin chào {username}!", category="success"
            )
            return redirect(url_for("index"))
        else:
            flash("Sai tên đăng nhập hoặc mật khẩu", category="error")

    html = BASE_LAYOUT.replace("{{ title }}", "Đăng nhập").replace(
        "{{ content | safe }}", LOGIN_PAGE_HTML
    )
    return render_template_string(html, username=username)


@app.route("/profile")
def profile():
    if "user" not in session:
        flash("Vui lòng đăng nhập...", category="error")
        return redirect(url_for("login"))

    html = BASE_LAYOUT.replace("{{ title }}", "Trang cá nhân").replace(
        "{{ content | safe }}", PROFILE_PAGE_HTML
    )
    return render_template_string(html)


@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user", None)
    session.clear()
    flash("Bạn đã đăng xuất.", category="success")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)