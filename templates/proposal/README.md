# MDS Diversified — Proposal Template

Master proposal template used for all new client engagements. Based on the TrackNow proposal layout: dark theme, orange accents, 4-page structure (Cover / Overview / Tech Stack / Investment).

**Location:** `mds-diversified/templates/proposal/proposal-template.html`
This is the single source of truth. Any project can pull from here.

## How to use (for future Claude sessions)

When James asks for "a proposal for [client]" or "new client proposal":

1. Copy `proposal-template.html` into the client's project folder
2. Replace these placeholders:

| Placeholder | Example |
|---|---|
| `{{CLIENT_NAME}}` | Mark Speelmeyer |
| `{{CLIENT_COMPANY}}` | TrackNow Pty Ltd |
| `{{PROJECT_TITLE}}` | Sales & Marketing Portal Build Proposal |
| `{{PROJECT_TAGLINE}}` | Custom-built digital sales platform for... |
| `{{PROJECT_OVERVIEW}}` | 1-paragraph intro of what the portal does |
| `{{PROPOSAL_DATE}}` | April 2026 |
| `{{STATUS_BANNER}}` | e.g. "PHASE 1 BUILD COMPLETE | $7,500 + GST Due & Payable" — or remove the banner div entirely for fresh proposals |
| `{{FEATURE_1..4_TITLE}}` | e.g. "Core Platform", "Sales Tools & Calculators" |
| `{{FEATURE_1..4_ITEMS}}` | `<li>Item one</li><li>Item two</li>...` |
| `{{LINE_ITEMS}}` | `<tr><td>Portal Design & Development</td><td>Included</td></tr>...` |
| `{{PRICE_EX_GST}}` | 7,500.00 |
| `{{PRICE_GST}}` | 750.00 |
| `{{PRICE_TOTAL}}` | 8,250.00 |

3. Save to the client's project folder as `<client>-proposal.html`
4. Convert to PDF if requested (use the `pdf` skill or Chrome print-to-PDF)

## Fixed elements (do NOT change per-client)

- MDS Diversified brand name, orange accent `#f97316`, dark navy background `#0f1419`
- Footer contact block: www.mdsdiversified.ai, james@mdsdiversified.ai, 0406 718 007
- Gold Coast: Level 13, 50 Cavill Avenue, Surfers Paradise QLD 4217
- Sydney: Level 33, Australia Square, 264 George Street, Sydney NSW 2000
- Prepared By block: James Okkerse / MDS Diversified Pty Ltd / ABN Pending
- Data Ownership & Code Licensing red callout on page 2
- Technology Stack page 3 (GitHub + Render + MDS Shield) — consistent across all proposals
- Payment Terms (50/50, Net 7) and Exclusions — consistent

## Rendering to PDF

```bash
# via Chrome headless
google-chrome --headless --print-to-pdf="proposal.pdf" \
  --no-pdf-header-footer --print-to-pdf-no-header \
  proposal-template.html
```

Or open in Chrome → Print → Save as PDF → Background graphics ON → Margins: None.
