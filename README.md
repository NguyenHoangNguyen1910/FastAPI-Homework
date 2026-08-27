# FastAPI Todo API

Một REST API quản lý công việc đơn giản được xây dựng bằng **FastAPI**, **Pydantic v2** và **SQLite**.

Project này dùng để thực hành các kiến thức backend cơ bản như:

- CRUD
- Validation dữ liệu với Pydantic
- Dependency Injection với `Depends`
- SQLite
- Lifespan
- CORS Middleware
- Liveness và Readiness Health Check

---

## Tính năng

- Tạo Todo mới
- Lấy danh sách toàn bộ Todo
- Lấy chi tiết Todo theo ID
- Cập nhật Todo
- Xóa Todo
- Validation dữ liệu đầu vào
- Lưu dữ liệu bằng SQLite
- Quản lý kết nối database bằng `Depends`
- Khởi tạo database bằng `lifespan`
- Cấu hình CORS
- Health check với `/health/live` và `/health/ready`

---

## Công nghệ sử dụng

- Python
- FastAPI
- Pydantic v2
- SQLite
- Uvicorn

---

## Cấu trúc project

```text
.
├── main.py
├── todos.db
└── README.md
```

> `todos.db` sẽ được tạo tự động khi ứng dụng khởi động nếu file chưa tồn tại.

---

# Cài đặt

## 1. Clone repository

```bash
git clone <repository-url>
cd <repository-folder>
```

---

## 2. Cài dependencies

Cài trực tiếp các thư viện cần thiết trên máy:

### Windows

```powershell
pip install fastapi uvicorn
```

Nếu máy có nhiều phiên bản Python, có thể dùng:

```powershell
python -m pip install fastapi uvicorn
```

### Linux / WSL / macOS

```bash
pip install fastapi uvicorn
```

Nếu cần:

```bash
python3 -m pip install fastapi uvicorn
```

---

# Chạy ứng dụng

Giả sử file FastAPI của project là:

```text
main.py
```

Chạy server bằng:

### Windows

```powershell
uvicorn main:app --reload
```

### Linux / WSL / macOS

```bash
uvicorn main:app --reload
```

Nếu chạy thành công, API mặc định có địa chỉ:

```text
http://127.0.0.1:8000
```

---

# API Documentation

FastAPI tự động sinh tài liệu API.

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

OpenAPI JSON:

```text
http://127.0.0.1:8000/openapi.json
```

---

# API Endpoints

| Method | Endpoint | Chức năng |
|---|---|---|
| GET | `/` | Kiểm tra API cơ bản |
| POST | `/todos` | Tạo Todo mới |
| GET | `/todos` | Lấy toàn bộ Todo |
| GET | `/todos/{todo_id}` | Lấy Todo theo ID |
| PUT | `/todos/{todo_id}` | Cập nhật Todo |
| DELETE | `/todos/{todo_id}` | Xóa Todo |
| GET | `/health/live` | Liveness check |
| GET | `/health/ready` | Readiness check |

---

# Todo Schema

Request body có dạng:

```json
{
  "Title": "Hoc FastAPI",
  "Description": "Hoc CRUD voi SQLite",
  "Priority": 3,
  "Completed": false
}
```

| Field | Kiểu dữ liệu | Bắt buộc | Mặc định |
|---|---|---|---|
| `Title` | `str` | Có | - |
| `Description` | `str \| null` | Không | `null` |
| `Priority` | `int` | Không | `1` |
| `Completed` | `bool` | Không | `false` |

---

# Validation

## Title

`Title` không được để trống hoặc chỉ chứa khoảng trắng.

Không hợp lệ:

```json
{
  "Title": "   "
}
```

Hợp lệ:

```json
{
  "Title": "Hoc FastAPI"
}
```

Khoảng trắng ở đầu và cuối `Title` sẽ được loại bỏ bằng:

```python
return value.strip()
```

