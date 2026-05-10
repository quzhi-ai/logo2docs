<p align="center">
  <a href="README.md">English</a> · <a href="README.zh.md">中文</a> · <a href="README.ja.md">日本語</a> · <a href="README.ko.md">한국어</a>
</p>

# logo2docs

**ロゴ1つで、ブランド統一の文書スイートを自動生成。**

会社のロゴをアップロードするだけで、ブランドカラーを自動抽出し、統一デザインの Excel / Word / PowerPoint / HTMLスライド / PDF / フローチャート / マニュアルを一括生成。

> Claude Code スキル — 作者 [曲直](https://github.com/quzhi-ai)

<p align="center">
  <img src="demos/showcase.gif" alt="logo2docs デモ — 3ブランド、7フォーマット" width="800">
</p>

---

## 仕組み

logo2docs は2層構造で動作します：

1. **ブランド構築**（初回のみ）— ロゴからカラー抽出 → 3つの質問 → 完全なデザインシステム `brand-config.json`（40以上のデザイントークン）
2. **文書生成**（オンデマンド）— brand-config.json に基づいて任意の文書タイプを生成、ブランドスタイル自動統一

```
ロゴアップロード → カラー抽出 → 3つの質問 → brand-config.json → 任意の文書タイプ
```

### サポートする文書タイプ

| フォーマット | 技術 | 出力 |
|------------|------|------|
| Excel スプレッドシート | openpyxl | `.xlsx` |
| Word 文書 | python-docx | `.docx` |
| PowerPoint プレゼン | python-pptx | `.pptx` |
| HTML プレゼンテーション | インラインHTML/CSS/JS | `.html` |
| PDF | HTML → ブラウザ印刷 | `.html` / `.pdf` |
| フローチャート / 図表 | インラインSVG | `.html` |
| マニュアル / ガイド | A4ページ分割HTML | `.html` / `.pdf` |

> **💡 PowerPointファイルは完全に編集可能** — PowerPoint / Google Slides / Keynoteで開いて、テキスト変更、要素移動、スライド追加が自由自在。画像ではなく本物の `.pptx` ファイルです。もっとリッチなアニメーションが欲しい場合は、HTMLプレゼンテーションモードを選択してください。

## クイックスタート

### スキルのインストール

```bash
npx skills add https://github.com/quzhi-ai/logo2docs
```

または手動：このリポジトリをクローンし、Claude Code スキルディレクトリにコピーしてください。

### 使い方

Claudeに話しかけるだけ：

> 「これが弊社のロゴです。ブランドシステムを構築して、四半期レポートをExcelで作成してください。」

Claudeが自動的に：
1. ロゴのカラーを分析
2. 3つの質問（業界、スタイル、既存のガイドライン）
3. `brand-config.json` — 完全なデザインシステムを生成
4. ブランド統一の文書を出力

## デザイン原則

### アンチAI美学

生成される文書はプロのデザイナーが作ったように見え、AIが作ったようには見えません：

- グラデーション背景なし（特にブルーパープル系）
- 絵文字を装飾として使わない
- 角丸カード＋左側カラーバー禁止
- 3D円グラフや偽3D効果なし
- 大胆な余白（40%の空白は良いデザイン）
- 高コントラスト、精密なグリッド配置
- ソリッドカラーのみ、細い線の区切り

### 60-30-10 配色ルール

- **60%** — ニュートラル（白/薄い背景、本文）
- **30%** — ブランド主色（見出し、重要セクション）
- **10%** — アクセントカラー（ハイライト、データ強調）

## デモ

`demos/` ディレクトリに3つの完全なブランドデモが含まれています：

### ABC Education（ボールドスタイル）
子ども教育企業 — コーラルレッド + ティール。Excel、Word、PowerPoint、HTMLスライド、フローチャート。

<p align="center">
<img src="demos/screenshots/abc-01-cover.png" width="400"> <img src="demos/screenshots/abc-02-content.png" width="400"><br>
<img src="demos/screenshots/abc-05-excel.png" width="400"> <img src="demos/screenshots/abc-06-word.png" width="400"><br>
<img src="demos/screenshots/abc-03-data.png" width="400"> <img src="demos/screenshots/abc-04-preview.png" width="400">
</p>

### NovaStar Tech（モダンスタイル）
AI/エッジコンピューティングスタートアップ — エレクトリックブルー + パープル。HTMLスライド、フローチャート。

<p align="center">
<img src="demos/screenshots/nova-01-cover.png" width="400"> <img src="demos/screenshots/nova-02-content.png" width="400"><br>
<img src="demos/screenshots/nova-03-data.png" width="400"> <img src="demos/screenshots/nova-04-flowchart.png" width="400">
</p>

### 朴叶堂（エレガントスタイル）
プレミアムウェルネス茶ブランド — オリーブグリーン + ウォームアプリコット。PowerPoint、HTMLマニュアル（A4 8ページ）。

<p align="center">
<img src="demos/screenshots/puye-01-cover.png" width="400"> <img src="demos/screenshots/puye-02-story.png" width="400"><br>
<img src="demos/screenshots/puye-03-plans.png" width="400"> <img src="demos/screenshots/puye-04-data.png" width="400">
</p>

## 支援する

logo2docs が役に立ったら、コーヒーをおごってください：

| WeChat Pay | Alipay |
|:---:|:---:|
| <img src="demos/donate/wechat-pay.jpg" width="200"> | <img src="demos/donate/alipay.jpg" width="200"> |

## Star History

<p align="center">
  <a href="https://star-history.com/#quzhi-ai/logo2docs&Date">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=quzhi-ai/logo2docs&type=Date&theme=dark" />
      <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=quzhi-ai/logo2docs&type=Date" />
      <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=quzhi-ai/logo2docs&type=Date" width="600" />
    </picture>
  </a>
</p>

## ライセンス

MIT — [LICENSE](LICENSE) を参照

## 作者

**曲直** (Justin Qu)
