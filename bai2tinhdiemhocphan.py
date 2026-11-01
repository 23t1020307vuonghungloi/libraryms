from flask import Flask, render_template_string, request

app = Flask(__name__)

# Template HTML duy nhất chứa giao diện cho cả Bài 1 và Bài 2
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Bài tập Form & Xử lý dữ liệu người dùng</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 30px; background-color: #f8f9fa; }
        .card { background: white; padding: 20px 30px; margin-bottom: 30px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); max-width: 600px; }
        h2 { color: #0d6efd; border-bottom: 2px solid #0d6efd; padding-bottom: 8px; margin-top: 0; }
        .form-group { margin-bottom: 15px; }
        label { font-weight: bold; }
        input[type="text"], select { width: 100%; padding: 8px; margin-top: 5px; box-sizing: border-box; border: 1px solid #ccc; border-radius: 4px; }
        button { background-color: #0d6efd; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; font-weight: bold; }
        button:hover { background-color: #0b5ed7; }
        .error { color: #dc3545; font-size: 14px; margin-top: 5px; display: block; }
        .result { margin-top: 20px; padding: 12px; background-color: #e7f1ff; border-left: 5px solid #0d6efd; font-weight: bold; font-size: 16px; }
    </style>
</head>
<body>

    <!-- BÀI 1: MÁY TÍNH CƠ BẢN -->
    <div class="card">
        <h2>Bài 1 ★. Máy tính cơ bản</h2>
        <form method="POST" action="/bai1">
            <div class="form-group">
                <label>Số thứ nhất (a):</label>
                <input type="text" name="a" value="{{ b1_a }}">
                {% if b1_err_a %}<span class="error">{{ b1_err_a }}</span>{% endif %}
            </div>

            <div class="form-group">
                <label>Phép toán (op):</label>
                <select name="op">
                    <option value="+" {% if b1_op == '+' %}selected{% endif %}>+</option>
                    <option value="-" {% if b1_op == '-' %}selected{% endif %}>-</option>
                    <option value="*" {% if b1_op == '*' %}selected{% endif %}>*</option>
                    <option value="/" {% if b1_op == '/' %}selected{% endif %}>/</option>
                </select>
                {% if b1_err_op %}<span class="error">{{ b1_err_op }}</span>{% endif %}
            </div>

            <div class="form-group">
                <label>Số thứ hai (b):</label>
                <input type="text" name="b" value="{{ b1_b }}">
                {% if b1_err_b %}<span class="error">{{ b1_err_b }}</span>{% endif %}
            </div>

            <button type="submit">Tính toán</button>
        </form>

        {% if b1_result %}
            <div class="result">Kết quả: {{ b1_result }}</div>
        {% endif %}
    </div>


    <!-- BÀI 2: TÍNH ĐIỂM HỌC PHẦN -->
    <div class="card">
        <h2>Bài 2 ★. Tính điểm học phần</h2>
        <form method="POST" action="/bai2">
            <div class="form-group">
                <label>Chuyên cần (CC - 10%):</label>
                <input type="text" name="cc" value="{{ b2_cc }}">
                {% if b2_err_cc %}<span class="error">{{ b2_err_cc }}</span>{% endif %}
            </div>

            <div class="form-group">
                <label>Giữa kỳ (GK - 30%):</label>
                <input type="text" name="gk" value="{{ b2_gk }}">
                {% if b2_err_gk %}<span class="error">{{ b2_err_gk }}</span>{% endif %}
            </div>

            <div class="form-group">
                <label>Cuối kỳ (CK - 60%):</label>
                <input type="text" name="ck" value="{{ b2_ck }}">
                {% if b2_err_ck %}<span class="error">{{ b2_err_ck }}</span>{% endif %}
            </div>

            {% if b2_err_gen %}
                <div class="error" style="font-weight: bold; margin-bottom: 15px;">{{ b2_err_gen }}</div>
            {% endif %}

            <button type="submit">Tính điểm học phần</button>
        </form>

        {% if b2_result %}
            <div class="result">Kết quả: {{ b2_result }}</div>
        {% endif %}
    </div>

</body>
</html>
"""


# --- CÁC HÀM XỬ LÝ KHỬ DỮ LIỆU ---
def parse_number_b1(val_str):
    """Xử lý ép kiểu số cho Bài 1, hỗ trợ cả dấu phẩy (,)"""
    if not val_str or not val_str.strip():
        return None, "Trống"
    clean_str = val_str.strip().replace(",", ".")
    try:
        return float(clean_str), None
    except ValueError:
        return None, "Vui lòng nhập một số."


def validate_score_b2(val_str, field_name):
    """Hàm dùng chung kiểm tra điểm cho Bài 2"""
    if not val_str or not val_str.strip():
        return None, f"Lỗi ở {field_name}: Vui lòng nhập một số."
    clean_str = val_str.strip().replace(",", ".")
    try:
        val = float(clean_str)
        if val < 0 or val > 10:
            return None, f"Lỗi ở {field_name}: Điểm phải từ 0 đến 10."
        return val, None
    except ValueError:
        return None, f"Lỗi ở {field_name}: Vui lòng nhập một số."


# --- ROUTES CỦA ỨNG DỤNG ---
@app.route("/", methods=["GET"])
def index():
    return render_template_string(HTML_TEMPLATE, b1_op="+")


@app.route("/bai1", methods=["POST"])
def process_bai1():
    a_raw = request.form.get("a", "")
    b_raw = request.form.get("b", "")
    op = request.form.get("op", "+")

    num_a, err_a = parse_number_b1(a_raw)
    num_b, err_b = parse_number_b1(b_raw)
    err_op = (
        "Phép toán không hợp lệ." if op not in ["+", "-", "*", "/"] else None
    )

    result = None

    if not err_a and not err_b and not err_op:
        if op == "+":
            res_val = num_a + num_b
        elif op == "-":
            res_val = num_a - num_b
        elif op == "*":
            res_val = num_a * num_b
        elif op == "/":
            if num_b == 0:
                err_b = "Không thể chia cho 0."
            else:
                res_val = num_a / num_b

        if err_b is None:

            def fmt(n):
                return int(n) if n.is_integer() else n

            result = f"{fmt(num_a)} {op} {fmt(num_b)} = {fmt(res_val)}"

    return render_template_string(
        HTML_TEMPLATE,
        b1_a=a_raw,
        b1_b=b_raw,
        b1_op=op,
        b1_err_a=err_a,
        b1_err_b=err_b,
        b1_err_op=err_op,
        b1_result=result,
    )


@app.route("/bai2", methods=["POST"])
def process_bai2():
    cc_raw = request.form.get("cc", "")
    gk_raw = request.form.get("gk", "")
    ck_raw = request.form.get("ck", "")

    err_cc = err_gk = err_ck = err_gen = None
    result = None

    # Kiểm tra rỗng cả 3 ô
    if not cc_raw.strip() and not gk_raw.strip() and not ck_raw.strip():
        err_gen = "Lỗi cả 3 ô"
    else:
        cc_val, err_cc = validate_score_b2(cc_raw, "CC")
        gk_val, err_gk = validate_score_b2(gk_raw, "GK")
        ck_val, err_ck = validate_score_b2(ck_raw, "CK")

        if not err_cc and not err_gk and not err_ck:
            total = round(cc_val * 0.1 + gk_val * 0.3 + ck_val * 0.6, 1)

            if ck_val < 1:
                letter, note = "F", "(điểm thi dưới 1)"
            else:
                note = ""
                if total >= 8.5:
                    letter = "A"
                elif total >= 7.0:
                    letter = "B"
                elif total >= 5.5:
                    letter = "C"
                elif total >= 4.0:
                    letter = "D"
                else:
                    letter = "F"

            result = (
                f"{total} - {letter} {note}".strip()
                if note
                else f"{total} - {letter}"
            )

    return render_template_string(
        HTML_TEMPLATE,
        b2_cc=cc_raw,
        b2_gk=gk_raw,
        b2_ck=ck_raw,
        b2_err_cc=err_cc,
        b2_err_gk=err_gk,
        b2_err_ck=err_ck,
        b2_err_gen=err_gen,
        b2_result=result,
        b1_op="+",
    )


if __name__ == "__main__":
    app.run(debug=True)