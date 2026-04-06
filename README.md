# VoiceDesignCloner

**録音不要でオリジナルなAI音声から完全なTTSモデルを作るための教師データ作成ツール。**

音声合成で大変な**録音・コーパス構築・量産・リサンプル**の問題を解決。

[Qwen3-TTS](https://huggingface.co/Qwen/Qwen3-TTS) の VoiceDesign と VoiceClone を GUI で操作できるツールです。
声の設計から [Style-Bert-VITS2](https://github.com/litagin02/Style-Bert-VITS2) の学習に必要な教師データ作成まで、一気通貫で完結します。

---

## 概要

**AITuberやAIキャラ、ゲームボイスやナレーション制作に悩んでいた音声問題をまとめて解決。**

- オリジナルの録音が用意できず、声を作れない
- ゼロショット運用のまま、まともなTTSモデルを動かせていない
- コーパス集めと大量音声生成が大変

声の設計・量産・前処理まで、数回のボタン操作で完結。

**できること：**
- **声の設計** — テキストプロンプトでゼロからオリジナルの声を生成
- **声ガチャ** — 気に入るまで何度でもやり直し可能
- **コーパス一括音声化** — 選んだ声で数百〜数千文をボタン一つで量産
- **リサンプル・esd.list生成** — Style-Bert-VITS2学習に必要な前処理まで完結

出力はStyle-Bert-VITS2の学習データ形式（44.1kHz WAV + esd.list）で直接渡せます。
その他音声合成エンジンでも使用できる形で出力できます。

---

## スクリーンショット

![screenshot](assets/スクリーンショット%202026-04-01%20210218.png)

---

## 必要環境

| 項目 | 要件 |
|---|---|
| OS | Windows 11 / Linux WSL2（動作確認済み） |
| Python | 3.10〜3.12（推奨: 3.12） |
| GPU | NVIDIA（CUDA対応） |
| VRAM | 8GB〜（推奨: 16GB） |

**動作確認済み環境:**

| OS | GPU | VRAM | RAM |
|---|---|---|---|
| Windows 11 | RTX 4060 Ti | 16GB | 128GB |
| Windows 11 | RTX 3060 | 12GB | 64GB |
| Windows 11 / WSL2 (Ubuntu 22.04) | RTX 5070 | 12GB | — |
| Windows 11 (VRAM 8GB) | — | 8GB | — |

> CPU 単体動作は未確認です。

---

## インストール

```
1. このリポジトリをクローンまたはZIPでダウンロード
2. setup.bat をダブルクリックして実行
3. 完了後、app.bat で起動
```

**Linux の場合は `setup.sh` / `app.sh` を使用してください。WSL2 (Ubuntu 22.04) で動作確認済みです。**

`setup.bat` が venv の作成・PyTorch・依存ライブラリのインストールをすべて自動で行います。

NVIDIA GPU が検出された場合、**faster-qwen3-tts** は自動でインストールされます。
後から追加する場合：

```
venv\Scripts\activate
pip install faster-qwen3-tts
```

> **初回起動について**: 初回のみ faster バックエンドが standard にフォールバックすることがあります。2回目以降は正常に faster で動作します。

---

## 使い方

起動後、アプリ内の **Manual タブ** に手順が記載されています。

大まかな流れ：

```
1. [Voice Design] タブ — 声を設計・プレビュー・保存
2. [Voice Clone]  タブ — 保存した声でコーパスを一括音声化
3. [Tools]        タブ — リサンプル・esd.list 生成
4. [Settings]     タブ — 推論バックエンド確認・切替
```

基本1と2だけで完結します。

> **注意**: Voice Clone の停止ボタンを押すと、ステータスが「エラー」と表示されます。これは Gradio の仕様で、実際には正常に停止しています。生成済みのファイルはそのまま残ります。

---

## Style-Bert-VITS2 への受け渡し

```
1. output/{フォルダ名}/raw/ の中身を Style-Bert-VITS2 の Data/{モデル名}/raw/ にコピー
2. Tools タブの「esd.list 生成」で esd.list を作成
3. Style-Bert-VITS2 の WebUI で前処理 → 学習を実行
```

esd.list の形式：
```
0001.wav|{話者名}|JP|テキスト内容
0002.wav|{話者名}|JP|テキスト内容
```

> **注意**: 言語列は `JP` 固定です。梱包コーパスはすべて日本語を前提としています。

---

## 推論バックエンド

| バックエンド | 速度 | 対応モデル |
|---|---|---|
| **faster**（推奨） | 約6-10倍速（RTF ~2.0） | 1.7B-VoiceDesign / 1.7B-Base |
| **standard** | 標準速度 | すべて（CPU/GPU） |

faster バックエンドは [faster-qwen3-tts](https://github.com/andimarafioti/faster-qwen3-tts) による CUDA Graph 最適化を使用。
**0.6B-Base は faster 非対応**のため、fasterバックエンド選択中でも自動的に standard で動作します。

---

## ライセンス

本ツール: [MIT License](LICENSE)

使用しているOSS:
- [Qwen3-TTS](https://huggingface.co/Qwen/Qwen3-TTS) — Apache License 2.0
- [faster-qwen3-tts](https://github.com/andimarafioti/faster-qwen3-tts) — Apache License 2.0
- [M2M-100](https://huggingface.co/facebook/m2m100_418M) — MIT License
- [Gradio](https://github.com/gradio-app/gradio) — Apache License 2.0
- ITAコーパス / ROHANコーパス / MANAコーパス — Public Domain

詳細: [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md)

---

## 免責事項

本ツールは Qwen3-TTS（Apache License 2.0）の GUI ラッパーです。

### Qwen3-TTS の学習データについて

Qwen3-TTS の学習データはブラックボックスであり、その内容・権利状況は公開されていません。
商用利用の際は Qwen3-TTS の利用規約を十分に確認してください。

### パブリシティ権・著作権・関連法令について

実在の人物・タレント・声優の声を商用目的で無断クローン・使用することは、
パブリシティ権・著作権・不正競争防止法等の権利侵害に該当する可能性があります。
個人利用と商用利用では法的リスクが大きく異なります。

### 禁止事項

- 詐欺・なりすまし・誹謗中傷を目的とした利用
- 違法または権利侵害となる音声コンテンツの生成・配布

### その他

- 生成した音声コンテンツについて、開発者は一切の責任を負いません
- 本ソフトウェアは現状のまま提供され、いかなる保証も伴いません

---

## サポート / 連絡先

- バグ報告・機能要望: このリポジトリの GitHub Issues を利用してください
- その他の連絡: [零音ほのかのXアカウント](https://x.com/ReineHonoka)のDMにてお願いいたします。

## Special Thanks

このプロジェクトの開発にご協力いただいた皆様に感謝いたします。

### Testers

- [フルエレ](https://x.com/fluele_alpha?s=20)
- [きんくまん](https://x.com/kinkuman_net?s=20)
- [ヒロナ](https://x.com/hirona98?s=20)

### Contributors
- kinkuman — fix: setup.sh numpy pre-install & pip upgrade