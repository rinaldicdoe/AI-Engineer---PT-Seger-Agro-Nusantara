from pathlib import Path
from jinja2 import Template
import markdown
from app.config import OUTPUT_DIR, REPORT_OWNER

HTML_TEMPLATE_PATH = Path(__file__).resolve().parents[1] / "templates" / "report_template.html"


def save_markdown(report_md: str, report_id: str) -> Path:
    out_dir = OUTPUT_DIR / "markdown"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{report_id}.md"
    path.write_text(report_md, encoding="utf-8")
    return path


def export_html(report_md: str, report_id: str, metadata: dict | None = None) -> Path:
    metadata = metadata or {}
    template = Template(HTML_TEMPLATE_PATH.read_text(encoding="utf-8"))
    html_body = markdown.markdown(report_md, extensions=["tables", "fenced_code"])
    html = template.render(content=html_body, owner=REPORT_OWNER, metadata=metadata)
    out_dir = OUTPUT_DIR / "html"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{report_id}.html"
    path.write_text(html, encoding="utf-8")
    return path


def export_pdf(html_path: Path, report_id: str) -> Path | None:
    out_dir = OUTPUT_DIR / "pdf"
    out_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = out_dir / f"{report_id}.pdf"
    try:
        from weasyprint import HTML
        HTML(filename=str(html_path)).write_pdf(str(pdf_path))
        return pdf_path
    except Exception as exc:
        # WeasyPrint kadang butuh dependency OS tambahan. HTML tetap menjadi output final sementara.
        print(f"PDF export skipped: {exc}")
        return None
