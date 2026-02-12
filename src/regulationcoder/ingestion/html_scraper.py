"""HTML scraping for regulation documents published on the web."""

import logging
from pathlib import Path

import httpx
from bs4 import BeautifulSoup, Tag

from regulationcoder.core.exceptions import IngestionError

logger = logging.getLogger(__name__)

# Tags that almost never contain regulation body text.
_STRIP_TAGS = frozenset({
    "nav",
    "footer",
    "header",
    "aside",
    "script",
    "style",
    "noscript",
    "iframe",
    "form",
    "svg",
    "img",
    "button",
    "input",
    "select",
    "textarea",
})

# CSS classes / ids commonly used for navigation and chrome.
_STRIP_PATTERNS = [
    "nav",
    "footer",
    "header",
    "sidebar",
    "breadcrumb",
    "menu",
    "cookie",
    "banner",
    "toolbar",
    "pagination",
    "social",
    "share",
    "comment",
    "advertisement",
    "ad-",
]


class HTMLScraper:
    """Fetch and extract readable text from HTML regulation pages.

    Handles both remote URLs (via ``httpx``) and local HTML files.
    Non-content elements (navigation, footer, scripts, etc.) are stripped
    before extraction.
    """

    DEFAULT_TIMEOUT = 30.0  # seconds
    DEFAULT_USER_AGENT = (
        "Mozilla/5.0 (compatible; RegulationCoder/0.1; +https://github.com/regulationcoder)"
    )

    def __init__(
        self,
        timeout: float = DEFAULT_TIMEOUT,
        user_agent: str = DEFAULT_USER_AGENT,
    ) -> None:
        self.timeout = timeout
        self.user_agent = user_agent

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def scrape_url(self, url: str) -> str:
        """Fetch an HTML page from *url* and return the article text.

        Parameters
        ----------
        url:
            Fully-qualified URL (``https://…``).

        Returns
        -------
        str
            Cleaned text extracted from the page.

        Raises
        ------
        IngestionError
            On network or parsing failures.
        """
        logger.info("Scraping URL: %s", url)
        try:
            with httpx.Client(
                timeout=self.timeout,
                follow_redirects=True,
                headers={"User-Agent": self.user_agent},
            ) as client:
                response = client.get(url)
                response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise IngestionError(
                f"HTTP {exc.response.status_code} when fetching {url}"
            ) from exc
        except httpx.RequestError as exc:
            raise IngestionError(f"Request failed for {url}: {exc}") from exc

        return self._extract_text(response.text)

    def scrape_file(self, file_path: str | Path) -> str:
        """Read a local HTML file and return the article text.

        Parameters
        ----------
        file_path:
            Path to the HTML file on disk.

        Returns
        -------
        str
            Cleaned text extracted from the file.

        Raises
        ------
        IngestionError
            If the file cannot be read or parsed.
        """
        path = Path(file_path)
        if not path.exists():
            raise IngestionError(f"HTML file not found: {path}")

        logger.info("Scraping local file: %s", path)
        try:
            html = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            raise IngestionError(f"Failed to read HTML file: {exc}") from exc

        return self._extract_text(html)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _extract_text(self, html: str) -> str:
        """Parse *html* and return cleaned body text."""
        soup = BeautifulSoup(html, "html.parser")

        # Remove known non-content tags entirely.
        for tag_name in _STRIP_TAGS:
            for tag in soup.find_all(tag_name):
                tag.decompose()

        # Remove elements whose class or id matches common chrome patterns.
        for element in soup.find_all(True):
            if not isinstance(element, Tag):
                continue
            class_list = " ".join(element.get("class", []))
            element_id = element.get("id", "") or ""
            combined = f"{class_list} {element_id}".lower()
            if any(pat in combined for pat in _STRIP_PATTERNS):
                element.decompose()

        # Prefer <article> or <main> if they exist; fall back to <body>.
        content_root = (
            soup.find("article")
            or soup.find("main")
            or soup.find("body")
            or soup
        )

        text = content_root.get_text(separator="\n", strip=True)

        # Collapse excessive blank lines.
        lines = [line.strip() for line in text.splitlines()]
        cleaned = "\n".join(line for line in lines if line)

        logger.info("Extracted %d characters from HTML", len(cleaned))
        return cleaned
