# LLM Proxy Sample

CPU専用環境で複数のLLMモデルを単一のエンドポイントから利用できるサンプルアプリケーション。

## 概要

このプロジェクトは、**llama.cpp**と**LiteLLM Proxy**を使用して、複数のLLMモデルを統合し、OpenAI互換のAPIエンドポイントとして公開します。

### 主な特徴

- **CPU専用**: GPUなしで動作
- **OpenAI互換API**: 既存のOpenAIクライアントコードがそのまま使える
- **複数モデル対応**: チャットモデルと埋め込みモデルを同時に提供
- **Dockerベース**: 環境構築が簡単

## アーキテクチャ

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │ HTTP
       ↓
┌─────────────────────────────────┐
│     LiteLLM Proxy (:4000)       │
│  統合エンドポイント・ルーティング   │
└──────┬──────────────┬───────────┘
       │              │
       ↓              ↓
┌──────────────┐  ┌──────────────────┐
│ llama.cpp    │  │  TEI Embedding   │
│ (:8000)      │  │  (:8001)         │
│ Qwen2.5-0.5B │  │  E5-Large        │
└──────────────┘  └──────────────────┘
```

### 使用するコンポーネント

1. **llama.cpp (llama-cpp-python)**
   - Qwen2.5-0.5B-Instruct (GGUF形式)
   - CPU最適化された高速推論エンジン
   - OpenAI互換サーバー機能搭載

2. **Text Embeddings Inference (TEI)**
   - intfloat/multilingual-e5-large-instruct
   - 多言語対応の埋め込みモデル

3. **LiteLLM Proxy**
   - 統一APIエンドポイント
   - モデル間のルーティング

## セットアップ

### 1. 前提条件

- Docker & Docker Compose
- Python 3.8以上 (モデルダウンロード用)
- 8GB以上のRAM推奨

### 2. リポジトリのクローン

```bash
git clone <repository-url>
cd LLM-Proxy
```

### 3. モデルのダウンロード

```bash
# ダウンロードスクリプトを実行
./download-model.sh
```

量子化レベルを選択できます：
- **q4_k_m** (推奨): バランスの取れた品質とサイズ (~400MB)
- **q5_k_m**: 高品質だが大きめ (~500MB)
- **q3_k_m**: 軽量だが品質がやや低下 (~300MB)

### 4. 環境変数の設定

```bash
# .envファイルを作成
cp .env.example .env

# .envファイルを編集（必要に応じて）
nano .env
```

`.env`の内容:
```env
# HuggingFace Hub トークン（Readトークン）
HUGGING_FACE_HUB_TOKEN=your_token_here

# LiteLLM マスターキー（API認証用）
LITELLM_MASTER_KEY=sk-1234
```

### 5. サービスの起動

```bash
# バックグラウンドで起動
docker compose up -d

# ログを確認
docker compose logs -f
```

初回起動時は埋め込みモデルのダウンロードに数分かかります。

### 6. 動作確認

#### 利用可能なモデル一覧

```bash
curl http://localhost:4000/v1/models \
  -H "Authorization: Bearer sk-1234"
```

#### チャット補完テスト

```bash
curl http://localhost:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-1234" \
  -d '{
    "model": "qwen2.5-0.5b",
    "messages": [{"role": "user", "content": "こんにちは"}],
    "max_tokens": 50
  }'
```

#### 埋め込みテスト

```bash
curl http://localhost:4000/v1/embeddings \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-1234" \
  -d '{
    "model": "multilingual-e5-large",
    "input": "テストテキスト"
  }'
```

#### クライアントコンテナから実行

```bash
docker compose exec client python main.py
```

## Pythonクライアントの使用例

```python
from openai import OpenAI

# LiteLLM Proxyに接続
client = OpenAI(
    base_url="http://localhost:4000/v1",
    api_key="sk-1234"
)

# チャット補完
response = client.chat.completions.create(
    model="qwen2.5-0.5b",
    messages=[
        {"role": "user", "content": "こんにちは"}
    ],
    max_tokens=50
)
print(response.choices[0].message.content)

# 埋め込み
embedding = client.embeddings.create(
    model="multilingual-e5-large",
    input="テストテキスト"
)
print(f"次元数: {len(embedding.data[0].embedding)}")
```

## 利用可能なモデル

| モデル名 | 種類 | 説明 |
|---------|------|------|
| `qwen2.5-0.5b` | チャット | Qwen2.5-0.5B-Instruct (GGUF) |
| `multilingual-e5-large` | 埋め込み | 多言語E5 Large Instruct (1024次元) |

## トラブルシューティング

### llama.cppが起動しない

モデルファイルが正しくダウンロードされているか確認：
```bash
ls -lh models/
```

### メモリ不足エラー

- より小さい量子化レベル（q3_k_m）を使用
- `docker-compose.yml`の`--n_ctx`を小さくする（例: 1024）

### 埋め込みモデルのダウンロードが遅い

初回起動時は数分かかります。ログで進捗を確認：
```bash
docker compose logs -f embedding
```

## 設定のカスタマイズ

### llama.cppのパラメータ調整

`docker-compose.yml`の`llama-cpp`サービスで調整可能：

```yaml
command: >
  --model /models/qwen2.5-0.5b-instruct-q4_k_m.gguf
  --host 0.0.0.0
  --port 8000
  --n_ctx 2048          # コンテキスト長
  --n_threads 4         # CPUスレッド数
  --n_batch 512         # バッチサイズ
```

### モデルの追加

`litellm-config.yaml`に新しいモデルを追加：

```yaml
model_list:
  - model_name: your-model
    litellm_params:
      model: openai/your-model-name
      api_base: http://your-service:port/v1
      api_key: dummy
```

## 開発者向け

### ログの確認

```bash
# 全サービスのログ
docker compose logs -f

# 特定のサービスのログ
docker compose logs -f llama-cpp
docker compose logs -f litellm
```

### サービスの再起動

```bash
# 全サービス
docker compose restart

# 特定のサービス
docker compose restart llama-cpp
```

### クリーンアップ

```bash
# コンテナとボリュームを削除
docker compose down -v

# モデルファイルも削除する場合
rm -rf models/
```

## 参考リンク

- [llama-cpp-python Documentation](https://llama-cpp-python.readthedocs.io/)
- [LiteLLM Documentation](https://docs.litellm.ai/)
- [Qwen2.5 Model Card](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF)
- [Text Embeddings Inference](https://github.com/huggingface/text-embeddings-inference)

## ライセンス

このサンプルプロジェクトはMITライセンスの下で公開されています。

使用しているモデルのライセンスについては各モデルのドキュメントを参照してください：
- Qwen2.5: Apache 2.0
- E5 Multilingual: MIT
