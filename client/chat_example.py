#!/usr/bin/env python3
"""
チャットモデル (Gemma-3 27B) の詳細サンプル
"""

import os
from openai import OpenAI

# 環境変数から設定を取得
LITELLM_BASE_URL = os.environ.get("LITELLM_BASE_URL", "http://litellm:4000/v1")
LITELLM_API_KEY = os.environ.get("LITELLM_API_KEY", "sk-1234")

client = OpenAI(
    base_url=LITELLM_BASE_URL,
    api_key=LITELLM_API_KEY
)

MODEL_NAME = "qwen2.5-0.5b"


def simple_chat():
    """シンプルなチャット例"""
    print("\n" + "="*60)
    print("1. シンプルなチャット")
    print("="*60 + "\n")

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "user", "content": "こんにちは！あなたは誰ですか？"}
        ],
        max_tokens=150,
        temperature=0.7
    )

    print("ユーザー: こんにちは！あなたは誰ですか？")
    print(f"AI: {response.choices[0].message.content}\n")


def streaming_chat():
    """ストリーミングレスポンスの例"""
    print("\n" + "="*60)
    print("2. ストリーミングレスポンス")
    print("="*60 + "\n")

    print("ユーザー: 機械学習について簡単に説明してください。")
    print("AI: ", end="", flush=True)

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "user", "content": "機械学習について簡単に説明してください。"}
        ],
        stream=True,
        max_tokens=200,
        temperature=0.7
    )

    for chunk in response:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)

    print("\n")


def multi_turn_conversation():
    """マルチターンの会話例"""
    print("\n" + "="*60)
    print("3. マルチターンの会話")
    print("="*60 + "\n")

    conversation = [
        {"role": "user", "content": "Pythonとは何ですか？"},
    ]

    print("ユーザー: Pythonとは何ですか？")

    # 最初の応答
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=conversation,
        max_tokens=100,
        temperature=0.7
    )

    assistant_message = response.choices[0].message.content
    print(f"AI: {assistant_message}\n")

    # 会話履歴に追加
    conversation.append({"role": "assistant", "content": assistant_message})

    # フォローアップの質問
    conversation.append({"role": "user", "content": "どんな用途で使われますか？"})
    print("ユーザー: どんな用途で使われますか？")

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=conversation,
        max_tokens=150,
        temperature=0.7
    )

    print(f"AI: {response.choices[0].message.content}\n")


def temperature_comparison():
    """異なるtemperature値の比較"""
    print("\n" + "="*60)
    print("4. Temperature パラメータの比較")
    print("="*60 + "\n")

    prompt = "AIの未来について一文で述べてください。"
    temperatures = [0.3, 0.7, 1.0]

    print(f"質問: {prompt}\n")

    for temp in temperatures:
        print(f"Temperature = {temp}:")
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
            temperature=temp
        )
        print(f"  {response.choices[0].message.content}\n")


def system_prompt_example():
    """システムプロンプトの使用例"""
    print("\n" + "="*60)
    print("5. システムプロンプトの使用")
    print("="*60 + "\n")

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "あなたは親切で丁寧な日本語のアシスタントです。敬語を使って回答してください。"},
            {"role": "user", "content": "今日の天気はどうですか？"}
        ],
        max_tokens=100,
        temperature=0.7
    )

    print("システム: あなたは親切で丁寧な日本語のアシスタントです。")
    print("ユーザー: 今日の天気はどうですか？")
    print(f"AI: {response.choices[0].message.content}\n")


def main():
    print("="*60)
    print("チャットモデル (Gemma-3 27B) サンプル")
    print("="*60)
    print(f"モデル: {MODEL_NAME}")
    print(f"ベースURL: {LITELLM_BASE_URL}")
    print("="*60)

    try:
        # 各サンプルを実行
        simple_chat()
        streaming_chat()
        multi_turn_conversation()
        temperature_comparison()
        system_prompt_example()

        print("="*60)
        print("すべてのサンプルが完了しました")
        print("="*60 + "\n")

    except Exception as e:
        print(f"\nエラーが発生しました: {e}")


if __name__ == "__main__":
    main()
