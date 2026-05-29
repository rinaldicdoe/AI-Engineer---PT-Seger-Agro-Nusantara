from app.report_service import generate_report


def test_generate_report_smoke():
    result = generate_report("2026-05-11", "2026-05-17", "html")
    assert result["status"] == "success"
    assert result["markdown"].endswith(".md")
    assert result["html"].endswith(".html")
