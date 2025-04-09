import os
import pytesseract
import platform
from pdf2image import convert_from_bytes
from PIL import Image
import json
from rq import get_current_job  # Lấy job hiện tại từ RQ

# 🧠 Cấu hình Tesseract cho Windows
if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# 📁 Thư mục lưu kết quả và PDF gốc
RESULT_DIR = "job_results"
UPLOADS_DIR = "uploads"
os.makedirs(RESULT_DIR, exist_ok=True)
os.makedirs(UPLOADS_DIR, exist_ok=True)

def ocr_pdf_job(file_bytes: bytes, original_filename: str):
    # 🆔 Lấy job_id thật từ RQ (đồng bộ với Redis)
    job = get_current_job()
    job_id = job.id

    # 💾 Lưu file PDF gốc
    pdf_path = os.path.join(UPLOADS_DIR, f"{job_id}.pdf")
    with open(pdf_path, "wb") as f:
        f.write(file_bytes)
    print(f"📄 [JOB {job_id}] Saved PDF to: {pdf_path}")

    # 🖼️ Chuyển PDF sang ảnh
    images = convert_from_bytes(file_bytes, dpi=200)
    print(f"🖼️ [JOB {job_id}] Total pages: {len(images)}")

    # 🔠 OCR từng trang
    results = []
    for i, image in enumerate(images):
        print(f"🔠 [JOB {job_id}] OCR page {i + 1}")
        text = pytesseract.image_to_string(image, lang="eng")  # Đổi sang 'vie' nếu OCR tiếng Việt
        results.append({
            "page": i + 1,
            "text": text.strip()
        })

    # 💾 Lưu kết quả OCR ra file JSON
    result_path = os.path.join(RESULT_DIR, f"{job_id}.json")
    with open(result_path, "w", encoding="utf-8") as f:
        json.dump({
            "job_id": job_id,
            "original_filename": original_filename,
            "saved_pdf_path": pdf_path,
            "total_pages": len(results),
            "results": results
        }, f, ensure_ascii=False, indent=2)

    print(f"✅ [JOB {job_id}] Done. Result saved to: {result_path}")
    return job_id
