# FastAPI Todo — Sync vs Async SQLite

Project này dùng để chạy và so sánh hai phiên bản FastAPI:

- `sync_main.py`: dùng `sqlite3` + endpoint `def`
- `async_main.py`: dùng `aiosqlite` + `async def` / `await`
- `benchmark.py`: gửi nhiều request để so sánh hiệu năng

---

## 1. Chạy ứng dụng

### Linux / WSL

Mở 2 terminal.

**Terminal 1 — Sync**

```bash
uv run uvicorn sync_main:app --port 8000
```

Ứng dụng sync chạy tại:

```text
http://127.0.0.1:8000
```

**Terminal 2 — Async**

```bash
uv run uvicorn async_main:app --port 8001
```

Ứng dụng async chạy tại:

```text
http://127.0.0.1:8001
```

### Windows PowerShell

Mở 2 cửa sổ PowerShell.

**PowerShell 1 — Sync**

```powershell
uv run uvicorn sync_main:app --port 8000
```

**PowerShell 2 — Async**

```powershell
uv run uvicorn async_main:app --port 8001
```

---

## 2. Test API bằng curl

Các lệnh bên dưới test bản **sync** ở port `8000`.

Muốn test bản **async**, chỉ cần đổi:

```text
8000 -> 8001
```

### Linux / WSL

#### GET danh sách Todo

```bash
curl http://127.0.0.1:8000/todos
```

#### GET một Todo

```bash
curl http://127.0.0.1:8000/todos/1
```

#### POST tạo Todo

```bash
curl -X POST http://127.0.0.1:8000/todos \
  -H "Content-Type: application/json" \
  -d '{
    "Title": "Lam FastAPI",
    "Description": "Hoc sync va async",
    "Priority": 3,
    "Completed": false
  }'
```

#### PUT cập nhật Todo

```bash
curl -X PUT http://127.0.0.1:8000/todos/1 \
  -H "Content-Type: application/json" \
  -d '{
    "Title": "Lam FastAPI",
    "Description": "Da cap nhat",
    "Priority": 2,
    "Completed": true
  }'
```

#### DELETE Todo

```bash
curl -X DELETE http://127.0.0.1:8000/todos/1
```

#### Liveness

```bash
curl http://127.0.0.1:8000/health/live
```

#### Readiness

```bash
curl http://127.0.0.1:8000/health/ready
```

---

### Windows PowerShell

Nên dùng `curl.exe` để chắc chắn gọi đúng chương trình curl của Windows.

#### GET danh sách Todo

```powershell
curl.exe http://127.0.0.1:8000/todos
```

#### GET một Todo

```powershell
curl.exe http://127.0.0.1:8000/todos/1
```

#### POST tạo Todo

```powershell
curl.exe -X POST http://127.0.0.1:8000/todos `
  -H "Content-Type: application/json" `
  -d '{"Title":"Lam FastAPI","Description":"Hoc sync va async","Priority":3,"Completed":false}'
```

#### PUT cập nhật Todo

```powershell
curl.exe -X PUT http://127.0.0.1:8000/todos/1 `
  -H "Content-Type: application/json" `
  -d '{"Title":"Lam FastAPI","Description":"Da cap nhat","Priority":2,"Completed":true}'
```

#### DELETE Todo

```powershell
curl.exe -X DELETE http://127.0.0.1:8000/todos/1
```

#### Liveness

```powershell
curl.exe http://127.0.0.1:8000/health/live
```

#### Readiness

```powershell
curl.exe http://127.0.0.1:8000/health/ready
```

---

## 3. So sánh Sync và Async

Chạy cả hai server trước:

```text
Sync  -> http://127.0.0.1:8000
Async -> http://127.0.0.1:8001
```

Sau đó chạy benchmark.

### Linux / WSL

```bash
uv run python benchmark.py
```

### Windows PowerShell

```powershell
uv run python benchmark.py
```

### Ý nghĩa các thông số

