# libraryms
##  DỰ ÁN LIBRARYMS V0.1 (KIỂM THỬ API VÀ GẮN TAG)

### 1. Kiểm thử Giao diện Web (Browser URLs)
* `http://127.0.0.1:8000/` $\rightarrow$ Trang chủ (Tổng số lượng sách & số sách sẵn sàng mượn).
* `http://127.0.0.1:8000/books` $\rightarrow$ Danh sách tất cả sách.
* `http://127.0.0.1:8000/books?category=Lập%20trình` $\rightarrow$ Lọc danh sách theo thể loại.
* `http://127.0.0.1:8000/books/1` $\rightarrow$ Chi tiết sách có ID = 1.
* `http://127.0.0.1:8000/books/999` $\rightarrow$ Giao diện HTML lỗi 404 custom.

### 2. Kiểm thử RESTful API (Lệnh `curl`)

* **Lấy danh sách tất cả sách (API):**
  ```bash
  curl -i [http://127.0.0.1:8000/api/books](http://127.0.0.1:8000/api/books)
  ```
  $\rightarrow$ HTTP 200 OK, JSON array danh sách sách.

* **Chi tiết sách theo ID (Thành công):**
  ```bash
  curl -i [http://127.0.0.1:8000/api/books/1](http://127.0.0.1:8000/api/books/1)
  ```
  $\rightarrow$ HTTP 200 OK: `{"id": 1, "title": "Lập trình Python Căn Bản", "author": "Nguyễn Văn A", ...}`

* **Chi tiết sách ID không tồn tại (HTTP 404):**
  ```bash
  curl -i [http://127.0.0.1:8000/api/books/999](http://127.0.0.1:8000/api/books/999)
  ```
  $\rightarrow$ HTTP 404 NOT FOUND: `{"error": "Không tìm thấy sách có ID = 999"}`

* **Lọc sách API theo thể loại:**
  ```bash
  curl -i "[http://127.0.0.1:8000/api/books?category=Lập%20trình](http://127.0.0.1:8000/api/books?category=Lập%20trình)"
  ```
  $\rightarrow$ HTTP 200 OK, JSON array filtered.

---

## V. LỆNH GIT NỘP BÀI VÀ GẮN TAG V0.1

```bash
# 1. Thêm và Commit toàn bộ thay đổi
git add .
git commit -m "feat: complete LibraryMS v0.1 & exercises 1-14 with full testing README"

# 2. Tạo Tag v0.1 cho bài dự án
git tag v0.1

# 3. Đẩy code và Tag v0.1 lên GitHub
git push -u origin main
git push origin v0.1
```
