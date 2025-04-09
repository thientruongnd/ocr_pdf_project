
# Project Title

A brief description of what this project does and who it's for

# FastAPI PDF OCR
Ứng dụng FastAPI dùng để OCR file PDF:
- Chuyển mỗi trang PDF sang ảnh
- Thực hiện OCR để trích xuất văn bản
- Trả về kết quả từng trang

## Cài đặt

```
Bước 1: Kiểm tra Python 3.11 đã cài chưa
 ```bash
    py -3.11 --version
```
🛠 Bước 2: Tạo virtual environment (venv) với Python 3.11
```bash
py -3.11 -m venv venv
```
Sau đó kích hoạt:

```bash
.\venv\Scripts\activate
```
📦 Bước 3: Cài lại dependencies
```bash
pip install -r requirements.txt
```
🚀 Chạy FastAPI
```bash
uvicorn main:app --reload
python worker.py
```
Dùng docker build product
```bash
docker-compose up -d --build
```
Rebuild container 
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```
