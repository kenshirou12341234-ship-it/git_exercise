# Jazz Guitarist Paper

Django + TailwindCSS + PostgreSQL のプロジェクト

## 初回セットアップ

1. **リポジトリのクローン**
   ```bash
   git clone [repository-url]
   cd jazz_guitarist_paper_realbook
   ```

2. **起動**
   ```bash
   docker compose --profile development up -d
   ```

3. **アクセス**

   http://localhost:8000

**ローカルにnpm/Node.jsは不要です。** すべてDocker内で完結します。

## 開発

### 起動・停止

```bash
# 開発モード（CSS auto-rebuild有効）
docker compose --profile development up -d

# 停止
docker compose --profile development down --remove-orphans

# データベースも含めて完全にリセット
docker compose --profile development down --remove-orphans -v
```

### CSS開発

- **入力**: `static_src/styles/app.css`
- **出力**: `static/css/app.css`（自動生成）
- **設定**: `tailwind.config.ts`

開発モード（`--profile development`）では2秒ごとに自動リビルドされます。


## テスト

```bash
# すべてのテスト
docker compose --profile test run --rm test

# E2Eテストのみ
docker compose --profile test run --rm test pytest tests/e2e/ -v

# 特定ファイル
docker compose --profile test run --rm test pytest tests/e2e/test_xxx.py -v
```

## トラブルシューティング

### コンテナの状態確認

```bash
docker compose ps
```

`tailwind-init`が`Exited (0)`、`web`と`tailwind-watch`が`Up`なら正常です。

## アーキテクチャ

- **Django**: Webアプリケーション
- **PostgreSQL**: データベース
- **TailwindCSS v4**: スタイリング
- **Docker Compose**: 開発環境

### コンテナ構成

- `db`: PostgreSQL 16
- `web`: Django開発サーバー
- `tailwind-init`: 初回CSSビルド（起動時のみ実行）
- `tailwind-watch`: CSS自動リビルド（開発モードのみ）
- `test`: テスト実行環境
