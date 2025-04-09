### main.py
from fastapi import FastAPI, UploadFile, File
from redis import Redis
from rq import Queue
import uuid
import os
import json
from tasks import ocr_pdf_job, RESULT_DIR

app = FastAPI()
redis_conn = Redis(host="redis", port=6379)
queue = Queue(connection=redis_conn)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/submit-ocr-job/")
async def submit_ocr_job(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        return {"error": "Chỉ hỗ trợ file .pdf"}

    file_bytes = await file.read()
    job = queue.enqueue(ocr_pdf_job, args=(file_bytes, file.filename), timeout=None)

    return {"job_id": job.id}

@app.get("/job-status/{job_id}")
def job_status(job_id: str):
    from rq.job import Job
    try:
        job = Job.fetch(job_id, connection=redis_conn)
        return {"job_id": job.id, "status": job.get_status()}
    except:
        return {"error": "Không tìm thấy job"}

@app.get("/job-result/{job_id}")
def job_result(job_id: str):
    result_file = os.path.join(RESULT_DIR, f"{job_id}.json")
    if not os.path.exists(result_file):
        return {"error": "Kết quả chưa sẵn sàng hoặc không tồn tại"}

    with open(result_file, "r", encoding="utf-8") as f:
        return json.load(f)