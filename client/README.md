# クライアントコンテナ

このディレクトリには、LiteLLM Proxyを使用してモデルを呼び出すクライアントアプリケーションが含まれています。

## 概要

このクライアントは、同一のベースURL (`http://litellm:4000/v1`) を使用して以下の2つのモデルを呼び出します:

1. **Gemma-3 27B** (チャットモデル) - vLLM経由でCPU上で動作
2. **Multilingual E5 Large** (埋め込みモデル) - TEI経由でCPU上で動作

## ファイル構成

```
client/
├── Dockerfile          # クライアントコンテナのビルド定義
├── requirements.txt    # Python依存パッケージ
├── main.py            # メインサンプルスクリプト
├── chat_example.py    # チャットモデルの詳細サンプル
├── embedding_example.py # 埋め込みモデルの詳細サンプル
└── README.md          # このファイル
```

## 使用方法

### 1. コンテナ内でスクリプトを実行

すべてのサービスが起動している状態で:

```bash
# メインサンプルを実行
docker-compose exec client python main.py

# チャットサンプルを実行
docker-compose exec client python chat_example.py

# 埋め込みサンプルを実行
docker-compose exec client python embedding_example.py
```

### 2. コンテナに入って対話的に実行

```bash
# コンテナに入る
docker-compose exec client bash

# 任意のスクリプトを実行
python main.py
python chat_example.py
python embedding_example.py

# Pythonインタラクティブシェルで試す
python
>>> from openai import OpenAI
>>> client = OpenAI(base_url="http://litellm:4000/v1", api_key="sk-1234")
>>> response = client.chat.completions.create(model="gemma-3-27b", messages=[{"role": "user", "content": "Hello"}])
```

### 3. ホストから実行（開発用）

```bash
cd client
pip install -r requirements.txt

# 環境変数を設定
export LITELLM_BASE_URL="http://localhost:4000/v1"
export LITELLM_API_KEY="sk-1234"

# スクリプトを実行
python main.py
```

## スクリプトの説明

### main.py

両方のモデル（チャットと埋め込み）を使用する統合サンプル。

実行内容:
- 利用可能なモデルの一覧表示
- Gemma-3でチャット応答を生成
- Multilingual E5で埋め込みベクトルを生成し、類似度を計算

### chat_example.py

チャットモデル（Gemma-3）の詳細なサンプル。

機能:
- 基本的なチャット
- ストリーミング応答
- マルチターンの会話
- パラメータ調整（temperature, max_tokensなど）

### embedding_example.py

埋め込みモデル（Multilingual E5）の詳細なサンプル。

機能:
- テキストの埋め込みベクトル生成
- 類似度検索
- ドキュメント検索のシミュレーション
- バッチ処理

## カスタマイズ

### 独自のスクリプトを追加

1. `client/`ディレクトリに新しい`.py`ファイルを作成
2. OpenAI SDKを使用してコードを記述
3. コンテナ内で実行

例:
```python
# my_script.py
from openai import OpenAI
import os

client = OpenAI(
    base_url=os.environ["LITELLM_BASE_URL"],
    api_key=os.environ["LITELLM_API_KEY"]
)

# あなたのコード
response = client.chat.completions.create(
    model="gemma-3-27b",
    messages=[{"role": "user", "content": "カスタムクエリ"}]
)
print(response.choices[0].message.content)
```

### 依存パッケージの追加

1. `requirements.txt`に追加
2. コンテナを再ビルド:
```bash
docker-compose build client
docker-compose up -d client
```

## トラブルシューティング

### 接続エラー

```
Error: Connection refused
```

原因: LiteLLMプロキシが起動していない

解決策:
```bash
docker-compose ps  # サービスの状態を確認
docker-compose logs litellm  # ログを確認
```

### タイムアウトエラー

```
Error: Timeout
```

原因: CPUモデルは推論に時間がかかる

解決策: `litellm-config.yaml`の`request_timeout`を増やす（現在1200秒に設定済み）

### モデルが見つからない

```
Error: Model not found
```

解決策: モデル名を確認
```bash
docker-compose exec client python -c "from openai import OpenAI; client = OpenAI(base_url='http://litellm:4000/v1', api_key='sk-1234'); print([m.id for m in client.models.list().data])"
```

## パフォーマンスについて

CPUでの推論は遅いため、以下に注意:

- **Gemma-3 27B**: 1回答あたり数分かかる場合があります
- **Multilingual E5**: 埋め込み生成は比較的高速（数秒）

本番環境ではGPUの使用を推奨します。
