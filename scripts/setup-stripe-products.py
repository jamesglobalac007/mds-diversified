"""
One-time setup: create all 6 MDS Diversified tier products in Stripe,
attach prices (one-off or recurring), and generate Payment Links.

Run with the saved Stripe secret key from ~/.mds/credentials.json.
Idempotent — looks up existing products by name and reuses, won't
create duplicates if re-run.

Output: prints a table mapping each tier to its Payment Link URL,
ready to paste into the package card CTAs.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import stripe

CREDS = Path.home() / ".mds" / "credentials.json"
stripe.api_key = json.load(open(CREDS))["stripe_secret_key"]

# (name, blurb, amount in dollars, recurring? AUD)
TIERS = [
    ("MDS — Launch",     "Custom marketing website setup",                    5000,  None),
    ("MDS — Lift",       "Website + branded social channel setup",            7500,  None),
    ("MDS — Scale",      "Complete marketing and sales setup",                9500,  None),
    ("MDS — Steady",     "1 post per week across LinkedIn / Facebook / IG",   350,   "month"),
    ("MDS — Active",     "2 posts per week + monthly content review call",    500,   "month"),
    ("MDS — Always-on",  "5+ posts per week across 4 channels, 7 days a week", 1000, "month"),
]

CURRENCY = "aud"


def find_product_by_name(name: str):
    """Search active products for an exact name match."""
    for prod in stripe.Product.list(active=True, limit=100).auto_paging_iter():
        if prod.name == name:
            return prod
    return None


def find_price(product_id: str, amount_cents: int, recurring: str | None):
    """Find an existing matching price on the product, or None."""
    for price in stripe.Price.list(product=product_id, active=True, limit=100).auto_paging_iter():
        if price.unit_amount != amount_cents:
            continue
        if recurring and (not price.recurring or price.recurring.interval != recurring):
            continue
        if not recurring and price.recurring:
            continue
        return price
    return None


def find_payment_link(price_id: str):
    """Find an existing payment link for a given price, or None."""
    for link in stripe.PaymentLink.list(active=True, limit=100).auto_paging_iter():
        for li in link.line_items.list(limit=10).data if hasattr(link, "line_items") else []:
            if li.price.id == price_id:
                return link
        # Fallback: list line items separately (PaymentLink list doesn't expand line_items by default)
        items = stripe.PaymentLink.list_line_items(link.id, limit=10)
        if any(li.price.id == price_id for li in items.data):
            return link
    return None


def main() -> None:
    results = []
    for name, blurb, dollars, recurring in TIERS:
        amount_cents = dollars * 100

        # Product
        prod = find_product_by_name(name) or stripe.Product.create(
            name=name,
            description=blurb,
        )

        # Price
        price_kwargs = {
            "product": prod.id,
            "unit_amount": amount_cents,
            "currency": CURRENCY,
        }
        if recurring:
            price_kwargs["recurring"] = {"interval": recurring}

        price = find_price(prod.id, amount_cents, recurring) or stripe.Price.create(**price_kwargs)

        # Payment Link
        link = find_payment_link(price.id) or stripe.PaymentLink.create(
            line_items=[{"price": price.id, "quantity": 1}],
            after_completion={"type": "hosted_confirmation"},
        )

        results.append((name, dollars, recurring or "one-off", link.url))

    # Summary
    print("\n" + "=" * 80)
    print(f"{'Tier':<22} {'Price':<10} {'Type':<10} {'Payment Link'}")
    print("=" * 80)
    for name, dollars, kind, url in results:
        suffix = "/mo" if kind == "month" else ""
        price_str = f"${dollars:,}{suffix}"
        print(f"{name:<22} {price_str:<10} {kind:<10} {url}")
    print("=" * 80)


if __name__ == "__main__":
    try:
        main()
    except stripe.error.StripeError as e:
        print(f"Stripe error: {e}", file=sys.stderr)
        sys.exit(1)
