#!/usr/bin/env python3
"""
schema_generator.py — 師匠式LP用 JSON-LD 7種一括生成スクリプト

使い方:
  python3 schema_generator.py \
    --site-name "先払い買取比較ナビ" \
    --site-url "https://example.com/" \
    --org-name "運営事務局" \
    --output schemas.json

オプション --config <yaml> でランキング/FAQも一括投入可能。
"""

import argparse
import json
import sys
from datetime import datetime, timezone, timedelta


JST = timezone(timedelta(hours=9))


def now_iso():
    return datetime.now(JST).strftime("%Y-%m-%dT%H:%M:%S+09:00")


def build_schemas(cfg: dict) -> list:
    site_name = cfg["site_name"]
    site_url = cfg["site_url"].rstrip("/") + "/"
    org_name = cfg.get("org_name", site_name)
    logo_url = cfg.get("logo_url", site_url + "images/logo.webp")
    hero_title = cfg.get("hero_title", site_name)
    publish_date = cfg.get("publish_date", now_iso())
    modified_date = cfg.get("modified_date", now_iso())
    rankings = cfg.get("rankings", [])
    faqs = cfg.get("faqs", [])

    schemas = []

    # 1. WebSite + SearchAction
    schemas.append({
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": site_name,
        "url": site_url,
        "potentialAction": {
            "@type": "SearchAction",
            "target": f"{site_url}?s={{search_term_string}}",
            "query-input": "required name=search_term_string",
        },
    })

    # 2. Organization
    schemas.append({
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": org_name,
        "url": site_url,
        "logo": logo_url,
    })

    # 3. ItemList
    schemas.append({
        "@context": "https://schema.org",
        "@type": "ItemList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": r["name"], "url": r["url"]}
            for i, r in enumerate(rankings)
        ],
    })

    # 4. Product + AggregateRating (各案件)
    for r in rankings:
        schemas.append({
            "@context": "https://schema.org",
            "@type": "Product",
            "name": r["name"],
            "image": r.get("banner", ""),
            "description": r.get("desc", ""),
            "aggregateRating": {
                "@type": "AggregateRating",
                "ratingValue": str(r.get("rating", "4.5")),
                "reviewCount": str(r.get("reviews", "100")),
            },
        })

    # 5. BreadcrumbList
    schemas.append({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "ホーム", "item": site_url},
            {"@type": "ListItem", "position": 2, "name": hero_title, "item": site_url},
        ],
    })

    # 6. Article + Speakable
    schemas.append({
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": hero_title,
        "image": site_url + "images/hero-main.webp",
        "datePublished": publish_date,
        "dateModified": modified_date,
        "author": {"@type": "Organization", "name": org_name},
        "publisher": {
            "@type": "Organization",
            "name": org_name,
            "logo": {"@type": "ImageObject", "url": logo_url},
        },
        "speakable": {
            "@type": "SpeakableSpecification",
            "cssSelector": [".hero-title", ".hero-sub"],
        },
    })

    # 7. WebPage + FAQPage
    schemas.append({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q["q"],
                "acceptedAnswer": {"@type": "Answer", "text": q["a"]},
            }
            for q in faqs
        ],
    })

    return schemas


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--site-name", required=True)
    p.add_argument("--site-url", required=True)
    p.add_argument("--org-name", default=None)
    p.add_argument("--logo-url", default=None)
    p.add_argument("--hero-title", default=None)
    p.add_argument("--config", default=None, help="JSON config (rankings/faqs等)")
    p.add_argument("--output", default="schemas.json")
    args = p.parse_args()

    cfg = {
        "site_name": args.site_name,
        "site_url": args.site_url,
        "org_name": args.org_name or args.site_name,
        "logo_url": args.logo_url,
        "hero_title": args.hero_title or args.site_name,
        "rankings": [],
        "faqs": [],
    }

    if args.config:
        with open(args.config, "r", encoding="utf-8") as f:
            cfg.update(json.load(f))

    schemas = build_schemas(cfg)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(schemas, f, ensure_ascii=False, indent=2)

    print(f"[OK] {len(schemas)}個のスキーマを {args.output} に出力しました", file=sys.stderr)


if __name__ == "__main__":
    main()
