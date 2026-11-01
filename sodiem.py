from flask import Flask, render_template, request, jsonify, abort, redirect, url_for, make_response

app = Flask(__name__)
app.json.ensure_ascii = False

# Dữ liệu mẫu sinh viên
STUDENTS = {
    "23T1020001": {
        "name": "Nguyễn Văn An",
        "lop": "K47A",
        "scores": {"PMMM": 8.5, "CSDL": 7.0, "MMT": 9.0}
    },
    "23T1020002": {
        "name": "Trần Thị Bình",
        "lop": "K47A",
        "scores": {"PMMM": 6.0, "CSDL": 5.5, "MMT": 7.0}
    },
    "23T1020003": {
        "name": "Lê Hoàng Cường",
        "lop": "K47B",
        "scores": {"PMMM": 9.5, "CSDL": 9.0}
    },
    "23T1020004": {
        "name": "Phan Minh Dũng",
        "lop": "K47B",
        "scores": {"PMMM": 4.0, "CSDL": 3.5, "MMT": 5.0}
    },
    "23T1020005": {
        "name": "Hoàng Thu Hà",
        "lop": "K47A",
        "scores": {}
    },
    "23T1020006": {
        "name": "Vũ Quốc Khánh",
        "lop": "K47C",
        "scores": {"PMMM": 7.5, "MMT": 8.0}
    }
}

def calculate_average_and_rank(scores):
    if not scores:
        return None, "Chưa có"
    avg = sum(scores.values()) / len(scores)
    if avg >= 8.5: rank = "Giỏi"
    elif avg >= 7.0: rank = "Khá"
    elif avg >= 5.0: rank = "Trung bình"
    else: rank = "Yếu"
    return round(avg, 2), rank

# --- Câu 1: Trang chủ ---
@app.route("/")
def home():
    total_students = len(STUDENTS)
    classes = sorted(list(set(s["lop"] for s in STUDENTS.values())))
    return render_template("index.html", page="home", total_students=total_students, classes=classes)

@app.route("/api/students")
def api_students():
    return jsonify(STUDENTS)

# --- Câu 2: Trang danh sách sinh viên ---
@app.route("/students")
def student_list():
    selected_class = request.args.get("lop", "").strip()
    classes = sorted(list(set(s["lop"] for s in STUDENTS.values())))
    
    filtered_students = {}
    for mssv, info in STUDENTS.items():
        if not selected_class or selected_class.lower() == "tất cả" or info["lop"].lower() == selected_class.lower():
            avg, rank = calculate_average_and_rank(info["scores"])
            filtered_students[mssv] = {
                "name": info["name"],
                "lop": info["lop"],
                "avg": avg,
                "rank": rank
            }

    return render_template(
        "index.html",
        page="list",
        classes=classes,
        filtered_students=filtered_students,
        selected_class=selected_class
    )

# --- Câu 3: Trang chi tiết sinh viên ---
@app.route("/students/<mssv>")
def student_detail(mssv):
    if mssv not in STUDENTS:
        abort(404, description=f"Không có sinh viên với MSSV = {mssv}.")
    
    info = STUDENTS[mssv]
    avg, rank = calculate_average_and_rank(info["scores"])
    
    return render_template(
        "index.html",
        page="detail",
        mssv=mssv,
        info=info,
        avg=avg,
        rank=rank
    )

# --- Câu 4: Đường dẫn rút gọn ---
@app.route("/sv/<mssv>")
def short_student_redirect(mssv):
    if mssv not in STUDENTS:
        abort(404, description=f"Không có sinh viên với MSSV = {mssv}.")
    return redirect(url_for('student_detail', mssv=mssv), code=301)

# --- Câu 5: Xuất bảng điểm CSV ---
@app.route("/students/<mssv>/export")
def export_student_csv(mssv):
    if mssv not in STUDENTS:
        abort(404, description=f"Không có sinh viên với MSSV = {mssv}.")
    
    student = STUDENTS[mssv]
    csv_content = "hoc_phan,diem\n"
    for hp, diem in student["scores"].items():
        csv_content += f"{hp},{diem}\n"
        
    response = make_response(csv_content)
    response.headers["Content-Type"] = "text/csv; charset=utf-8"
    response.headers["Content-Disposition"] = f"attachment; filename=diem_{mssv}.csv"
    return response

# --- Câu 6: Tìm kiếm ---
@app.route("/search")
def search_students():
    keyword = request.args.get("q", "").strip()
    matched_students = {}
    
    if keyword:
        keyword_lower = keyword.lower()
        for mssv, info in STUDENTS.items():
            if keyword_lower in info["name"].lower() or keyword_lower in mssv.lower():
                avg, rank = calculate_average_and_rank(info["scores"])
                matched_students[mssv] = {
                    "name": info["name"],
                    "lop": info["lop"],
                    "avg": avg,
                    "rank": rank
                }

    return render_template(
        "index.html",
        page="search",
        keyword=keyword,
        matched_students=matched_students
    )

if __name__ == "__main__":
    app.run(debug=True, port=8000)