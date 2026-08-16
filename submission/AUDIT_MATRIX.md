# Official requirements matrix

| Requirement | Evidence in this workspace | Status |
|---|---|---|
| Project name | `DEVPOST.md` → Policy Evidence Cards | Ready |
| Story / problem | `DEVPOST.md` → The story behind it / The problem | Ready |
| Solution | `DEVPOST.md` → The solution; `src/index.html` | Ready |
| Key features | `DEVPOST.md` → Key features | Ready |
| Tools / languages / APIs | `DEVPOST.md` → Tools and technology | Ready |
| Intended users | `DEVPOST.md` → Who it helps | Ready |
| Impact statement | `IMPACT_STATEMENT.md` | Ready |
| Proof of work | At least one current Chromium screenshot; seven-image handoff bundle available locally | Official minimum ready; remaining images are internal options |
| Project link | `DELIVERY.md` | Officially optional but encouraged; requires public deployment or repository URL |
| Team | `DEVPOST.md` | Official size is 1–5; requires every builder's public name and contribution, while solo entries still name the entrant and work |
| Eligibility / deadline | `README.md`; `DELIVERY.md` | Human confirmation required; official Overview and Rules pages currently disagree on deadline |
| Evidence provenance | `data/evidence.json`; S1–S3 links on cards | Ready |
| Reader action | `src/index.html` source-to-action panel | Ready |
| Automated acceptance | `check_mvp.py`, `check_browser.py`, plus inline JavaScript syntax check | Internal validation ready; not an extra Devpost field |
| Responsive proof | Chromium-generated `impactforge-mvp-mobile.png` and `impactforge-mvp-runtime-mobile.png` | 320px browser proof ready; real phone test still required |
| Real-user validation | `USER_TEST_PROTOCOL.md` | Not an official requirement; requires real student testers and may strengthen impact and UX evidence |
| Demo video | `DEMO_SCRIPT.md` | Optional proof format; requires human recording, while a current screenshot already meets the proof minimum |

## Official judging criteria

| Criterion | Evidence in this workspace | Remaining limit |
|---|---|---|
| Build Quality (30%) | Working dependency-free MVP; provenance check; Chromium interaction and responsive checks | Public hosting is still encouraged for judge access |
| Real-World Impact (25%) | Documented student problem; source-linked evidence; direct path to current USDA rules | Real student testing has not been run and no results are claimed |
| Creativity & Approach (20%) | Reusable evidence-card sequence connects scale, severity, policy gap, caveats, and action | Judges determine originality; no comparative claim is made |
| User Experience (15%) | Responsive desktop/mobile layouts; keyboard focus; clear next-step choices; private reader check | Real phone and real-user validation remain external |
| Clarity of Submission (10%) | Devpost story, impact statement, demo script, proof images, delivery checklist, and this matrix | Builder identity and final public link must be supplied by the entrant |

## Acceptance commands

```bash
python3 submission/check_mvp.py
python3 submission/check_mvp.py --url http://127.0.0.1:4173/
python3 submission/check_browser.py
```

The matrix intentionally does not mark external identity, publication, or human research as complete without the required person or authorization.
