from redis import Redis
from rq import Queue, SimpleWorker
from rq.timeouts import BaseDeathPenalty
from tasks import ocr_pdf_job

# Tắt cơ chế timeout bằng DummyDeathPenalty
class DummyDeathPenalty(BaseDeathPenalty):
    def __enter__(self): pass
    def __exit__(self, *exc_info): pass

redis_conn = Redis(host="localhost", port=6379)
queue = Queue(connection=redis_conn)

if __name__ == "__main__":
    SimpleWorker.death_penalty_class = DummyDeathPenalty  # 🛡 Bắt buộc trên Windows
    worker = SimpleWorker([queue], connection=redis_conn)
    print("✅ SimpleWorker running safely on Windows (no SIGALRM)")
    worker.work()
