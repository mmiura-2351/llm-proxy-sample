# LLM Proxy - 最小構成

vLLM、TEI、LiteLLMを使用したCPU専用の最小構成LLMプロキシです。

## 構成

```
┌──────────┐
│  Client  │
└─────┬────┘
      │
      ↓
┌──────────┐
│ LiteLLM  │ :4000
└─────┬────┘
      │
  ┌───┴────┐
  ↓        ↓
┌─────┐  ┌────┐
│vLLM │  │TEI │
│Qwen │  │ E5 │
│8000 │  │8001│
└─────┘  └────┘
```

## 使用モデル

- **Qwen2.5-0.5B** (チャット): `Qwen/Qwen2.5-0.5B-Instruct` (約500MB)
- **E5 Large** (埋め込み): `intfloat/multilingual-e5-large-instruct` (約1.5GB)

## セットアップ

### 1. 環境変数

```bash
cp .env.example .env
nano .env
```

```bash
HUGGING_FACE_HUB_TOKEN=your_token_here
LITELLM_MASTER_KEY=sk-1234
```

### 2. 起動

```bash
docker-compose up -d
```

### 3. 確認

```bash
curl http://localhost:4000/health
```

## 使用方法

### クライアントコンテナから

```bash
docker-compose exec client python main.py
```

### ホストから

```bash
# チャット
curl http://localhost:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-1234" \
  -d '{
    "model": "qwen2.5-0.5b",
    "messages": [{"role": "user", "content": "Hello"}]
  }'

# 埋め込み
curl http://localhost:4000/v1/embeddings \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-1234" \
  -d '{
    "model": "multilingual-e5-large",
    "input": "テキスト"
  }'
```

### Python

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:4000/v1",
    api_key="sk-1234"
)

# チャット
response = client.chat.completions.create(
    model="qwen2.5-0.5b",
    messages=[{"role": "user", "content": "Hello"}]
)

# 埋め込み
embedding = client.embeddings.create(
    model="multilingual-e5-large",
    input="テキスト"
)
```

## ファイル構成

```
LLM-Proxy/
├── docker-compose.yml    # サービス定義
├── litellm-config.yaml   # LiteLLM設定
├── .env.example          # 環境変数
├── README.md
└── client/               # クライアントコンテナ
    ├── Dockerfile
    ├── requirements.txt
    └── main.py
```

## コマンド

```bash
# 起動
docker-compose up -d

# ログ
docker-compose logs -f

# 停止
docker-compose down

# 削除（キャッシュも）
docker-compose down -v
```

## 必要リソース

- CPU: 2コア以上
- RAM: 4GB以上
- Disk: 3GB以上

## 備考

- Redis/PostgreSQL不要
- ネットワーク設定不要（Dockerが自動設定）
- コンテナ名でDNS解決
