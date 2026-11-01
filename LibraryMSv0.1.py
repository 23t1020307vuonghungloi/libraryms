from flask import Flask, abort, jsonify, request, url_for
from markupsafe import escape

app = Flask(__name__)
app.json.ensure_ascii = False  # Hiển thị tiếng Việt trong JSON đúng chuẩn

# --- 1. DANH SÁCH SÁCH (BOOKS >= 4 cuốn) ---
BOOKS = [
    {
        "id": 1,
        "title": "Lập trình Python Căn Bản",
        "author": "Nguyễn Văn A",
        "year": 2023,
        "category": "Lập trình",
        "available": True
    },
    {
        "id": 2,
        "title": "Flask Web Development",
        "author": "Trần Thị B",
        "year": 2024,
        "category": "Lập trình",
        "available": True
    },
    {
        "id": 3,
        "title": "Cơ Sở Dữ Liệu Quan Hệ",
        "author": "Lê Văn C",
        "year": 2022,
        "category": "Cơ sở dữ liệu",
        "available": False
    },
    {
        "id": 4,
        "title": "Cấu Trúc Dữ Liệu và Giải Thuật",
        "author": "Phạm Văn D",
        "year": 2021,
        "category": "Lập trình",
        "available": True
    },
    {
        "id": 5,
        "title": "Mạng Máy Tính Căn Bản",
        "author": "Hoàng Văn E",
        "year": 2020,
        "category": "Mạng máy tính",
        "available": False
    }
]

def find_book(book_id):
    """Tìm sách theo ID."""
    for book in BOOKS:
        if book["id"] == book_id:
            return book
    return None

# --- 6 & 7. KHUNG TRANG LAYOUT VÀ MENU CHUNG (DÙNG url_for VÀ escape) ---
def layout(title, body):
    return f"""<!doctype html>
<html lang="vi">
<head>
    <meta charset="utf-8">
    <title>{escape(title)} - LibraryMS</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }}
        nav a {{ margin-right: 15px; text-decoration: none; color: #0066cc; font-weight: bold; }}
        table {{ border-collapse: collapse; width: 100%; margin-top: 15px; }}
        th, td {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        .badge-success {{ color: green; font-weight: bold; }}
        .badge-danger {{ color: red; font-weight: bold; }}
        .filter-bar {{ margin: 15px 0; padding: 10px; background-color: #f9f9f9; border: 1px solid #eee; }}
        .filter-bar a {{ margin-right: 8px; text-decoration: none; }}
    </style>
</head>
<body>
    <nav>
        <a href="{url_for('index')}">Trang chủ</a> |
        <a href="{url_for('list_books')}">Danh sách sách</a> |
        <a href="{url_for('api_list_books')}">API Books</a>
    </nav>
    <hr>
    {body}
</body>
</html>"""


# --- 2. TRANG CHỦ / ---
@app.route("/")
def index():
    total_books = len(BOOKS)
    available_books = sum(1 for b in BOOKS if b["available"])
    
    body = f"""
    <h1>Hệ thống Quản lý Thư viện (LibraryMS)</h1>
    <p>Thống kê kho sách hiện tại:</p>
    <ul>
        <li><strong>Tổng số đầu sách:</strong> {total_books} cuốn</li>
        <li><strong>Số sách sẵn sàng cho mượn:</strong> {available_books} cuốn</li>
    </ul>
    <p><a href="{url_for('list_books')}">→ Xem danh sách chi tiết</a></p>
    """
    return layout("Trang chủ", body)


