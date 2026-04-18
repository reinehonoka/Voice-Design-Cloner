# VoiceDesignCloner

**A training data creation tool for building complete TTS models from original AI voices — no recording required.**

Solves the hardest problems in voice synthesis: **recording, corpus building, bulk generation, and resampling**.

A GUI tool for [Qwen3-TTS](https://huggingface.co/Qwen/Qwen3-TTS) VoiceDesign and VoiceClone.
From voice design to generating training data for [Style-Bert-VITS2](https://github.com/litagin02/Style-Bert-VITS2) — all in one place.

**Switch UI language, bundled corpus, and generation language with one click — JA / EN / ZH / KO supported**

---

## Overview

**Solves the voice problems that have been holding back AI Tubers, AI characters, game voice, and narration production.**

- Can't prepare original recordings, so you can't create a voice
- Running zero-shot inference without a proper TTS model
- Corpus collection and bulk audio generation are too much work

Voice design, bulk generation, and preprocessing — done in just a few button clicks.

**What you can do:**
- **Voice Design** — Generate a completely original voice from scratch using text prompts
- **Voice Gacha** — Keep regenerating until you find the voice you love
- **Bulk Corpus Synthesis** — Generate hundreds to thousands of lines with your chosen voice at the push of a button
- **Resample & esd.list generation** — Preprocessing for Style-Bert-VITS2 training, all handled automatically

Output is in Style-Bert-VITS2 training data format (44.1kHz WAV + esd.list), ready to use directly.
Output can also be used with other TTS engines.

---

## Screenshots

![screenshot](assets/screenshot1.png)

---

## Requirements

| Item | Requirement |
|---|---|
| OS | Windows 11 / Linux WSL2 (tested) |
| Python | 3.10–3.12 (recommended: 3.12) |
| GPU | NVIDIA (CUDA required) |
| VRAM | 8GB+ (recommended: 16GB) |

**Tested environments:**

| OS | GPU | VRAM | RAM |
|---|---|---|---|
| Windows 11 | RTX 4060 Ti | 16GB | 128GB |
| Windows 11 | RTX 3060 | 12GB | 64GB |
| Windows 11 / WSL2 (Ubuntu 22.04) | RTX 5070 | 12GB | — |
| Windows 11 (VRAM 8GB) | — | 8GB | — |

> CPU-only operation has not been tested.

---

## Installation

```
1. Clone this repository or download as ZIP
2. Double-click setup.bat to run
3. After setup, launch with app.bat
```

**On Linux, use `setup.sh` / `app.sh`. Tested on WSL2 (Ubuntu 22.04).**

`setup.bat` automatically handles venv creation, PyTorch, and all dependency installation.

If an NVIDIA GPU is detected, **faster-qwen3-tts** is installed automatically.
To add it manually later:

```
venv\Scripts\activate
pip install faster-qwen3-tts
```

> **First launch note**: On the first run, the faster backend may fall back to standard. From the second run onward, faster will work correctly.

---

## Usage

After launching, step-by-step instructions are available in the **Manual tab** inside the app.

General workflow:

```
1. [Voice Design] tab — Design, preview, and save your voice
2. [Voice Clone]  tab — Bulk synthesize your corpus with the saved voice
3. [Tools]        tab — Resample and generate esd.list
4. [Settings]     tab — Check and switch inference backend
```

Steps 1 and 2 are all you need for basic use.

> **Note**: Pressing the stop button in Voice Clone will show "Error" in the status display. This is a Gradio behavior — the process has actually stopped correctly. All generated files are preserved.

---

## Supported Languages

### UI Language

Switchable from the Settings tab.

| Language | Code |
|---|---|
| Japanese | JA |
| English | EN |
| Chinese | ZH |
| Korean | KO |

### Voice Generation Language (Qwen3-TTS)

Both Voice Design and Voice Clone support the following 10 languages.
When using bundled corpora (JA/EN/ZH), the corpus language selector syncs automatically.
When using your own corpus, you can generate in all 10 languages.

| Language | Language |
|---|---|
| Japanese | Korean |
| English | German |
| Chinese | French |
| Spanish | Italian |
| Portuguese | Russian |

---

## Bundled Corpora

| File | Lines | Content |
|---|---|---|
| ita_emotion100.txt | 100 | ITA corpus (emotional expressions) |
| ita_recitation324.txt | 324 | ITA corpus (recitation) |
| mana652.txt | 652 | MANA corpus |
| rohan4600.txt | 4600 | ROHAN corpus |

Japanese (JA) is included as-is. English (EN) and Chinese (ZH) were translated offline using M2M-100, with all looping outputs and unknown token artifacts (`<unk>`) manually corrected.

---

## Passing Data to Style-Bert-VITS2

```
1. Copy the contents of output/{folder}/raw/ to Style-Bert-VITS2's Data/{model}/raw/
2. Generate esd.list using "Generate esd.list" in the Tools tab
3. Run preprocessing → training in the Style-Bert-VITS2 WebUI
```

esd.list format:
```
0001.wav|{speaker_name}|JP|text content
0002.wav|{speaker_name}|JP|text content
```

> **Note**: The language column can be set to JP / EN / ZH from the Tools tab.

---

## Inference Backends

| Backend | Speed | Supported Models |
|---|---|---|
| **faster** (recommended) | ~6–10x faster (RTF ~2.0) | 1.7B-VoiceDesign / 1.7B-Base |
| **standard** | Standard speed | All (CPU/GPU) |

The faster backend uses CUDA Graph optimization via [faster-qwen3-tts](https://github.com/andimarafioti/faster-qwen3-tts).
**0.6B-Base is not supported by faster** — when faster is selected, it automatically falls back to standard for this model.

---

## License

This tool: [MIT License](LICENSE)

OSS used:
- [Qwen3-TTS](https://huggingface.co/Qwen/Qwen3-TTS) — Apache License 2.0
- [faster-qwen3-tts](https://github.com/andimarafioti/faster-qwen3-tts) — Apache License 2.0
- [M2M-100](https://huggingface.co/facebook/m2m100_418M) — MIT License
- [Gradio](https://github.com/gradio-app/gradio) — Apache License 2.0
- ITA corpus / ROHAN corpus / MANA corpus — Public Domain

Details: [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md)

---

## Disclaimer

This tool is a GUI wrapper for Qwen3-TTS (Apache License 2.0).

### About Qwen3-TTS Training Data

The training data of Qwen3-TTS is a black box — its contents and rights status have not been disclosed.
For commercial use, please carefully review the Qwen3-TTS terms of service.

### Publicity Rights, Copyright, and Related Laws

Cloning or using the voice of a real person, talent, or voice actor for commercial purposes without permission may constitute infringement of publicity rights, copyright, unfair competition prevention laws, and other applicable regulations.
The legal risks differ significantly between personal and commercial use.

### Prohibited Uses

- Use for fraud, impersonation, or defamation
- Generation or distribution of audio content that is illegal or infringes on rights

### Other

- The developer assumes no responsibility for any audio content generated with this tool
- This software is provided as-is, without any warranty of any kind

---

## Support / Contact

- Bug reports & feature requests: Please use GitHub Issues in this repository
- Other inquiries: Please DM via [Reine Honoka's X account](https://x.com/ReineHonoka)

## Special Thanks

Thank you to everyone who contributed to the development of this project.

### Testers

- [フルエレ](https://x.com/fluele_alpha?s=20)
- [きんくまん](https://x.com/kinkuman_net?s=20)
- [ヒロナ](https://x.com/hirona98?s=20)

### Contributors
- kinkuman — fix: setup.sh numpy pre-install & pip upgrade
