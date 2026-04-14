# デプロイ手順 (Cloudflare Pages + GitHub)

## 1. GitHubリポジトリ作成

```bash
cd ~/projects/my-new-site/
git init
git add .
git commit -m "Initial commit (lp_shishou template)"
gh repo create my-new-site --public --source=. --push
```

## 2. Cloudflare Pages 連携

1. https://dash.cloudflare.com/ にログイン
2. **Workers & Pages** → **Create application** → **Pages** → **Connect to Git**
3. リポジトリ `my-new-site` を選択
4. ビルド設定:
   - Framework preset: `None`
   - Build command: (空欄でOK / 静的HTML)
   - Build output directory: `/`
5. **Save and Deploy**

数十秒で `https://my-new-site.pages.dev` が公開される。

## 3. カスタムドメイン設定

1. Cloudflare Pages プロジェクト → **Custom domains** → **Set up a custom domain**
2. 独自ドメイン (例: `example.com`) を入力
3. CloudflareでDNS管理している場合は自動でCNAME設定
4. 外部DNSの場合: `CNAME my-new-site.pages.dev` を追加

SSL証明書は自動で発行 (Let's Encrypt)。

## 4. Google Search Console 登録

1. https://search.google.com/search-console/ にアクセス
2. **プロパティを追加** → **URLプレフィックス** → `https://example.com/`
3. 所有権確認: HTMLタグ方式が簡単
   - `<meta name="google-site-verification" content="xxx">` を `<head>` に追加
   - 再デプロイ後、SCで「確認」クリック
4. **サイトマップ** → `sitemap.xml` を送信
5. **URL検査** → トップURLを入力 → **インデックス登録をリクエスト**

## 5. Google Tag Manager / GA4

1. https://tagmanager.google.com/ で新規コンテナ作成
2. 取得した `GTM-XXXXXXX` を `base-template.html` の `{{GTM_ID}}` に置換
3. GTM管理画面でGA4タグを追加 (測定ID `G-XXXXXXX`)
4. **公開** ボタンでタグを反映

## 6. Lighthouse スコア確認

```bash
npx lighthouse https://example.com/ --view
```

目標: Performance 90+ / SEO 100 / Best Practices 95+ / Accessibility 90+

## 7. 公開後チェックリスト

- [ ] canonical URL が正しい
- [ ] OGP画像が表示される (https://www.opengraph.xyz/ で確認)
- [ ] JSON-LDが正しい (https://search.google.com/test/rich-results)
- [ ] モバイル表示崩れなし
- [ ] CTAリンクが全て生きている
- [ ] 【広告・PR】開示が表示されている
- [ ] Google Search Console にインデックス登録リクエスト済み