---

## Priority và Description

Khi:

```text
Priority >= 4
```

thì `Description` bắt buộc phải có.

Không hợp lệ:

```json
{
  "Title": "Task quan trong",
  "Priority": 5
}
```

Hợp lệ:

```json
{
  "Title": "Task quan trong",
  "Description": "Phai hoan thanh som",
  "Priority": 5
}
```

---

# Test API bằng curl

Đảm bảo FastAPI đang chạy trước khi test:

```bash
uvicorn main:app --reload
```

Sau đó mở một terminal khác để chạy `curl`.

---

## 1. GET root

Lệnh này có thể dùng trên cả Windows và Linux:

```bash
curl http://127.0.0.1:8000/
```

Response:

```json
{
  "message": "Hello fastapi"
}
```

---

## 2. POST - Tạo Todo

### Windows PowerShell

```powershell
curl.exe -X POST `
  http://127.0.0.1:8000/todos `
  -H "Content-Type: application/json" `
  -d "{\"Title\":\"Hoc FastAPI\",\"Description\":\"Hoc CRUD\",\"Priority\":3,\"Completed\":false}"
```

### Linux / WSL / macOS

```bash
curl -X POST \
  http://127.0.0.1:8000/todos \
  -H "Content-Type: application/json" \
  -d '{
    "Title": "Hoc FastAPI",
    "Description": "Hoc CRUD",
    "Priority": 3,
    "Completed": false
  }'
```

Response hiện tại:

```json
{
  "message": "Cretae sucessully"
}
```

---

## 3. GET - Lấy toàn bộ Todo

Có thể dùng trên cả Windows và Linux:

```bash
curl http://127.0.0.1:8000/todos
```

Ví dụ response:

```json
[
  {
    "Id": 1,
    "Title": "Hoc FastAPI",
    "Description": "Hoc CRUD",
    "Priority": 3,
    "Completed": 0
  }
]
```

> SQLite lưu boolean dưới dạng số nguyên: `false = 0`, `true = 1`.

---

## 4. GET - Lấy Todo theo ID

```bash
curl http://127.0.0.1:8000/todos/1
```

Ví dụ response:

```json
{
  "Id": 1,
  "Title": "Hoc FastAPI",
  "Description": "Hoc CRUD",
  "Priority": 3,
  "Completed": 0
}
```

Nếu không tìm thấy:

```json
{
  "message": "Todo not found"
}
```

---

## 5. PUT - Cập nhật Todo

### Windows PowerShell

```powershell
curl.exe -X PUT `
  http://127.0.0.1:8000/todos/1 `
  -H "Content-Type: application/json" `
  -d "{\"Title\":\"Hoc FastAPI nang cao\",\"Description\":\"Hoc PUT\",\"Priority\":4,\"Completed\":true}"
```

### Linux / WSL / macOS

```bash
curl -X PUT \
  http://127.0.0.1:8000/todos/1 \
  -H "Content-Type: application/json" \
  -d '{
    "Title": "Hoc FastAPI nang cao",
    "Description": "Hoc PUT",
    "Priority": 4,
    "Completed": true
  }'
```

Response:

```json
{
  "message": "Updated successfully"
}
```

---

## 6. DELETE - Xóa Todo

Lệnh này có thể dùng trên cả Windows và Linux:

```bash
curl -X DELETE http://127.0.0.1:8000/todos/1
```

Response:

```json
{
  "message": "Deleted successfully"
}
```

---

# Database

Project sử dụng SQLite với file:

```text
todos.db
```

Table được tạo bằng:

```sql
CREATE TABLE IF NOT EXISTS ToDos(
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Title TEXT NOT NULL,
    Description TEXT,
    Priority INTEGER NOT NULL,
    Completed INTEGER NOT NULL
);
```

Database được tạo khi ứng dụng startup thông qua `lifespan`.

---

# Dependency Injection

