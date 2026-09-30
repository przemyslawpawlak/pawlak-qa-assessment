# GenericCRM — QA Automation Assessment

Automated UI tests for the GenericCRM **Data Issues** page, written with
Playwright (Python sync API) and pytest.

## Prerequisites

- Python 3.10+
- The provided assessment app files (`index.html`, `vf-container.html`, `app.html`)

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS / Linux

pip install -r requirements.txt
playwright install chromium
```

## Running the tests

The tests drive the app over HTTP, so it must be served locally first.

1. In a separate terminal, from the folder containing the app files:

   ```bash
   python -m http.server 9000
   ```

   The app must be reachable at http://localhost:9000/index.html

2. In the project folder, with the venv active:

   ```bash
   pytest -v
   ```

All five tests should pass.

> The target URL is defined once in `conftest.py` (`APP_URL`). If you serve the
> app on a different port, change that single line.

## The tests (`test_data_issues.py`)

1. **test_data_issues_shows_ten_cards** — the page displays exactly 10 issue cards.
2. **test_original_rows_have_sfid** — every card's Original row carries a non-empty
   sfid, with a count guard so the test can't pass on a truncated grid.
3. **test_selecting_original_updates_final_row** — choosing the "Original" radio on a
   card updates its Final row to match.
4. **test_editing_final_value_persists** — editing a card's Final value (located by
   sfid) saves and displays the new value.
5. **test_selection_counter_and_select_all** — individual selection, select-all, and
   deselect-all correctly drive the selection counter and confirm bar.

## Approach & notes

- **Nested iframes.** The app mirrors a Salesforce Visualforce layout — the UI lives
  two iframes deep (`#outerFrame` -> `#appFrame`), while the welcome modal sits on the
  top page. App locators traverse the frame chain with `frame_locator`; a shared
  `conftest.py` fixture performs this navigation once per test.
- **No fixed sleeps.** Every assertion uses Playwright's auto-waiting `expect`. The one
  explicit timeout (waiting for the grid to render) is sized to the app's own behavior —
  cards render after a randomized 0.5–5s delay — rather than a guessed number.
- **Assertions with teeth.** Tests verify real state changes and include guards (such as
  the exact card count) so they fail loudly on a regression instead of passing vacuously.
- **Stable locators.** Roles, labels, and data attributes (`data-record-id`,
  `data-row-type`) are preferred over brittle positional selectors.

## Project structure

```
.
├── conftest.py            # APP_URL, the iframe helper, and the data_issues fixture
├── test_data_issues.py    # the five tests
├── requirements.txt
└── README.md
```
