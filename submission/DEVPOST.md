# Policy Evidence Cards

## The story behind it

Public policy data is often technically available but practically unreadable. A student can encounter a statistic about food insecurity, search for the source, and still not know what the number measures, how severe the situation is, or whether a policy program can help.

I built Policy Evidence Cards as a small, source-linked reading layer for that moment. The first brief focuses on food insecurity among U.S. college students and puts the measure, severity, and policy context in one readable sequence.

## The problem

Students need to make sense of public data quickly. A single statistic can leave out what it measures, how severe the reported experience is, and how a policy program relates to it. Without those pieces, readers have less context for a useful next question—and potential eligibility can be mistaken for reported receipt.

## The solution

Policy Evidence Cards reduces one policy topic to three linked cards:

1. **Scale** — 23% of college students in the cited study experienced food insecurity in 2020.
2. **Severity** — 2.2 million food-insecure students reported very low food security, including repeated reductions in food intake or skipped meals.
3. **Policy gap** — 59% of food-insecure students who were potentially eligible for SNAP did not report receiving benefits.

The page ends with one evidence-based takeaway and a next-step link to the USDA student SNAP rules. Every card shows its year and links directly to the original public source. The source notes distinguish food insecurity from hunger and explain what the 2020 estimates cannot prove.

## Key features

- Three-card progression: scale → severity → policy gap
- Plain-language explanations beside the headline number
- Direct links to GAO, USDA ERS, and USDA Food and Nutrition Administration source pages
- A source-to-action path that lets a reader choose context, definition, or help
- A private, in-browser self-reported clarity check without collecting personal data
- Explicit data year and limitation notes
- Responsive layout for phone and desktop reading
- No account, backend, or build step required
- Keyboard-visible focus states and semantic section landmarks

## Tools and technology

- HTML5 and CSS3
- Vanilla JavaScript for the source-to-action path and private reader check
- Python standard library acceptance checks
- Playwright and headless Chromium for interaction, responsive, and screenshot validation
- Small, dependency-free runtime with no account, backend, build step, or live API
- Public U.S. Government Accountability Office and U.S. Department of Agriculture sources
- JSON evidence manifest in `data/evidence.json`

## Who it helps

- Students who want to understand a public issue before reposting or citing a statistic
- Campus educators, advisers, and student journalists who need a compact briefing format
- Community organizations that want to explain a policy pathway without hiding the caveats

## Impact statement

Policy Evidence Cards gives students a reusable way to move from a public statistic to a better question: What exactly is being measured, who is affected, what can a policy do, and where are the gaps? The prototype starts with student food insecurity and can be reused for housing, mental health, financial aid, or other issues where a source-linked explanation is more useful than another data dump.

## Proof of work

ImpactForge requires at least one screenshot, demo video, or file showing the project in action. Upload at least one of the two current Chromium runtime screenshots below; the remaining files are optional internal handoff assets.

- `src/index.html` — working responsive MVP
- `data/evidence.json` — evidence and provenance manifest
- `submission/check_mvp.py` — dependency-free acceptance check
- `submission/USER_TEST_PROTOCOL.md` — five-minute student comprehension test
- `submission/impactforge-mvp-runtime-desktop.png` — current Chromium runtime proof at desktop width
- `submission/impactforge-mvp-runtime-mobile.png` — current Chromium runtime proof at 320px width
- `submission/impactforge-mvp-interaction-desktop.png` — current Chromium proof of the selected help path
- `submission/impactforge-mvp-desktop.png`, `impactforge-mvp-desktop-page2.png`, `impactforge-mvp-desktop-page3.png` — optional cropped desktop handoff views
- `submission/impactforge-mvp-full.png`, `impactforge-mvp-mobile.png` — optional full-page handoff views
- `submission/DEMO_SCRIPT.md` — 60-second walkthrough
- `submission/impactforge-demo.webm` — silent 60-second interaction walkthrough

## Project link

Public repository: https://github.com/csmar432/impactforge-policy-evidence-cards

Live demo: https://csmar432.github.io/impactforge-policy-evidence-cards/

The local demo runs with:

```bash
python3 -m http.server 4173 --directory src
```

## Team

yi (public GitHub handle: csmar432) — product concept, evidence framing, UX, implementation, validation, and submission materials.

Confirm that the Devpost profile uses the intended public display name before submitting.
