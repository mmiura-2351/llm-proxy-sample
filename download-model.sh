#!/bin/bash

# Qwen2.5-0.5B-Instruct GGUF モデルダウンロードスクリプト

set -e

echo "=========================================="
echo "Qwen2.5-0.5B-Instruct GGUF モデルダウンロード"
echo "=========================================="
echo

# モデル保存先ディレクトリを作成
MODEL_DIR="./models"
mkdir -p "$MODEL_DIR"

# 量子化レベルを選択
echo "量子化レベルを選択してください:"
echo "1) q4_k_m (推奨・バランス型) - 約400MB"
echo "2) q5_k_m (高品質) - 約500MB"
echo "3) q3_k_m (軽量) - 約300MB"
echo
read -p "選択 (1-3) [デフォルト: 1]: " QUANT_CHOICE
QUANT_CHOICE=${QUANT_CHOICE:-1}

case $QUANT_CHOICE in
  1)
    QUANT="q4_k_m"
    ;;
  2)
    QUANT="q5_k_m"
    ;;
  3)
    QUANT="q3_k_m"
    ;;
  *)
    echo "無効な選択です。q4_k_mを使用します。"
    QUANT="q4_k_m"
    ;;
esac

MODEL_FILE="qwen2.5-0.5b-instruct-${QUANT}.gguf"
echo
echo "ダウンロード中: $MODEL_FILE"
echo

# huggingface-cliがインストールされているか確認
if ! command -v huggingface-cli &> /dev/null; then
    echo "huggingface-cli が見つかりません。インストール中..."
    pip install -U "huggingface_hub[cli]"
fi

# モデルをダウンロード
huggingface-cli download \
    Qwen/Qwen2.5-0.5B-Instruct-GGUF \
    "$MODEL_FILE" \
    --local-dir "$MODEL_DIR" \
    --local-dir-use-symlinks False

echo
echo "=========================================="
echo "ダウンロード完了！"
echo "モデルファイル: $MODEL_DIR/$MODEL_FILE"
echo "=========================================="
echo
echo "次のステップ:"
echo "1. .env ファイルを作成してください"
echo "   cp .env.example .env"
echo "2. 必要に応じて .env を編集してください"
echo "3. Docker Compose でサービスを起動してください"
echo "   docker compose up -d"
echo
