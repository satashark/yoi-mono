# 師匠式LP テンプレート (lp_shishou)

完全SEO装備の再利用可能ランディングページテンプレート。
sakibarai.jp の構造を参考に、汎用化したものです。

## ディレクトリ構成

```
lp_shishou/
├── README.md              # この説明書
├── base-template.html     # メインHTMLテンプレート
├── css/base.css           # スタイルシート
├── schemas/schema_generator.py  # JSON-LD自動生成
├── scripts/deploy_helper.md     # デプロイ手順
└── images/                # 差し替え用画像置き場
```

## 使い方 (3ステップ)

### Step 1. プロジェクトにコピー
```bash
cp -r ~/.openclaw/workspace/templates/lp_shishou/ ~/projects/my-new-site/
cd ~/projects/my-new-site/
```

### Step 2. プレースホルダー置換
`base-template.html` の `{{VARIABLE}}` を sed もしくはエディタで一括置換。

### Step 3. 構造化データ生成 + デプロイ
```bash
python3 schemas/schema_generator.py --site my-new-site --output schemas.json
# 生成されたJSON-LDをHTMLに埋め込み (もしくはschemas.jsonを直接読み込み)
# Cloudflare Pages にデプロイ (scripts/deploy_helper.md 参照)
```

## プレースホルダー一覧

### サイト基本情報
- `{{SITE_NAME}}` — サイト名 (例: 先払い買取比較ナビ)
- `{{SITE_URL}}` — フルURL (例: https://example.com/)
- `{{SITE_DESCRIPTION}}` — meta description (120-160文字)
- `{{SITE_KEYWORDS}}` — meta keywords (カンマ区切り)
- `{{SITE_LOGO_URL}}` — ロゴ画像URL
- `{{ORG_NAME}}` — 運営組織名
- `{{PUBLISH_DATE}}` — ISO 8601形式 (例: 2026-04-13T09:00:00+09:00)
- `{{MODIFIED_DATE}}` — 同上

### Hero
- `{{HERO_TITLE}}` — H1メインタイトル
- `{{HERO_SUB}}` — サブコピー
- `{{HERO_IMAGE}}` — ヒーロー画像パス (推奨: images/hero-main.webp)
- `{{HERO_CTA_PRIMARY}}` — 主CTAテキスト
- `{{HERO_CTA_PRIMARY_URL}}` — 主CTA遷移先
- `{{HERO_CTA_SECONDARY}}` — 副CTAテキスト
- `{{HERO_CTA_SECONDARY_URL}}` — 副CTA遷移先

### ランキング (1〜5位、各項目に番号付与)
- `{{RANK1_NAME}}` `{{RANK1_BANNER}}` `{{RANK1_RATE}}` `{{RANK1_LIMIT}}` `{{RANK1_SPEED}}` `{{RANK1_DESC}}` `{{RANK1_URL}}`
- ...同様に RANK2〜RANK5

### 比較表
- `{{COMPARISON_ROWS}}` — テーブル行HTML (もしくは個別 ROW1_X 〜 ROW5_X)

### FAQ
- `{{FAQ1_Q}}` `{{FAQ1_A}}` 〜 `{{FAQ5_Q}}` `{{FAQ5_A}}`

### Footer
- `{{FOOTER_LINKS}}` `{{COPYRIGHT}}`

### 解析タグ
- `{{GTM_ID}}` — Google Tag Manager ID (例: GTM-XXXXXXX)
- `{{GA_ID}}` — GA4測定ID (任意)

## JSON-LD生成方法

`schemas/schema_generator.py` を実行すると以下7種を生成:
1. WebSite + SearchAction
2. Organization
3. ItemList (ランキング)
4. Product + AggregateRating (各案件)
5. BreadcrumbList
6. Article + SpeakableSpecification
7. WebPage + FAQPage

```bash
python3 schemas/schema_generator.py \
  --site-name "先払い買取比較ナビ" \
  --site-url "https://example.com/" \
  --output schemas.json
```

## 画像差し替え手順

| ファイル名 | 用途 | 推奨サイズ |
|---|---|---|
| images/hero-main.webp | ヒーロー画像 | 1200×800 |
| images/rank-1.webp 〜 rank-5.webp | 順位アイコン | 200×200 |
| images/banner-{slug}.webp | 案件バナー | 600×300 |
| images/logo.webp | ロゴ | 300×80 |
| images/og-image.webp | OGP用 | 1200×630 |

WebP変換例:
```bash
cwebp -q 85 input.png -o images/hero-main.webp
```

## 注意事項

- ❌ sakibarai.jp の文言そのままコピーは禁止 (著作権侵害)
- ✅ 構造・配色・組み立てのみ参考にし、文言は独自に
- ✅ 【広告・PR】開示は必須 (景表法・ステマ規制)
- ✅ デプロイ前に Lighthouse で90点以上を目標に
