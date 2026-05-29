from datetime import datetime, timedelta
from app.config import DATABASE_URL, OPENAI_MODEL
from app.data_access import pull_sales_data
from app.kpi import build_kpi_tables, calculate_growth
from app.alerts import detect_anomalies, build_alert_message
from app.prompts import build_report_prompt, PROMPT_VERSION
from app.ai_client import generate_ai_narrative
from app.render import save_markdown, export_html, export_pdf
from app.logging_utils import write_report_log


def _previous_period(start_date: str, end_date: str) -> tuple[str, str]:
    start = datetime.fromisoformat(start_date)
    end = datetime.fromisoformat(end_date)
    days = (end - start).days + 1
    prev_end = start - timedelta(days=1)
    prev_start = prev_end - timedelta(days=days-1)
    return prev_start.date().isoformat(), prev_end.date().isoformat()


def generate_report(start_date: str, end_date: str, output_format: str = "pdf") -> dict:
    current = pull_sales_data(DATABASE_URL, start_date, end_date)
    prev_start, prev_end = _previous_period(start_date, end_date)
    previous = pull_sales_data(DATABASE_URL, prev_start, prev_end)

    summary, by_channel, by_sku = build_kpi_tables(current)
    growth = calculate_growth(current, previous)
    alert_df = detect_anomalies(growth)

    prompt = build_report_prompt(summary, by_channel, by_sku, growth, alert_df, start_date, end_date)
    report_md = generate_ai_narrative(prompt)

    report_id = f"weekly_sales_{start_date}_{end_date}".replace("/", "-")
    md_path = save_markdown(report_md, report_id)
    html_path = export_html(report_md, report_id, metadata={"start_date": start_date, "end_date": end_date})
    pdf_path = export_pdf(html_path, report_id) if output_format in ["pdf", "all"] else None
    alert_message = build_alert_message(alert_df, str(pdf_path or html_path))

    log_path = write_report_log(report_id, {
        "start_date": start_date,
        "end_date": end_date,
        "previous_start_date": prev_start,
        "previous_end_date": prev_end,
        "model": OPENAI_MODEL,
        "prompt_version": PROMPT_VERSION,
        "row_count": len(current),
        "alert_count": len(alert_df),
        "status": "success"
    })

    return {
        "status": "success",
        "report_id": report_id,
        "markdown": str(md_path),
        "html": str(html_path),
        "pdf": str(pdf_path) if pdf_path else None,
        "log": str(log_path),
        "alert_message": alert_message,
        "summary_preview": report_md[:700]
    }