Database connection được truyền vào endpoint bằng:

```python
Depends(get_db)
```

Flow:

```text
Request
   ↓
FastAPI
   ↓
Depends(get_db)
   ↓
Mở SQLite connection
   ↓
yield connection
   ↓
Endpoint xử lý request
   ↓
Request kết thúc
   ↓
finally
   ↓
Đóng connection
```

---

# CORS

Project sử dụng `CORSMiddleware`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)
```

Cấu hình hiện tại:

- Cho phép mọi origin
- Cho phép mọi HTTP method
- Cho phép mọi request header
- Không cho phép credentials

Trong môi trường production nên giới hạn `allow_origins` về các frontend được tin cậy.

---

# Health Check

## Liveness

Endpoint:

```text
GET /health/live
```

Test:

```bash
curl http://127.0.0.1:8000/health/live
```

Response:

```json
{
  "status": "alive"
}
```

Liveness dùng để kiểm tra ứng dụng có đang chạy hay không.

---

## Readiness

Endpoint:

```text
GET /health/ready
```

Test:

```bash
curl http://127.0.0.1:8000/health/ready
```

Response:

```json
{
  "status": "ready"
}
```

Readiness thực hiện:

```sql
SELECT 1
```

để kiểm tra database có thể được truy cập.

Có thể hiểu:

```text
Liveness
    ↓
Ứng dụng còn sống không?

Readiness
    ↓
Ứng dụng đã sẵn sàng phục vụ request chưa?
```

---

# Random Test Data

Project có hàm:

```python
add_random_todos()
```

để thêm 5 Todo ngẫu nhiên.

Hiện tại đang bị comment:

```python
# add_random_todos()
```

Nếu bật lại:

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()
    add_random_todos()
    yield
```

thì mỗi lần ứng dụng startup sẽ thêm 5 record mới.

---

# Reset dữ liệu

Xóa toàn bộ Todo:

```sql
DELETE FROM ToDos;
```

Reset `AUTOINCREMENT`:

```sql
DELETE FROM ToDos;
DELETE FROM sqlite_sequence WHERE name = 'ToDos';
```

Sau đó Todo mới sẽ bắt đầu lại từ:

```text
Id = 1
```

---

# Khác biệt curl giữa Windows và Linux

Với lệnh `curl` đơn giản:

```bash
curl http://127.0.0.1:8000/todos
```

có thể dùng gần như giống nhau.

Điểm khác biệt chính khi viết lệnh nhiều dòng:

| Môi trường | Ký tự xuống dòng |
|---|---|
| Windows PowerShell | `` ` `` |
| Linux / WSL / macOS | `\` |
| Windows CMD | `^` |

Trong README này sử dụng:

- **Windows PowerShell** cho Windows
- **Bash** cho Linux / WSL / macOS

---

# Một số điểm có thể cải thiện

Project hiện tại phục vụ mục đích học tập.

Có thể cải thiện thêm:

- Trả `404 Not Found` bằng `HTTPException`
- Tạo schema riêng cho update
- Thêm `PATCH`
- Thêm pagination
- Thêm filter
- Thêm test với `pytest`
- Thêm logging
- Thêm Docker
- Giới hạn CORS origin khi deploy production

Ví dụ thay:

```python
if row == None:
    return {"message": "Todo not found"}
```

bằng:

```python
from fastapi import HTTPException

if row is None:
    raise HTTPException(
        status_code=404,
        detail="Todo not found"
    )
```

---

# Ghi chú

Trong code hiện tại:

```python
if self.Priority >= 4 and not self.Description:
```

nhưng message validation lại ghi:

```text
Priority > 4
```

Điều kiện thực tế là:

```text
Priority >= 4
```

Ngoài ra:

```text
Cretae sucessully
```

có thể sửa thành:

```text
Created successfully
```

---

# License

Project được sử dụng cho mục đích học tập và thực hành.