- `Total requests`: tổng số request gửi đi.
- `Concurrency`: số request tối đa được chạy đồng thời tại một thời điểm.
- `Success`: số request thành công.
- `Errors`: số request bị lỗi.
- `Average response`: thời gian phản hồi trung bình.
- `Requests / second`: số request xử lý được trong một giây.

### Một số kết quả benchmark ổn định

| Concurrency | SQLite3 Sync | aiosqlite Async |
|---:|---:|---:|
| 10 | 42.50 req/s | 45.40 req/s |
| 10 | 35.60 req/s | 44.47 req/s |
| 20 | 40.67 req/s | 41.67 req/s |
| 50 | 38.16 req/s | 48.48 req/s |
| 50 | 50.92 req/s | 53.12 req/s |
| 50 | 44.77 req/s | 48.84 req/s |

Trong các lần chạy ổn định, `aiosqlite` thường có throughput cao hơn `sqlite3`.

Tuy nhiên, async không có nghĩa là mọi request luôn chạy nhanh hơn sync. Lợi ích chính của async là khi chương trình phải chờ I/O, `await` cho phép event loop chuyển sang xử lý coroutine khác thay vì giữ luồng chờ.

Với bài này, SQLite chạy local và câu query khá nhẹ nên mức chênh lệch giữa sync và async không quá lớn.

## 4. Cách dùng `benchmark.py`

`benchmark.py` dùng để gửi nhiều request tới cả hai server và so sánh hiệu năng giữa:

```text
SQLite3 Sync    -> http://127.0.0.1:8000
Aiosqlite Async -> http://127.0.0.1:8001
```

### Bước 1 — Chạy server Sync

Linux / WSL:

```bash
uv run uvicorn sync_main:app --port 8000
```

Windows PowerShell:

```powershell
uv run uvicorn sync_main:app --port 8000
```

### Bước 2 — Chạy server Async

Mở terminal khác.

Linux / WSL:

```bash
uv run uvicorn async_main:app --port 8001
```

Windows PowerShell:

```powershell
uv run uvicorn async_main:app --port 8001
```

### Bước 3 — Chạy benchmark

Mở terminal thứ ba.

Linux / WSL:

```bash
uv run python benchmark.py
```

Windows PowerShell:

```powershell
uv run python benchmark.py
```

### Chỉnh số request và concurrency

Trong `benchmark.py`, phần gọi hàm thường có dạng:

```python
await benchmark(
    name="SQLite3 Sync",
    url="http://127.0.0.1:8000/todos",
    total_requests=100,
    concurrency=10
)
```

và:

```python
await benchmark(
    name="Aiosqlite Async",
    url="http://127.0.0.1:8001/todos",
    total_requests=100,
    concurrency=10
)
```

Trong đó:

- `total_requests=100`: tổng cộng gửi 100 request.
- `concurrency=10`: tối đa 10 request chạy đồng thời tại một thời điểm.

Ví dụ muốn tăng tải:

```python
total_requests=100
concurrency=50
```

hoặc:

```python
total_requests=100
concurrency=100
```

Nên giữ cùng `total_requests` và `concurrency` cho cả Sync và Async để so sánh công bằng.

### Ví dụ kết quả

```text
==============================
SQLite3 Sync
==============================
Total requests       : 100
Concurrency          : 10
Success              : 100
Errors               : 0
Total time           : 2.353 s
Average response     : 0.213 s
Requests / second    : 42.50

==============================
Aiosqlite Async
==============================
Total requests       : 100
Concurrency          : 10
Success              : 100
Errors               : 0
Total time           : 2.203 s
Average response     : 0.206 s
Requests / second    : 45.40
```

Khi đọc kết quả:

- `Success` càng gần `Total requests` càng tốt.
- `Errors` nên bằng `0`.
- `Total time` càng thấp càng tốt.
- `Average response` càng thấp càng tốt.
- `Requests / second` càng cao càng tốt.

Nên chạy benchmark nhiều lần với cùng cấu hình rồi so sánh các kết quả ổn định, thay vì kết luận từ một lần chạy duy nhất.
