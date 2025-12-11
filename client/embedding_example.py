#!/usr/bin/env python3
"""
埋め込みモデル (Multilingual E5 Large) の詳細サンプル
"""

import os
import numpy as np
from openai import OpenAI
from typing import List

# 環境変数から設定を取得
LITELLM_BASE_URL = os.environ.get("LITELLM_BASE_URL", "http://litellm:4000/v1")
LITELLM_API_KEY = os.environ.get("LITELLM_API_KEY", "sk-1234")

client = OpenAI(
    base_url=LITELLM_BASE_URL,
    api_key=LITELLM_API_KEY
)

MODEL_NAME = "multilingual-e5-large"


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """コサイン類似度を計算"""
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


def basic_embedding():
    """基本的な埋め込み生成"""
    print("\n" + "="*60)
    print("1. 基本的な埋め込み生成")
    print("="*60 + "\n")

    text = "機械学習は人工知能の一分野です"
    print(f"テキスト: {text}")

    response = client.embeddings.create(
        model=MODEL_NAME,
        input=text
    )

    embedding = response.data[0].embedding
    print(f"埋め込みベクトルの次元数: {len(embedding)}")
    print(f"最初の10要素: {embedding[:10]}\n")


def batch_embedding():
    """バッチでの埋め込み生成"""
    print("\n" + "="*60)
    print("2. バッチでの埋め込み生成")
    print("="*60 + "\n")

    texts = [
        "Python はプログラミング言語です",
        "Java もプログラミング言語です",
        "犬は動物です",
        "猫も動物です"
    ]

    print("テキスト:")
    for i, text in enumerate(texts, 1):
        print(f"  {i}. {text}")

    response = client.embeddings.create(
        model=MODEL_NAME,
        input=texts
    )

    embeddings = [data.embedding for data in response.data]
    print(f"\n{len(embeddings)}個の埋め込みベクトルを生成しました\n")

    return texts, embeddings


def similarity_comparison():
    """テキスト間の類似度比較"""
    print("\n" + "="*60)
    print("3. テキスト間の類似度比較")
    print("="*60 + "\n")

    texts = [
        "機械学習とディープラーニング",
        "ニューラルネットワークと深層学習",
        "今日は良い天気です",
        "明日は雨が降るでしょう"
    ]

    print("テキスト:")
    for i, text in enumerate(texts, 1):
        print(f"  {i}. {text}")

    # 埋め込みを生成
    response = client.embeddings.create(
        model=MODEL_NAME,
        input=texts
    )
    embeddings = [data.embedding for data in response.data]

    # 類似度マトリックスを計算
    print("\nコサイン類似度マトリックス:")
    print("    " + "  ".join([f"T{i+1}" for i in range(len(texts))]))

    for i in range(len(embeddings)):
        row = [f"T{i+1}"]
        for j in range(len(embeddings)):
            sim = cosine_similarity(embeddings[i], embeddings[j])
            row.append(f"{sim:.3f}")
        print("  ".join(row))

    print("\n解釈:")
    print("  - T1とT2は高い類似度（どちらも機械学習関連）")
    print("  - T3とT4も比較的高い類似度（どちらも天気関連）")
    print("  - T1/T2とT3/T4は低い類似度（異なるトピック）\n")


def semantic_search():
    """意味検索のシミュレーション"""
    print("\n" + "="*60)
    print("4. 意味検索のシミュレーション")
    print("="*60 + "\n")

    # ドキュメントコーパス
    documents = [
        "Pythonは高水準プログラミング言語で、読みやすい構文が特徴です",
        "機械学習はデータからパターンを学習するAIの手法です",
        "深層学習はニューラルネットワークを使った機械学習の一種です",
        "東京は日本の首都で、人口が最も多い都市です",
        "富士山は日本で最も高い山で、標高3776メートルです",
        "Webスクレイピングはウェブサイトからデータを抽出する技術です"
    ]

    print("ドキュメントコーパス:")
    for i, doc in enumerate(documents, 1):
        print(f"  {i}. {doc}")

    # ドキュメントの埋め込みを生成
    print("\nドキュメントの埋め込みを生成中...")
    doc_response = client.embeddings.create(
        model=MODEL_NAME,
        input=documents
    )
    doc_embeddings = [data.embedding for data in doc_response.data]

    # クエリ
    query = "AIと機械学習について教えてください"
    print(f"\nクエリ: {query}")

    # クエリの埋め込みを生成
    query_response = client.embeddings.create(
        model=MODEL_NAME,
        input=query
    )
    query_embedding = query_response.data[0].embedding

    # 類似度を計算してランキング
    similarities = [
        (i, cosine_similarity(query_embedding, doc_emb))
        for i, doc_emb in enumerate(doc_embeddings)
    ]
    similarities.sort(key=lambda x: x[1], reverse=True)

    print("\n検索結果（類似度順）:")
    for rank, (doc_idx, sim) in enumerate(similarities, 1):
        print(f"  {rank}位 (類似度: {sim:.4f}): {documents[doc_idx]}")

    print()


def multilingual_example():
    """多言語サポートのデモ"""
    print("\n" + "="*60)
    print("5. 多言語サポート")
    print("="*60 + "\n")

    texts = [
        "こんにちは、世界",  # 日本語
        "Hello, world",      # 英語
        "你好，世界",         # 中国語
        "Hola, mundo"        # スペイン語
    ]

    print("異なる言語で同じ意味のテキスト:")
    for i, text in enumerate(texts, 1):
        print(f"  {i}. {text}")

    # 埋め込みを生成
    response = client.embeddings.create(
        model=MODEL_NAME,
        input=texts
    )
    embeddings = [data.embedding for data in response.data]

    # 類似度を計算
    print("\nコサイン類似度:")
    for i in range(len(embeddings)):
        for j in range(i + 1, len(embeddings)):
            sim = cosine_similarity(embeddings[i], embeddings[j])
            print(f"  {texts[i]} vs {texts[j]}: {sim:.4f}")

    print("\n多言語モデルは異なる言語でも意味的に類似したテキストを")
    print("近い埋め込み空間にマッピングできます。\n")


def main():
    print("="*60)
    print("埋め込みモデル (Multilingual E5 Large) サンプル")
    print("="*60)
    print(f"モデル: {MODEL_NAME}")
    print(f"ベースURL: {LITELLM_BASE_URL}")
    print("="*60)

    try:
        # 各サンプルを実行
        basic_embedding()
        batch_embedding()
        similarity_comparison()
        semantic_search()
        multilingual_example()

        print("="*60)
        print("すべてのサンプルが完了しました")
        print("="*60 + "\n")

    except Exception as e:
        print(f"\nエラーが発生しました: {e}")


if __name__ == "__main__":
    main()
