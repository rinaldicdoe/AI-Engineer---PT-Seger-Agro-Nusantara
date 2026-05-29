import json, time
from pathlib import Path
from app.config import OUTPUT_DIR


def write_report_log(report_id: str, payload: dict) -> Path:
    log_dir = OUTPUT_DIR / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    payload = dict(payload)
    payload["report_id"] = report_id
    payload["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")
    path = log_dir / f"{report_id}.json"
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return path
