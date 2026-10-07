# F&A Hospitality Calculators

Free UK calculators for hospitality businesses, built for the F&A Accountants website.

- **VAT calculator**: add or remove VAT at 20%, 5% or 0%
- **GP% and prime cost**: food GP, drink GP and prime cost, with benchmark checks
- **Payroll cost**: take-home pay and total employer cost (tax, NI, pension, Employment Allowance)

Rates are for the **2026/27 UK tax year** (England, Wales and NI), from HMRC's
[rates and thresholds for employers 2026 to 2027](https://www.gov.uk/guidance/rates-and-thresholds-for-employers-2026-to-2027).

## Files

| File | What it is |
|---|---|
| `index.html` | Stand-alone page. Open it in a browser or publish with GitHub Pages. |
| `elementor-embed.html` | The calculators only, for one Elementor **HTML** widget. Styles are scoped to `.fac`. |
| `elementor-template/fa-hospitality-calculators.json` | Full Elementor page template: hero, calculators, FAQ (with FAQ schema for Google) and CTA. |
| `tools/build_template.py` | Rebuilds the template JSON from `elementor-embed.html`. |

## Import the Elementor template

1. WordPress → **Templates → Saved Templates → Import Templates**
2. Choose `elementor-template/fa-hospitality-calculators.json` and import
3. Create a new page → **Edit with Elementor** → folder icon → **My Templates** → insert
   "F&A – Hospitality Calculators (Native Elementor)"
4. Preview, then publish

Link to one calculator with `#vat`, `#gp` or `#payroll` at the end of the page URL.

## Updating rates every April

1. Change the `R = { ... }` line in **both** `index.html` and `elementor-embed.html`
2. Run `python3 tools/build_template.py` to refresh the template
3. Re-import the template, or paste the new embed into the HTML widget

Estimates for guidance only, not tax advice.
