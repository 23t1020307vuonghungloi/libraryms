from flask import Flask, jsonify, url_for
from werkzeug.routing import BaseConverter
from markupsafe import escape
from flask import Flask, request
from flask import Flask, request, jsonify, abort

app = Flask(__name__)

# --- BÀI 5: Tùy chỉnh Converter cho Danh sách ---
class ListConverter(BaseConverter):
    regex = r"-?\d+(?:,-?\d+)*"

    def to_python(self, value):
        return [int(number) for number in value.split(",")]

    def to_url(self, values):
        return ",".join(str(value) for value in values)

app.url_map.converters["list"] = ListConverter


# --- BÀI 1 & BÀI 2 ---
@app.route("/home")
@app.route("/index-page")
def home():
    return "Hello, Flask!"

@app.route("/chia-nhom")
def chia_nhom():
    so_bai = 12
    so_nhom = 1
    rs = f"Mỗi nhóm làm {so_bai / so_nhom} bài"
    return rs


# --- BÀI 3 & BÀI 4 ---
@app.route("/profile/<user_name>")  # Đã đổi route để không trùng với bài 6
def profile_bai3(user_name):
    return f"Xin chào bạn: {user_name}"

@app.route("/square/<float:n>")
def square(n):
    return str(n ** 2)


# --- BÀI 5 ---
@app.route("/sum/<list:numbers>")
def sum_numbers(numbers):
    return jsonify(numbers=numbers, sum=sum(numbers))


# --- BÀI 6 ---
@app.route("/")
def index():
    return "Trang chủ"

@app.route("/about")
def about():
    return "Giới thiệu"

@app.route("/post/<int:post_id>")
def post_detail(post_id):
    return f"Chi tiết bài viết: {post_id}"

@app.route("/user/<username>")
def user_profile(username):
    return f"Trang cá nhân: {username}"

@app.route("/search")
def search():
    return "Tìm kiếm"

@app.route("/menu")
def menu():
    links = [
        f'<li><a href="{url_for("index")}">1. Trang chủ (index)</a></li>',
        f'<li><a href="{url_for("about")}">2. Giới thiệu (about)</a></li>',
        f'<li><a href="{url_for("post_detail", post_id=10)}">3. Bài viết số 10</a></li>',
        f'<li><a href="{url_for("user_profile", username="AnNguyen")}">4. Trang cá nhân AnNguyen</a></li>',
        f'<li><a href="{url_for("search", q="python")}">5. Tìm kiếm keyword "python"</a></li>',
    ]
    return f"<h2>Danh mục liên kết (Bài 6)</h2><ul>{''.join(links)}</ul>"
#bai7
# 1. Phương thức GET: Hiển thị form đăng nhập
@app.get("/login")
def login_form():
    # Sinh URL tự động bằng url_for cho thuộc tính action
    login_url = url_for("login_submit")
    
    return f'''
        <form action="{login_url}" method="post">
            <label for="username">Tên đăng nhập:</label>
            <input type="text" id="username" name="username" required>
            <button type="submit">Đăng nhập</button>
        </form>
    '''

# 2. Phương thức POST: Xử lý yêu cầu đăng nhập
@app.post("/login")
def login_submit():
    return "Đã nhận yêu cầu đăng nhập (POST)"
#bai8
@app.route("/info", methods=["GET", "POST"])
def info():
    # Lấy dữ liệu và thực hiện escape() để phòng chống lỗ hổng XSS
    method = escape(request.method)
    path = escape(request.path)
    full_path = escape(request.full_path)
    url = escape(request.url)
    remote_addr = escape(request.remote_addr or "")
    user_agent = escape(request.headers.get("User-Agent", ""))
    
    # Chuyển đổi request.args thành dict và chuỗi để hiển thị
    query_params = escape(str(dict(request.args)))

    return f"""
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <title>Thông tin Request</title>
        <style>
            table {{ border-collapse: collapse; width: 70%; margin: 20px auto; font-family: Arial, sans-serif; }}
            th, td {{ border: 1px solid #dddddd; padding: 10px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <h2 style="text-align: center;">Bảng thông tin Request</h2>
        <table>
            <tr>
                <th>Thuộc tính</th>
                <th>Giá trị</th>
            </tr>
            <tr><td>Phương thức</td><td>{method}</td></tr>
            <tr><td>Đường dẫn</td><td>{path}</td></tr>
            <tr><td>Đường dẫn kèm query</td><td>{full_path}</td></tr>
            <tr><td>URL đầy đủ</td><td>{url}</td></tr>
            <tr><td>Địa chỉ IP</td><td>{remote_addr}</td></tr>
            <tr><td>User-Agent</td><td>{user_agent}</td></tr>
            <tr><td>Các tham số query</td><td>{query_params}</td></tr>
        </table>
    </body>
    </html>
    """
#bai 9
# Bắt lỗi 400 Bad Request và trả về định dạng JSON
@app.errorhandler(400)
def bad_request_error(error):
    return jsonify({"error": error.description}), 400

@app.route("/calc")
def calc():
    # 1. Kiểm tra sự tồn tại của tham số 'a' và 'b'
    if "a" not in request.args or "b" not in request.args:
        abort(400, description="Thiếu tham số 'a' hoặc 'b'")

    # 2. Ép kiểu float cho a và b (trả về None nếu chuyển đổi thất bại)
    a = request.args.get("a", type=float)
    b = request.args.get("b", type=float)

    if a is None or b is None:
        abort(400, description="Giá trị của 'a' và 'b' phải là số")

    # 3. Lấy tham số 'op', mặc định là 'add'
    op = request.args.get("op", default="add")

    # Định nghĩa các phép toán hợp lệ và ký tự tương ứng
    valid_ops = {
        "add": "+",
        "sub": "-",
        "mul": "*",
        "div": "/"
    }

    # 4. Kiểm tra 'op' có hợp lệ không
    if op not in valid_ops:
        abort(400, description=f"Phép toán '{op}' không hợp lệ. Các phép toán cho phép: add, sub, mul, div")

    # 5. Kiểm tra lỗi chia cho 0
    if op == "div" and b == 0:
        abort(400, description="Không thể chia cho 0")

    # 6. Tính toán kết quả
    if op == "add":
        result = a + b
    elif op == "sub":
        result = a - b
    elif op == "mul":
        result = a * b
    elif op == "div":
        result = a / b

    # Định dạng biểu thức (loại bỏ .0 nếu là số nguyên để hiển thị đẹp như ví dụ)
    a_fmt = int(a) if a.is_integer() else a
    b_fmt = int(b) if b.is_integer() else b
    expression = f"{a_fmt} {valid_ops[op]} {b_fmt}"

    # Trả về JSON thành công
    return jsonify({
        "a": a,
        "b": b,
        "op": op,
        "expression": expression,
        "result": result
    })
#bai tren lop

if __name__ == "__main__":
    app.run(debug=True, port=8000)