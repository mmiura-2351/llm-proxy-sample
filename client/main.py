#!/usr/bin/env python3
"""
LiteLLM Proxyクライアントのサンプル
"""

import os
from openai import OpenAI

# 環境変数から設定を取得
API_KEY = os.environ.get("LITELLM_API_KEY", "sk-1234")

# LiteLLMに接続（コンテナ名で指定）
client = OpenAI(
    base_url="http://litellm:4000/v1",
    api_key=API_KEY
)

print("="*60)
print("LiteLLM Proxy クライアント")
print("="*60)
print()

# 1. モデル一覧
print("1. 利用可能なモデル:")
try:
    models = client.models.list()
    for model in models.data:
        print(f"  - {model.id}")
except Exception as e:
    print(f"  エラー: {e}")
print()

# 2. チャット
print("2. チャット (Qwen2.5-0.5B):")
try:
    response = client.chat.completions.create(
        model="qwen2.5-0.5b",
        messages=[{"role": "user", "content": "こんにちは"}],
        max_tokens=50
    )
    print(f"  応答: {response.choices[0].message.content}")
except Exception as e:
    print(f"  エラー: {e}")
print()

# 3. 埋め込み
print("3. 埋め込み (E5):")
try:
    response = client.embeddings.create(
        model="multilingual-e5-large",
        input="テスト"
    )
    embedding = response.data[0].embedding
    print(f"  次元数: {len(embedding)}")
    print(f"  最初の5要素: {embedding[:5]}")
except Exception as e:
    print(f"  エラー: {e}")
print()

print("="*60)
print("完了")
print("="*60)
