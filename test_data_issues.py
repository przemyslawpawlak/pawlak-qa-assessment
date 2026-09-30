from playwright.sync_api import expect

def test_data_issues_shows_ten_cards(data_issues):
    expect(data_issues.locator(".issue-card")).to_have_count(10)

def test_original_rows_have_sfid(data_issues):
    original_rows = data_issues.locator('tr[data-row-type="original"]')
    expect(original_rows).to_have_count(10)
    for i in range(original_rows.count()):
        sfid = original_rows.nth(i).locator("td").last.inner_text().strip()
        assert sfid, f"Original row {i + 1} has an empty sfid"

def test_selecting_original_updates_final_row(data_issues):
    card = data_issues.locator(".issue-card").nth(6)
    original_value = card.locator(
        'tr[data-row-type="original"] .cell-issue span'
    ).inner_text().strip()
    card.locator('input[type="radio"][value="original"]').check()
    expect(
        card.locator('tr[data-row-type="final"] .cell-editable span')
    ).to_have_text(original_value)

def test_editing_final_value_persists(data_issues):
    card = data_issues.locator('[data-record-id="00Qak00000RHtuzEAD"]')
    editable = card.locator('tr[data-row-type="final"] .cell-editable')
    editable.click()
    edit_input = card.locator('.inline-edit-input')
    edit_input.fill("123 Test Street")
    edit_input.press("Enter")
    expect(editable.locator("span")).to_have_text("123 Test Street")

def test_selection_counter_and_select_all(data_issues):
    cards       = data_issues.locator(".issue-card")
    counter     = data_issues.locator("#selectedCount")
    confirm_bar = data_issues.locator("#confirmBar")
    select_all  = data_issues.locator("#selectAll")

    for i in (0, 2, 4):
        cards.nth(i).locator(".issue-checkbox").check()
    expect(counter).to_have_text("3")
    expect(confirm_bar).to_be_visible()

    select_all.check()
    expect(select_all).to_be_checked()
    expect(counter).to_have_text("10")

    select_all.uncheck()
    expect(confirm_bar).to_be_hidden()