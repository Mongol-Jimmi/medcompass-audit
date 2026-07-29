from html.parser import HTMLParser
from pathlib import Path
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
HTML_FILES = [
    ROOT / "index.html",
    ROOT / "sample.html",
    ROOT / "privacy.html",
    ROOT / "terms.html",
    ROOT / "guides" / "gpa-formulas.html",
]


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            href = dict(attrs).get("href")
            if href:
                self.links.append(href)


class SiteTests(unittest.TestCase):
    def test_internal_links_resolve(self):
        for page in HTML_FILES:
            parser = LinkParser()
            parser.feed(page.read_text(encoding="utf-8"))
            for href in parser.links:
                if href.startswith(("http", "mailto:", "#")):
                    continue
                target = (page.parent / href.split("#", 1)[0]).resolve()
                self.assertTrue(target.exists(), f"{page.name}: missing {href}")

    def test_sample_contains_no_prior_applicant_data(self):
        sample = (ROOT / "sample.html").read_text(encoding="utf-8").lower()

        self.assertIn("alex example", sample)
        self.assertNotIn("international_applicant_abroad", sample)

    def test_homepage_has_offer_and_disclosures(self):
        homepage = (ROOT / "index.html").read_text(encoding="utf-8")

        self.assertIn("CAD $79", homepage)
        self.assertIn("48-hour", homepage)
        self.assertIn("Not an admissions prediction", homepage)
        self.assertIn("65 official admissions sources", homepage)
        self.assertIn("has not served on an admissions committee", homepage)
        self.assertIn("medcompass.audit@atomicmail.io", homepage)
        self.assertIn("privacy.html", homepage)
        self.assertIn("terms.html", homepage)

    def test_site_has_no_tracking_or_form_data_sink(self):
        content = "\n".join(page.read_text(encoding="utf-8").lower() for page in HTML_FILES)

        self.assertNotIn("google-analytics", content)
        self.assertNotIn("googletagmanager", content)
        self.assertNotIn("facebook.com/tr", content)
        self.assertNotIn("<form", content)

    def test_structured_offer_and_sitemap_are_valid(self):
        homepage = (ROOT / "index.html").read_text(encoding="utf-8")
        match = re.search(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', homepage, re.S)
        self.assertIsNotNone(match)
        offer = json.loads(match.group(1))
        self.assertEqual(offer["@type"], "Service")
        self.assertEqual(offer["provider"]["name"], "MedCompass Audit")
        self.assertEqual(offer["offers"]["priceCurrency"], "CAD")
        self.assertEqual(offer["offers"]["price"], "79")

        sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        for page in ("sample.html", "privacy.html", "terms.html", "guides/gpa-formulas.html"):
            self.assertIn(page, sitemap)


if __name__ == "__main__":
    unittest.main()
