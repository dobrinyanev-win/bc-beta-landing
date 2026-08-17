from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "public" / "index.html"
EXPECTED_TITLE = "Blend Calculator Beta — 21 места"
EXPECTED_CANONICAL = "https://bc-beta.beyourwealthyness.com/"
EXPECTED_ENROLLMENT = "https://beyourwealthyness.newzenler.com/courses/bc-beta/buy"
PLACEHOLDER = "__ZENLER_ENROLLMENT_URL__"


class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.lang = None
        self.viewport = None
        self.in_title = False
        self.title_parts = []
        self.title_count = 0
        self.canonical = None
        self.canonical_count = 0
        self.favicon = None
        self.favicon_count = 0
        self.og_url = None
        self.og_url_count = 0
        self.og_locale = None
        self.og_locale_count = 0
        self.ctas = []
        self.main_depth = 0
        self.main_count = 0

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "html":
            self.lang = values.get("lang")
        elif tag == "meta" and values.get("name") == "viewport":
            self.viewport = values.get("content")
        elif tag == "meta" and values.get("property") == "og:url":
            self.og_url = values.get("content")
            self.og_url_count += 1
        elif tag == "meta" and values.get("property") == "og:locale":
            self.og_locale = values.get("content")
            self.og_locale_count += 1
        elif tag == "link" and "canonical" in (values.get("rel") or "").split():
            self.canonical = values.get("href")
            self.canonical_count += 1
        elif tag == "link" and "icon" in (values.get("rel") or "").split():
            self.favicon = values.get("href")
            self.favicon_count += 1
        elif tag == "title":
            self.in_title = True
            self.title_count += 1
        elif tag == "main":
            self.main_count += 1
            self.main_depth += 1
        elif tag == "a" and "bc-button" in (values.get("class") or "").split():
            self.ctas.append(values.get("href") or "")

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        elif tag == "main":
            self.main_depth -= 1

    def handle_data(self, data):
        if self.in_title:
            self.title_parts.append(data)

    @property
    def title(self):
        return "".join(self.title_parts).strip()


def main():
    text = INDEX.read_text(encoding="utf-8")
    parser = Parser()
    parser.feed(text)
    checks = {
        "doctype": text.lstrip().lower().startswith("<!doctype html>"),
        "lang_bg": parser.lang == "bg",
        "viewport": parser.viewport == "width=device-width, initial-scale=1",
        "one_exact_title": parser.title_count == 1 and parser.title == EXPECTED_TITLE,
        "one_balanced_main": parser.main_count == 1 and parser.main_depth == 0,
        "one_exact_canonical": parser.canonical_count == 1 and parser.canonical == EXPECTED_CANONICAL,
        "one_exact_og_url": parser.og_url_count == 1 and parser.og_url == EXPECTED_CANONICAL,
        "one_bg_locale": parser.og_locale_count == 1 and parser.og_locale == "bg_BG",
        "one_favicon": parser.favicon_count == 1 and parser.favicon == "/favicon.svg" and (ROOT / "public" / "favicon.svg").is_file(),
        "two_exact_ctas": parser.ctas == [EXPECTED_ENROLLMENT, EXPECTED_ENROLLMENT],
        "no_placeholder": PLACEHOLDER not in text,
        "no_zenler_full_bleed": "margin-left: -50vw" not in text,
        "reduced_motion": "@media (prefers-reduced-motion: reduce)" in text,
    }
    for name, ok in checks.items():
        print(f"{'PASS' if ok else 'FAIL'} {name}")
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
