"""Record a silent 60-second walkthrough of the working MVP."""

import os
import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "submission" / "impactforge-demo.webm"
URL = os.environ.get("IMPACTFORGE_URL", "http://127.0.0.1:4173/")
SYSTEM_CHROME = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")


def pause(page, milliseconds: int = 6500) -> None:
    page.wait_for_timeout(milliseconds)


def main() -> None:
    with sync_playwright() as playwright:
        launch_options = {"headless": True}
        if SYSTEM_CHROME.exists():
            launch_options["executable_path"] = str(SYSTEM_CHROME)
        browser = playwright.chromium.launch(**launch_options)
        with tempfile.TemporaryDirectory(prefix="impactforge-demo-") as video_dir:
            context = browser.new_context(
                viewport={"width": 1120, "height": 900},
                record_video_dir=video_dir,
                record_video_size={"width": 1120, "height": 900},
            )
            page = context.new_page()
            video = page.video
            page.goto(URL, wait_until="networkidle")
            pause(page, 9000)

            page.locator("#cards").scroll_into_view_if_needed()
            pause(page, 9000)

            page.locator('[data-choice="definition"]').click()
            pause(page, 8000)

            page.locator('[data-choice="help"]').click()
            pause(page, 9000)

            page.locator("#takeaway").scroll_into_view_if_needed()
            pause(page, 9000)

            page.locator('[data-feedback="unclear"]').click()
            pause(page, 8000)

            page.locator("#sources").scroll_into_view_if_needed()
            pause(page, 9000)

            context.close()
            video.save_as(OUTPUT)
        browser.close()

    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
