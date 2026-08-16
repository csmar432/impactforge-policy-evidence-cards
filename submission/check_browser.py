"""Run a real Chromium smoke test and refresh all proof screenshots."""

from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
SUBMISSION = ROOT / "submission"
URL = "http://127.0.0.1:4173/"
SYSTEM_CHROME = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")


def assert_text(page, selector: str, expected: str) -> None:
    actual = page.locator(selector).text_content().strip()
    assert actual == expected, (selector, actual, expected)


def assert_no_horizontal_overflow(page) -> None:
    layout = page.evaluate(
        "({viewport: window.innerWidth, content: document.documentElement.scrollWidth})"
    )
    assert layout["content"] <= layout["viewport"], layout


def exercise_page(page) -> None:
    assert page.title() == "Policy Evidence Cards · Student food insecurity"
    assert page.locator("[data-card-id]").count() == 3

    definition = page.locator('[data-choice="definition"]')
    definition.click()
    assert definition.get_attribute("aria-pressed") == "true"
    assert_text(page, "#action-label", "Start with the definition")
    assert page.locator("#action-link").get_attribute("href") == "#evidence-severity"

    help_choice = page.locator('[data-choice="help"]')
    help_choice.click()
    assert help_choice.get_attribute("aria-pressed") == "true"
    assert_text(page, "#action-label", "Start with the official rules")
    help_link = page.locator("#action-link")
    assert help_link.get_attribute("href") == "https://www.fna.usda.gov/snap/students"
    assert help_link.get_attribute("target") == "_blank"

    clear = page.locator('[data-feedback="clear"]')
    clear.click()
    assert clear.get_attribute("aria-pressed") == "true"
    assert_text(page, "#feedback-status", "That is the intended outcome: a clear takeaway with an honest caveat.")

    not_yet = page.locator('[data-feedback="unclear"]')
    not_yet.click()
    assert not_yet.get_attribute("aria-pressed") == "true"
    assert_text(page, "#feedback-status", "That is useful feedback: revisit the cards or open the original sources.")


def main() -> None:
    with sync_playwright() as playwright:
        launch_options = {"headless": True}
        if SYSTEM_CHROME.exists():
            launch_options["executable_path"] = str(SYSTEM_CHROME)
        browser = playwright.chromium.launch(**launch_options)
        desktop = browser.new_page(viewport={"width": 1120, "height": 900}, device_scale_factor=1)
        desktop.goto(URL, wait_until="networkidle")
        assert_no_horizontal_overflow(desktop)
        desktop_capture = desktop.screenshot(full_page=True)
        for name in ("impactforge-mvp-runtime-desktop.png", "impactforge-mvp-full.png"):
            (SUBMISSION / name).write_bytes(desktop_capture)

        page_height = desktop.evaluate("document.documentElement.scrollHeight")
        desktop.set_viewport_size({"width": 1120, "height": page_height})
        crop_names = (
            "impactforge-mvp-desktop.png",
            "impactforge-mvp-desktop-page2.png",
            "impactforge-mvp-desktop-page3.png",
        )
        for index, name in enumerate(crop_names):
            top = page_height * index // len(crop_names)
            bottom = page_height * (index + 1) // len(crop_names)
            desktop.screenshot(
                path=str(SUBMISSION / name),
                clip={"x": 0, "y": top, "width": 1120, "height": bottom - top},
            )
        desktop.set_viewport_size({"width": 1120, "height": 900})
        exercise_page(desktop)

        mobile = browser.new_page(viewport={"width": 320, "height": 900}, device_scale_factor=1)
        mobile.goto(URL, wait_until="networkidle")
        assert_no_horizontal_overflow(mobile)
        mobile_capture = mobile.screenshot(full_page=True)
        for name in ("impactforge-mvp-runtime-mobile.png", "impactforge-mvp-mobile.png"):
            (SUBMISSION / name).write_bytes(mobile_capture)
        exercise_page(mobile)

        for width in (820, 560):
            responsive = browser.new_page(viewport={"width": width, "height": 900})
            responsive.goto(URL, wait_until="networkidle")
            assert_no_horizontal_overflow(responsive)
            assert responsive.locator("[data-card-id]").count() == 3
            responsive.close()

        browser.close()

    print("PASS: Chromium interactions, 4 responsive widths, and 7 current proof screenshots")


if __name__ == "__main__":
    main()
