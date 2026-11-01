from flask import Flask, render_template_string, request

app = Flask(__name__)


# --- CÁC HÀM XỬ LÝ DỮ LIỆU ---
def parse_number_b1(val_str):
    """Bài 1: Xử lý số thực, chấp nhận dấu phẩy (,)"""
    if not val_str or not val_str.strip():
        return None, "Không được để trống"
    clean_str = val_str.strip().replace(",", ".")
    try:
        return float(clean_str), None
    except ValueError:
        return None, "Vui lòng nhập một số hợp lệ."


def validate_score_b2(val_str, field_name):
    """Bài 2: Kiểm tra điểm từ 0 đến 10 dùng chung cho CC, GK, CK"""
    if not val_str or not val_str.strip():
        return None, f"Vui lòng nhập điểm {field_name}."
    clean_str = val_str.strip().replace(",", ".")
    try:
        val = float(clean_str)
        if val < 0 or val > 10:
            return None, f"Điểm {field_name} phải từ 0 đến 10."
        return val, None
    except ValueError:
        return None, f"Điểm {field_name} phải là số."


def validate_bmi_b3(val_str, field_name, min_val, max_val):
    """Bài 3: Kiểm tra chiều cao (50-250cm) và cân nặng (10-300kg)"""
    if not val_str or not val_str.strip():
        return None, f"Vui lòng nhập {field_name}."
    clean_str = val_str.strip().replace(",", ".")
    try:
        val = float(clean_str)
        if field_name == "chiều cao" and val < 3:
            return (
                None,
                f"Giá trị từ {min_val}-{max_val} cm (vui lòng nhập cm thay vì mét).",
            )
        if val < min_val or val > max_val:
            return None, f"{field_name.capitalize()} phải từ {min_val} đến {max_val}."
        return val, None
    except ValueError:
        return None, f"{field_name.capitalize()} phải là số."


