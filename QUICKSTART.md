# クイックスタート

5分でLLM Proxyを動かす最短手順です。

## 1. モデルのダウンロード

```bash
./download-model.sh
```

量子化レベルを選択（推奨: 1 = q4_k_m）

## 2. 環境変数設定

```bash
cp .env.example .env
nano .env
```

HuggingFace Tokenを設定:
```bash
HUGGING_FACE_HUB_TOKEN=hf_xxxxx
LITELLM_MASTER_KEY=sk-1234
```

## 3. 起動

```bash
docker compose up -d
```

初回は埋め込みモデルのダウンロードに3-5分かかります。

ログ確認:
```bash
docker compose logs -f
```

## 4. 動作確認

### モデル一覧
```bash
curl http://localhost:4000/v1/models -H "Authorization: Bearer sk-1234"
```

### チャット
```bash
curl http://localhost:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-1234" \
  -d '{"model":"qwen2.5-0.5b","messages":[{"role":"user","content":"こんにちは"}]}'
```

### クライアントから実行
```bash
docker compose exec client python main.py
```

## 停止

```bash
docker compose down
```

完全削除（キャッシュも）:
```bash
docker compose down -v
rm -rf models/
```

## トラブルシューティング

### llama.cppが起動しない
```bash
ls -lh models/  # モデルファイル確認
```

### メモリ不足
より小さい量子化（q3_k_m）を使用するか、docker-compose.ymlで`--n_ctx 1024`に変更

詳細は[README.md](README.md)を参照してください。