# --- 3. BẢNG SÁCH VÀ LỌC THEO THỂ LOẠI /books ---
@app.route("/books")
def list_books():
    selected_category = request.args.get("category", "").strip()
    
    # Lấy các thể loại duy nhất
    categories = sorted(list(set(b["category"] for b in BOOKS)))
    
    # Thanh liên kết theo thể loại
    filter_links = [f'<a href="{url_for("list_books")}">Tất cả</a>']
    for cat in categories:
        link = url_for("list_books", category=cat)
        filter_links.append(f'<a href="{link}">[{escape(cat)}]</a>')
        
    filter_bar = f'<div class="filter-bar"><strong>Lọc theo thể loại:</strong> {" | ".join(filter_links)}</div>'
    
    # Lọc danh sách
    if selected_category:
        filtered_books = [b for b in BOOKS if b["category"].lower() == selected_category.lower()]
        heading = f'Danh sách sách - Thể loại: "{escape(selected_category)}"'
    else:
        filtered_books = BOOKS
        heading = "Danh sách tất cả sách"
        
    # Tạo bảng HTML
    rows = []
    for b in filtered_books:
        detail_url = url_for("book_detail", book_id=b["id"])
        cat_url = url_for("list_books", category=b["category"])
        status = '<span class="badge-success">Sẵn sàng</span>' if b["available"] else '<span class="badge-danger">Đã mượn</span>'
        
        rows.append(f"""
        <tr>
            <td>{b["id"]}</td>
            <td><a href="{detail_url}"><strong>{escape(b["title"])}</strong></a></td>
            <td>{escape(b["author"])}</td>
            <td>{b["year"]}</td>
            <td><a href="{cat_url}">{escape(b["category"])}</a></td>
            <td>{status}</td>
        </tr>
        """)
        
    table_html = f"""
    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>Tên sách</th>
                <th>Tác giả</th>
                <th>Năm XB</th>
                <th>Thể loại</th>
                <th>Trạng thái</th>
            </tr>
        </thead>
        <tbody>
            {"".join(rows) if rows else '<tr><td colspan="6">Không tìm thấy sách nào.</td></tr>'}
        </tbody>
    </table>
    """
    return layout("Danh sách sách", f"<h1>{heading}</h1>{filter_bar}{table_html}")


# --- 4. CHI TIẾT SÁCH /books/<int:book_id> ---
@app.route("/books/<int:book_id>")
def book_detail(book_id):
    book = find_book(book_id)
    if not book:
        body = f"""
        <h2>404 - Không tìm thấy sách</h2>
        <p>Không có sách với ID = {book_id}</p>
        <p><a href="{url_for('list_books')}">← Quay lại danh sách sách</a></p>
        """
        return layout("Không tìm thấy sách", body), 404
        
    status = '<span class="badge-success">Sẵn sàng cho mượn</span>' if book["available"] else '<span class="badge-danger">Đã được mượn</span>'
    cat_url = url_for("list_books", category=book["category"])
    
    body = f"""
    <h1>{escape(book["title"])}</h1>
    <ul>
        <li><strong>Mã sách (ID):</strong> {book["id"]}</li>
        <li><strong>Tác giả:</strong> {escape(book["author"])}</li>
        <li><strong>Năm xuất bản:</strong> {book["year"]}</li>
        <li><strong>Thể loại:</strong> <a href="{cat_url}">{escape(book["category"])}</a></li>
        <li><strong>Trạng thái:</strong> {status}</li>
    </ul>
    <p><a href="{url_for('list_books')}">← Quay lại danh sách sách</a></p>
    """
    return layout(book["title"], body)


# --- 5. API ENDPOINTS (/api/books & /api/books/<int:book_id>) ---
@app.get("/api/books")
def api_list_books():
    category = request.args.get("category", "").strip()
    if category:
        filtered = [b for b in BOOKS if b["category"].lower() == category.lower()]
        return jsonify(filtered)
    return jsonify(BOOKS)

@app.get("/api/books/<int:book_id>")
def api_book_detail(book_id):
    book = find_book(book_id)
    if not book:
        return jsonify({"error": f"Không có sách với ID = {book_id}"}), 404
    return jsonify(book)


# --- 6. TRANG 404 TUỲ BIẾN CÓ MENU CHUNG ---
@app.errorhandler(404)
def page_not_found(error):
    msg = getattr(error, "description", "Trang hoặc tài nguyên bạn tìm kiếm không tồn tại.")
    body = f"""
    <h1>404 - Không Tìm Thấy Trang</h1>
    <p>{escape(str(msg))}</p>
    <p><a href="{url_for('index')}">→ Quay về trang chủ</a></p>
    """
    return layout("404 Not Found", body), 404


if __name__ == "__main__":
    app.run(debug=True, port=8000)