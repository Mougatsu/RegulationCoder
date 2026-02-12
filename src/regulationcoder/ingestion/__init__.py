"""Document ingestion pipeline — PDF, HTML, OCR, language detection, normalization."""

from regulationcoder.ingestion.html_scraper import HTMLScraper
from regulationcoder.ingestion.language_detector import LanguageDetector
from regulationcoder.ingestion.normalizer import DocumentNormalizer
from regulationcoder.ingestion.ocr_fallback import OCRFallback
from regulationcoder.ingestion.pdf_processor import PDFProcessor

__all__ = [
    "PDFProcessor",
    "HTMLScraper",
    "OCRFallback",
    "LanguageDetector",
    "DocumentNormalizer",
]