# --- GIAO DIỆN HTML/CSS MỚI ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bộ Công Cụ Tiện Ích Flask</title>
    <!-- Google Fonts & FontAwesome -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        :root {
            --primary: #4f46e5;
            --primary-hover: #4338ca;
            --bg-body: #f8fafc;
            --card-bg: #ffffff;
            --text-main: #0f172a;
            --text-muted: #64748b;
            --border-color: #e2e8f0;
            --danger: #ef4444;
            --success: #10b981;
            --warning: #f59e0b;
        }

        * { box-sizing: border-box; font-family: 'Inter', sans-serif; margin: 0; padding: 0; }
        body { background-color: var(--bg-body); color: var(--text-main); min-height: 100vh; padding-bottom: 40px; }

        /* Header & Nav */
        .header { background: linear-gradient(135deg, #1e293b, #0f172a); padding: 30px 20px 25px; text-align: center; color: white; }
        .header h1 { font-size: 24px; font-weight: 700; margin-bottom: 6px; letter-spacing: -0.5px; }
        .header p { color: #94a3b8; font-size: 14px; }

        .nav-tabs { display: flex; justify-content: center; gap: 10px; margin-top: -22px; padding: 0 15px; flex-wrap: wrap; }
        .tab-btn {
            background: var(--card-bg);
            color: var(--text-muted);
            padding: 12px 20px;
            border-radius: 12px;
            text-decoration: none;
            font-weight: 600;
            font-size: 14px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            border: 1px solid var(--border-color);
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .tab-btn:hover { color: var(--primary); transform: translateY(-2px); }
        .tab-btn.active { background: var(--primary); color: white; border-color: var(--primary); shadow: 0 10px 15px -3px rgba(79, 70, 229, 0.3); }

        /* Container & Card */
        .container { max-width: 520px; margin: 30px auto 0; padding: 0 15px; }
        .card { background: var(--card-bg); border-radius: 16px; padding: 28px; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.05), 0 8px 10px -6px rgba(0,0,0,0.01); border: 1px solid var(--border-color); }
        .card-title { font-size: 18px; font-weight: 700; color: var(--text-main); margin-bottom: 20px; padding-bottom: 12px; border-bottom: 1px solid var(--border-color); display: flex; align-items: center; gap: 10px; }

        /* Form Controls */
        .form-group { margin-bottom: 18px; }
        label { display: block; font-size: 13px; font-weight: 600; color: #334155; margin-bottom: 6px; }
        input[type="text"], select {
            width: 100%;
            padding: 11px 14px;
            border-radius: 8px;
            border: 1px solid var(--border-color);
            background-color: #f8fafc;
            font-size: 14px;
            color: var(--text-main);
            transition: all 0.2s;
            outline: none;
        }
        input[type="text"]:focus, select:focus {
            border-color: var(--primary);
            background-color: #fff;
            box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.15);
        }
        .btn-submit {
            width: 100%;
            background-color: var(--primary);
            color: white;
            border: none;
            padding: 12px;
            border-radius: 8px;
            font-size: 15px;
            font-weight: 600;
            cursor: pointer;
            transition: background-color 0.2s, transform 0.1s;
            margin-top: 10px;
        }
        .btn-submit:hover { background-color: var(--primary-hover); }
        .btn-submit:active { transform: scale(0.99); }

        /* Error Messages */
        .error-msg { color: var(--danger); font-size: 12px; font-weight: 500; margin-top: 4px; display: flex; align-items: center; gap: 4px; }
        .error-box { background: #fef2f2; border: 1px solid #fecaca; color: #991b1b; padding: 10px 14px; border-radius: 8px; font-size: 13px; margin-bottom: 15px; font-weight: 500; }

        /* Results Box */
        .result-card { margin-top: 22px; padding: 16px; border-radius: 10px; font-size: 15px; font-weight: 600; display: flex; align-items: center; gap: 12px; }
        .result-default { background: #f0fdf4; border: 1px solid #bbf7d0; color: #166534; }
        .result-green { background: #f0fdf4; border: 1px solid #bbf7d0; color: #166534; }
        .result-yellow { background: #fefce8; border: 1px solid #fef08a; color: #854d0e; }
        .result-red { background: #fef2f2; border: 1px solid #fecaca; color: #991b1b; }
        .result-icon { font-size: 20px; }
    </style>
</head>
<body>

    <div class="header">
        <h1>Bảng Báo Cáo & Tính Toán</h1>
        <p>Ứng dụng tổng hợp các công cụ tính toán tự động</p>
    </div>

    <!-- TAB MENU -->
    <div class="nav-tabs">
        <a href="/?tab=bai1" class="tab-btn {% if active_tab == 'bai1' %}active{% endif %}">
            <i class="fa-solid fa-calculator"></i> Bài 1: Máy tính
        </a>
        <a href="/?tab=bai2" class="tab-btn {% if active_tab == 'bai2' %}active{% endif %}">
            <i class="fa-solid fa-graduation-cap"></i> Bài 2: Điểm học phần
        </a>
        <a href="/?tab=bai3" class="tab-btn {% if active_tab == 'bai3' %}active{% endif %}">
            <i class="fa-solid fa-heart-pulse"></i> Bài 3: Chỉ số BMI
        </a>
    </div>

    <div class="container">
        <div class="card">
            
            <!-- BÀI 1: MÁY TÍNH CƠ BẢN -->
            {% if active_tab == 'bai1' %}
                <div class="card-title">
                    <i class="fa-solid fa-calculator" style="color: var(--primary);"></i>
                    <span>Máy Tính Cơ Bản</span>
                </div>
                <form method="POST" action="/?tab=bai1">
                    <div class="form-group">
                        <label>Số thứ nhất (a)</label>
                        <input type="text" name="a" placeholder="Ví dụ: 10.5" value="{{ b1_a }}">
                        {% if b1_err_a %}<div class="error-msg"><i class="fa-solid fa-circle-exclamation"></i> {{ b1_err_a }}</div>{% endif %}
                    </div>

                    <div class="form-group">
                        <label>Phép toán</label>
                        <select name="op">
                            <option value="+" {% if b1_op == '+' %}selected{% endif %}>Cộng (+)</option>
                            <option value="-" {% if b1_op == '-' %}selected{% endif %}>Trừ (-)</option>
                            <option value="*" {% if b1_op == '*' %}selected{% endif %}>Nhân (×)</option>
                            <option value="/" {% if b1_op == '/' %}selected{% endif %}>Chia (÷)</option>
                        </select>
                        {% if b1_err_op %}<div class="error-msg"><i class="fa-solid fa-circle-exclamation"></i> {{ b1_err_op }}</div>{% endif %}
                    </div>

                    <div class="form-group">
                        <label>Số thứ hai (b)</label>
                        <input type="text" name="b" placeholder="Ví dụ: 5" value="{{ b1_b }}">
                        {% if b1_err_b %}<div class="error-msg"><i class="fa-solid fa-circle-exclamation"></i> {{ b1_err_b }}</div>{% endif %}
                    </div>

                    <button type="submit" class="btn-submit">Thực hiện tính toán</button>
                </form>

                {% if b1_result %}
                    <div class="result-card result-default">
                        <i class="fa-solid fa-circle-check result-icon"></i>
                        <div>Kết quả: {{ b1_result }}</div>
                    </div>
                {% endif %}
            {% endif %}


            <!-- BÀI 2: TÍNH ĐIỂM HỌC PHẦN -->
            {% if active_tab == 'bai2' %}
                <div class="card-title">
                    <i class="fa-solid fa-graduation-cap" style="color: var(--primary);"></i>
                    <span>Tính Điểm Học Phần</span>
                </div>
                <form method="POST" action="/?tab=bai2">
                    {% if b2_err_gen %}
                        <div class="error-box"><i class="fa-solid fa-triangle-exclamation"></i> {{ b2_err_gen }}</div>
                    {% endif %}

                    <div class="form-group">
                        <label>Điểm chuyên cần (CC - 10%)</label>
                        <input type="text" name="cc" placeholder="Nhập từ 0 - 10" value="{{ b2_cc }}">
                        {% if b2_err_cc %}<div class="error-msg"><i class="fa-solid fa-circle-exclamation"></i> {{ b2_err_cc }}</div>{% endif %}
                    </div>

                    <div class="form-group">
                        <label>Điểm giữa kỳ (GK - 30%)</label>
                        <input type="text" name="gk" placeholder="Nhập từ 0 - 10" value="{{ b2_gk }}">
                        {% if b2_err_gk %}<div class="error-msg"><i class="fa-solid fa-circle-exclamation"></i> {{ b2_err_gk }}</div>{% endif %}
                    </div>

                    <div class="form-group">
                        <label>Điểm cuối kỳ (CK - 60%)</label>
                        <input type="text" name="ck" placeholder="Nhập từ 0 - 10" value="{{ b2_ck }}">
                        {% if b2_err_ck %}<div class="error-msg"><i class="fa-solid fa-circle-exclamation"></i> {{ b2_err_ck }}</div>{% endif %}
                    </div>

                    <button type="submit" class="btn-submit">Tính điểm trung bình</button>
                </form>

                {% if b2_result %}
                    <div class="result-card result-default">
                        <i class="fa-solid fa-award result-icon"></i>
                        <div>{{ b2_result }}</div>
                    </div>
                {% endif %}
            {% endif %}


            <!-- BÀI 3: TÍNH CHỈ SỐ BMI -->
            {% if active_tab == 'bai3' %}
                <div class="card-title">
                    <i class="fa-solid fa-heart-pulse" style="color: var(--primary);"></i>
                    <span>Đánh Giá Chỉ Số BMI</span>
                </div>
                <form method="POST" action="/?tab=bai3">
                    {% if b3_err_gen %}
                        <div class="error-box"><i class="fa-solid fa-triangle-exclamation"></i> {{ b3_err_gen }}</div>
                    {% endif %}

                    <div class="form-group">
                        <label>Chiều cao (cm)</label>
                        <input type="text" name="height" placeholder="Ví dụ: 170" value="{{ b3_h }}">
                        {% if b3_err_h %}<div class="error-msg"><i class="fa-solid fa-circle-exclamation"></i> {{ b3_err_h }}</div>{% endif %}
                    </div>

                    <div class="form-group">
                        <label>Cân nặng (kg)</label>
                        <input type="text" name="weight" placeholder="Ví dụ: 65" value="{{ b3_w }}">
                        {% if b3_err_w %}<div class="error-msg"><i class="fa-solid fa-circle-exclamation"></i> {{ b3_err_w }}</div>{% endif %}
                    </div>

                    <button type="submit" class="btn-submit">Kiểm tra BMI</button>
                </form>

                {% if b3_result %}
                    <div class="result-card {{ b3_class }}">
                        <i class="fa-solid fa-chart-simple result-icon"></i>
                        <div>{{ b3_result }}</div>
                    </div>
                {% endif %}
            {% endif %}

        </div>
    </div>

</body>
</html>
"""


# --- ROUTE XỬ LÝ CHUNG ---
@app.route("/", methods=["GET", "POST"])
def main_app():
    active_tab = request.args.get("tab", "bai1")

    # Khởi tạo biến Bài 1
    b1_a, b1_b, b1_op = "", "", "+"
    b1_err_a = b1_err_b = b1_err_op = b1_result = None

    # Khởi tạo biến Bài 2
    b2_cc, b2_gk, b2_ck = "", "", ""
    b2_err_cc = b2_err_gk = b2_err_ck = b2_err_gen = b2_result = None

    # Khởi tạo biến Bài 3
    b3_h, b3_w = "", ""
    b3_err_h = b3_err_w = b3_err_gen = b3_result = b3_class = None

    if request.method == "POST":
        # --- BÀI 1 ---
        if active_tab == "bai1":
            b1_a = request.form.get("a", "")
            b1_b = request.form.get("b", "")
            b1_op = request.form.get("op", "+")

            num_a, b1_err_a = parse_number_b1(b1_a)
            num_b, b1_err_b = parse_number_b1(b1_b)
            if b1_op not in ["+", "-", "*", "/"]:
                b1_err_op = "Phép toán không hợp lệ."

            if not b1_err_a and not b1_err_b and not b1_err_op:
                if b1_op == "+":
                    res_val = num_a + num_b
                elif b1_op == "-":
                    res_val = num_a - num_b
                elif b1_op == "*":
                    res_val = num_a * num_b
                elif b1_op == "/":
                    if num_b == 0:
                        b1_err_b = "Không thể chia cho 0."
                    else:
                        res_val = num_a / num_b

                if b1_err_b is None:

                    def fmt(n):
                        return int(n) if n.is_integer() else n

                    b1_result = (
                        f"{fmt(num_a)} {b1_op} {fmt(num_b)} = {fmt(res_val)}"
                    )

        # --- BÀI 2 ---
        elif active_tab == "bai2":
            b2_cc = request.form.get("cc", "")
            b2_gk = request.form.get("gk", "")
            b2_ck = request.form.get("ck", "")

            if not b2_cc.strip() and not b2_gk.strip() and not b2_ck.strip():
                b2_err_gen = "Vui lòng nhập đầy đủ điểm cả 3 cột."
            else:
                cc_val, b2_err_cc = validate_score_b2(b2_cc, "chuyên cần")
                gk_val, b2_err_gk = validate_score_b2(b2_gk, "giữa kỳ")
                ck_val, b2_err_ck = validate_score_b2(b2_ck, "cuối kỳ")

                if not b2_err_cc and not b2_err_gk and not b2_err_ck:
                    total = round(
                        cc_val * 0.1 + gk_val * 0.3 + ck_val * 0.6, 1
                    )
                    if ck_val < 1:
                        letter, note = "F", "(Điểm thi cuối kỳ dưới 1)"
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

                    if note:
                        b2_result = (
                            f"Điểm tổng kết: {total} | Điểm chữ: {letter} {note}"
                        )
                    else:
                        b2_result = (
                            f"Điểm tổng kết: {total} | Điểm chữ: {letter}"
                        )

        # --- BÀI 3 ---
        elif active_tab == "bai3":
            b3_h = request.form.get("height", "")
            b3_w = request.form.get("weight", "")

            if not b3_h.strip() and not b3_w.strip():
                b3_err_gen = "Vui lòng nhập đầy đủ chiều cao và cân nặng."
            else:
                h_val, b3_err_h = validate_bmi_b3(b3_h, "chiều cao", 50, 250)
                w_val, b3_err_w = validate_bmi_b3(b3_w, "cân nặng", 10, 300)

                if not b3_err_h and not b3_err_w:
                    h_m = h_val / 100.0
                    bmi = round(w_val / (h_m**2), 1)

                    if bmi < 18.5:
                        b3_result = f"BMI = {bmi} — Thiếu cân"
                        b3_class = "result-yellow"
                    elif bmi < 23:
                        min_w = round(18.5 * (h_m**2), 1)
                        max_w = round(22.9 * (h_m**2), 1)
                        b3_result = f"BMI = {bmi} — Bình thường (Cân nặng lý tưởng: {min_w} – {max_w} kg)"
                        b3_class = "result-green"
                    elif bmi < 25:
                        b3_result = f"BMI = {bmi} — Thừa cân"
                        b3_class = "result-yellow"
                    else:
                        b3_result = f"BMI = {bmi} — Béo phì"
                        b3_class = "result-red"

    return render_template_string(
        HTML_TEMPLATE,
        active_tab=active_tab,
        b1_a=b1_a,
        b1_b=b1_b,
        b1_op=b1_op,
        b1_err_a=b1_err_a,
        b1_err_b=b1_err_b,
        b1_err_op=b1_err_op,
        b1_result=b1_result,
        b2_cc=b2_cc,
        b2_gk=b2_gk,
        b2_ck=b2_ck,
        b2_err_cc=b2_err_cc,
        b2_err_gk=b2_err_gk,
        b2_err_ck=b2_err_ck,
        b2_err_gen=b2_err_gen,
        b2_result=b2_result,
        b3_h=b3_h,
        b3_w=b3_w,
        b3_err_h=b3_err_h,
        b3_err_w=b3_err_w,
        b3_err_gen=b3_err_gen,
        b3_result=b3_result,
        b3_class=b3_class,
    )


if __name__ == "__main__":
    app.run(debug=True)