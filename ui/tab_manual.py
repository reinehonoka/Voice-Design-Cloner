"""Manual tab: usage guide."""

import gradio as gr


def build_manual_tab():
    # ── 概要 ──
    gr.Markdown(
        "## VoiceDesignCloner とは\n\n"
        "**録音不要**でオリジナルの声をテキストプロンプトから作成し、"
        "コーパスを用いてその声で大量の音声を自動生成する一貫したGUIツールです。\n"
        "出力は Style-Bert-VITS2（SBV2）などのTTSモデル学習にそのまま使える教師データ形式になっています。\n\n"
        "音声合成の学習で地味に面倒な**コーパスの用意・音声の量産・リサンプル**などが、これ一つで完結します。"
    )

    gr.Markdown("---")

    # ── Voice Design 手順 ──
    gr.Markdown(
        "### Voice Design タブ — 声を作る\n\n"
        "1. **ボイスプロンプト** に作りたい声の特徴を書く\n"
        "   - どの言語でも入力できますが、英語・中国語が推奨です\n"
        "   - 翻訳ボタンで中国語・英語に変換できます\n"
        "   - 「プリセットから選ぶ」に簡単なサンプルもあります\n"
        "2. **生成パラメータ** はデフォルトのままでもOK、好みに合わせて調整も可能\n"
        "3. **読み上げテキスト** にプレビュー用の文章を入力\n"
        "4. **生成** → プレビュー再生 → 気に入らなければ **再生成**\n"
        "5. 気に入ったら **保存名** を付けて **保存**\n"
        "   - `output/voice_design/` に `{保存名}.wav` と `{保存名}.txt` がセットで保存されます\n"
        "   - 同名が存在する場合は `_1`, `_2`... が自動付与されます\n"
        "   - Voice Clone の「ショートカット」は `voice_design*.wav` 系の保存音声を対象にします"
    )

    gr.Markdown("---")

    # ── Voice Clone 手順 ──
    gr.Markdown(
        "### Voice Clone タブ — 声を量産する\n\n"
        "1. **参照音声** を選ぶ\n"
        "   - ショートカット: Voice Design で保存した声を番号で選択（書き起こしは自動入力）\n"
        "   - アップロード: 自前の音声を使う場合（その声の書き起こしを手動入力）\n"
        "2. **コーパス** を選ぶ\n"
        "   - 同梱コーパス: ita_emotion100（100文）、ita_recitation324（324文）、mana652（652文）、rohan4600（4600文）\n"
        "   - all は上記すべてをこの順番で結合したもの（5676文）\n"
        "   - アップロード: 自作の1行1文の .txt ファイルも使えます\n"
        "   - 「使用する文数」で先頭N文だけ生成可（0=すべて）\n"
        "3. **モデル** と **サンプルレート** を選択\n"
        "   - SBV2 で使うことを想定してデフォルトは 44100Hz\n"
        "4. **出力先** のフォルダ名を設定\n"
        "   - デフォルトでは `output/clone/` に出力されます\n"
        "   - `raw/` に 0001.wav 形式で連番音声、フォルダ直下に Neutral.txt（1行1文のテキストリスト）が作成されます\n"
        "5. **一括生成開始**\n\n"
        "> **■ 停止** ボタンで途中停止できます。停止後にステータスが「エラー」と表示されますが、"
        "これは Gradio の仕様です。生成済みのファイルはそのまま残り、停止します。"
    )

    gr.Markdown("---")

    # ── Tools 手順 ──
    gr.Markdown(
        "### Tools タブ — 後処理\n\n"
        "- **リサンプル**: フォルダの `raw/` 内WAVを一括変換 → `resampled/` に出力\n"
        "- **esd.list 生成**: `raw/` のWAVと `Neutral.txt` から SBV2用リストを作成\n"
        "- **音声情報**: WAVファイルの秒数・サンプルレートを確認"
    )

    gr.Markdown("---")

    # ── SBV2 受け渡し ──
    gr.Markdown(
        "### SBV2 への受け渡し\n\n"
        "1. `output/{フォルダ名}/raw/` → SBV2 の `Data/{モデル名}/raw/` にコピー\n"
        "2. Tools タブで esd.list を生成 → `Data/{モデル名}/esd.list` として配置\n"
        "3. SBV2 の WebUI で前処理 → 学習を実行"
    )

    gr.Markdown("---")

    # ── VRAM 目安 ──
    gr.Markdown(
        "### VRAM 目安\n\n"
        "| モデル | VRAM (bf16) |\n"
        "|---|---|\n"
        "| 1.7B-VoiceDesign | ~7-8 GB |\n"
        "| 1.7B-Base | ~7-8 GB |\n"
        "| 0.6B-Base | ~3-4 GB |"
    )

    gr.Markdown("---")

    # ── 推論バックエンド ──
    gr.Markdown(
        "### 推論バックエンド（Settings タブ）\n\n"
        "Settings タブでバックエンドを切り替えられます。\n\n"
        "| バックエンド | 速度 | 対応モデル | 備考 |\n"
        "|---|---|---|---|\n"
        "| **faster** | 約6-10倍速（RTF ~2.0） | 1.7B-VoiceDesign / 1.7B-Base | GPU必須。`pip install faster-qwen3-tts` が必要 |\n"
        "| **standard** | 標準速度 | すべて | CPU/GPU両対応 |\n\n"
        "**0.6B-Base は faster 非対応**です。fasterバックエンド選択中でも自動的にstandardで動作します。\n\n"
        "faster が未インストールの場合は Settings タブのバックエンド選択が無効化され、standard で動作します。"
    )
