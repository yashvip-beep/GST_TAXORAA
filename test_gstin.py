import json
from pathlib import Path

from gstin_engine import checksum_char, format_details_text, validate_gstin
from gstin_pdf import build_gstin_report

NEWS = Path("/content/gst-rate-finder/data/news.json")


def test_known_valid_gstin_passes_checksum():
    res = validate_gstin("27AAPFU0939F1ZV")
    assert res["valid"] is True
    assert res["state"] == "Maharashtra"


def test_wrong_check_character_fails():
    res = validate_gstin("27AAPFU0939F1ZW")
    assert res["valid"] is False
    assert "typo" in res["message"]


def test_wrong_length_fails():
    res = validate_gstin("27AAPFU0939F1Z")
    assert res["valid"] is False
    assert "15 characters" in res["message"]


def test_spaces_and_lowercase_are_normalised():
    assert validate_gstin(" 27aapfu0939f1zv ")["valid"] is True


def test_bad_format_fails():
    assert validate_gstin("ABAAPFU0939F1ZV")["valid"] is False


def test_checksum_char_matches_known_example():
    assert checksum_char("27AAPFU0939F1Z") == "V"


def test_details_text_without_details_still_works():
    text = format_details_text("27AAPFU0939F1ZV", "Maharashtra", None)
    assert text.startswith("GSTIN: 27AAPFU0939F1ZV")


def test_pdf_report_is_pdf_bytes():
    pdf = build_gstin_report("27AAPFU0939F1ZV", "Maharashtra", None,
                             "Format valid", "Test disclaimer", "18 Nov 2026")
    assert pdf.startswith(b"%PDF")


def test_news_file_has_required_fields():
    data = json.loads(NEWS.read_text(encoding="utf-8"))
    required = {"id", "date", "effective", "category", "title", "summary", "reference", "source_url"}
    assert data["items"]
    for item in data["items"]:
        assert required <= item.keys()
