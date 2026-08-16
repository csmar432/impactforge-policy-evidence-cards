"""Dependency-free acceptance check for the ImpactForge static MVP."""

from __future__ import annotations

import argparse
import json
import re
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import urlopen


ROOT = Path(__file__).resolve().parents[1]
CARD_IDS = {"evidence-scale", "evidence-severity", "evidence-gap"}


class PageCheck(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self.in_title = False
        self.card_ids: set[str] = set()
        self.card_text: dict[str, str] = {}
        self.card_links: dict[str, set[str]] = {}
        self.card_meta: dict[str, dict[str, str]] = {}
        self.external_links: set[str] = set()
        self.required_ids: set[str] = set()
        self.button_types: list[str | None] = []
        self.empty_links: list[str] = []
        self.images_without_alt: list[str] = []
        self.current_card: str | None = None
        self.card_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if tag == "title":
            self.in_title = True
        element_id = attributes.get("id")
        if element_id:
            self.required_ids.add(element_id)
        if tag == "article" and "evidence-card" in (attributes.get("class") or "") and element_id:
            self.card_ids.add(element_id)
            self.card_text[element_id] = ""
            self.card_links[element_id] = set()
            self.card_meta[element_id] = {key: value or "" for key, value in attributes.items() if key.startswith("data-")}
            self.current_card = element_id
            self.card_depth = 1
        elif self.current_card:
            self.card_depth += 1
        if tag == "button":
            self.button_types.append(attributes.get("type"))
        if tag == "img" and not attributes.get("alt"):
            self.images_without_alt.append(element_id or "<unnamed>")
        if tag == "a":
            href = attributes.get("href") or ""
            if not href or href == "#":
                self.empty_links.append(href)
            if href.startswith("https://"):
                self.external_links.add(href)
            if self.current_card and href:
                self.card_links[self.current_card].add(href)

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False
        if self.current_card:
            self.card_depth -= 1
            if self.card_depth == 0:
                self.current_card = None

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title += data
        if self.current_card:
            self.card_text[self.current_card] += f" {data}"


def read_page(url: str | None) -> str:
    if url:
        return urlopen(url, timeout=5).read().decode("utf-8")
    return (ROOT / "src/index.html").read_text(encoding="utf-8")


def normalise(text: str) -> str:
    return re.sub(r"\s+", " ", unescape(text)).strip().lower()


def assert_card_provenance(parsed: PageCheck, data: dict) -> None:
    sources = {source["id"]: source for source in data["sources"]}
    expected_cards = {card["id"]: card for card in data["cards"]}
    assert set(expected_cards) == {"01", "02", "03"}
    source_field = {"01": "evidence-scale", "02": "evidence-severity", "03": "evidence-gap"}

    for card_id, card in expected_cards.items():
        element_id = source_field[card_id]
        text = normalise(parsed.card_text[element_id])
        meta = parsed.card_meta[element_id]
        display_metric = card.get("display_metric", card["metric"])
        assert meta["data-card-id"] == card_id, (element_id, "card id")
        assert normalise(meta["data-label"]) == normalise(card["label"]), (element_id, "label")
        assert normalise(meta["data-metric"]) == normalise(card["metric"]), (element_id, "metric")
        assert normalise(meta["data-supporting-value"]) == normalise(card["supporting_value"]), (element_id, "supporting value")
        assert meta["data-year"] == str(card["year"]), (element_id, "year metadata")
        assert normalise(meta["data-claim"]) == normalise(card["claim"]), (element_id, "claim")
        assert normalise(display_metric) in text, (element_id, display_metric)
        assert str(card["year"]) in text, (element_id, card["year"])
        assert sources[card["source_id"]]["url"] in parsed.card_links[element_id], element_id
        for optional_source_key in ("definition_source_id", "policy_source_id"):
            source_id = card.get(optional_source_key)
            if source_id:
                assert sources[source_id]["url"] in parsed.card_links[element_id], (element_id, source_id)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="also verify a running local server")
    args = parser.parse_args()

    page = read_page(args.url)
    parsed = PageCheck()
    parsed.feed(page)
    data = json.loads((ROOT / "data/evidence.json").read_text(encoding="utf-8"))

    assert parsed.title == "Policy Evidence Cards · Student food insecurity"
    assert parsed.card_ids == CARD_IDS
    assert {"next-step", "action-label", "action-copy", "action-link", "feedback-status"}.issubset(parsed.required_ids)
    visible_markup = page.split("<script>", 1)[0]
    assert all(text in visible_markup for text in ("23%", "2.2M", "59%", "The takeaway", "Source notes"))
    assert len(parsed.external_links) >= 3
    assert parsed.external_links == {source["url"] for source in data["sources"]}
    assert not parsed.empty_links
    assert not parsed.images_without_alt
    assert all(button_type == "button" for button_type in parsed.button_types)
    assert 'data-choice="context"' in page
    assert 'data-choice="definition"' in page
    assert 'data-choice="help"' in page
    assert "self-reported clarity" in page
    assert 'id="feedback-recovery"' in page
    assert "official federal SNAP student rules" in page
    assert "That is the intended outcome" in page
    assert "That is useful feedback" in page
    assert "Potential SNAP eligibility is not reported receipt." in page
    assert "support is failing to connect" not in page
    assert "support systems fail to reach people" not in page

    assert len(data["cards"]) == 3
    assert {card["source_id"] for card in data["cards"]} == {"S1"}
    assert {source["id"] for source in data["sources"]} == {"S1", "S2", "S3"}
    assert all(source["url"].startswith("https://") for source in data["sources"])
    assert all(source.get("accessed_at") for source in data["sources"])
    assert data["limitations"]
    assert all(phrase in visible_markup for phrase in (
        "Food insecurity" ,
        "not the same measure as hunger",
        "not a rate for all college students",
        "does not determine eligibility",
    ))
    assert_card_provenance(parsed, data)

    target = args.url or "local source"
    print(f"PASS: {target}; content, provenance, actions, accessibility, and claims checks")


if __name__ == "__main__":
    main()
