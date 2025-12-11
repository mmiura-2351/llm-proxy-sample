# クイックスタート

## 1. 環境変数設定

```bash
cp .env.example .env
nano .env
```

HuggingFace Tokenを設定:
```bash
HUGGING_FACE_HUB_TOKEN=hf_xxxxx
```

## 2. 起動

```bash
docker-compose up -d
docker-compose logs -f  # ログ監視
```

初回はモデルダウンロードに3-5分かかります（約2GB）。

## 3. 動作確認

```bash
curl http://localhost:4000/health
```

## 4. 実行

```bash
docker-compose exec client python main.py
```

## 停止

```bash
docker-compose down
```
