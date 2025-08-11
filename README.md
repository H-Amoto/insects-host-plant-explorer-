# 昆虫・寄主植物探索サイト + リポジトリ整備ツール

昆虫と寄主植物の関係を探索できる静的サイトです。リポジトリ整備と画像最適化の自動化ツールも含まれています。

## サイト機能

React + Viteで構築された昆虫・寄主植物データベースの検索・閲覧サイトです。

## リポジトリ整備ツール

### 機能

- 不要ファイルの除去・アーカイブ
- CSVファイルの世代管理
- 画像の自動最適化（WebP/AVIF生成）
- GitHub Actionsによる自動画像最適化

### セットアップ

```bash
# 依存関係のインストール
npm install

# 画像最適化用ライブラリのインストール
npm install sharp --save-dev
```

### 使い方

#### 1. リポジトリのクリーンアップ

```bash
# ステップ1: インベントリ作成
node scripts/cleanup-inventory.mjs

# ステップ2: ドライラン（確認）
node scripts/cleanup-apply.mjs --dry-run

# ステップ3: 実行
node scripts/cleanup-apply.mjs --apply
```

#### 2. 画像の最適化

```bash
# すべての画像を最適化
node scripts/optimize-images.mjs

# 特定の画像を最適化
node scripts/optimize-images.mjs path/to/image.jpg
```

### GitHub Actions自動最適化

`images/originals/`に画像を追加すると自動的に：
1. WebP版を生成（品質: 82）
2. AVIF版を生成（品質: 60）
3. プルリクエストを作成

### ディレクトリ構造

```
├── scripts/              # 整備スクリプト
├── reports/              # 実行レポート
├── images/originals/     # 元画像
├── public/images/        # 最適化済み画像
├── data/archive/         # アーカイブCSV
└── misc/archive/         # その他アーカイブ
```

## 開発

```bash
# 開発サーバー起動
npm run dev

# ビルド
npm run build

# デプロイ
npm run deploy
```
