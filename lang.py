"""Internationalization strings for VoiceDesignCloner.

Supported languages: ja (Japanese), en (English), zh (Chinese), ko (Korean)
"""

_STRINGS: dict[str, dict[str, str]] = {
    "ja": {
        # ── App ──
        "app_title": "VoiceDesignCloner",
        # ── Tab names ──
        "tab_voice_design": "ボイスデザイン",
        "tab_voice_clone": "ボイスクローン",
        "tab_lora": "LoRA学習",
        "tab_irodori_infer": "Irodori推論",
        "tab_tools": "ツール",
        "tab_settings": "設定",
        "tab_manual": "マニュアル",
        # ── Voice Design tab ──
        "vd_prompt_section": "### 1. ボイスプロンプト",
        "vd_prompt_desc": "生成したい声の特徴を記述（言語不問）",
        "vd_prompt_label": "LLMプロンプト",
        "vd_prompt_placeholder": "例: 落ち着いた大人の女性の声、低めのトーン（日本語OK → 下のボタンで翻訳）",
        "vd_btn_translate_ja": "日本語に翻訳",
        "vd_btn_translate_zh": "中国語に翻訳",
        "vd_btn_translate_en": "英語に翻訳",
        "vd_preset_accordion": "プリセットから選ぶ",
        "vd_preset_ja_label": "日本語",
        "vd_preset_zh_label": "中国語",
        "vd_preset_en_label": "英語",
        "vd_btn_clear_preset": "クリア",
        "vd_params_section": "### 2. 生成パラメータ",
        "vd_temperature_label": "Temperature（高い=表現豊か / 低い=安定）",
        "vd_top_p_label": "Top-P（低いほど品質安定）",
        "vd_top_k_label": "Top-K（候補トークン数）",
        "vd_rep_penalty_label": "繰り返しペナルティ",
        "vd_btn_reset_params": "デフォルトに戻す",
        "vd_sample_section": "### 3. 読み上げテキスト",
        "vd_sample_desc": "この声で読み上げる文章",
        "vd_sample_label": "読み上げテキスト",
        "vd_tts_lang_label": "音声生成言語",
        "vd_preview_section": "### 4. プレビュー",
        "vd_preview_label": "プレビュー",
        "vd_status_label": "ステータス",
        "vd_btn_generate": "生成",
        "vd_btn_reroll": "再生成",
        "vd_save_section": "### 5. 保存",
        "vd_save_name_label": "保存名",
        "vd_btn_save": "保存",
        # vd messages
        "vd_err_empty_prompt": "ボイス指示が空です",
        "vd_err_translate_empty": "テキストを入力してください",
        "vd_err_translate_fail": "翻訳エラー: {}",
        "vd_err_generate_fail": "エラー: {}",
        "vd_ok_generated": "生成完了 ({}Hz)",
        "vd_err_no_audio": "保存する音声がありません",
        "vd_ok_saved": "保存完了: {}",
        "vd_err_save_fail": "エラー: {}",
        # ── Voice Clone tab ──
        "vc_ref_section": "### 1. 参照音声",
        "vc_ref_tab_shortcut": "ショートカット",
        "vc_ref_tab_upload": "アップロード",
        "vc_shortcut_label": "voice_design 番号",
        "vc_upload_audio_label": "音声ファイル",
        "vc_ref_text_label": "参照音声の書き起こし",
        "vc_ref_text_placeholder": "ショートカットなら自動入力",
        "vc_btn_refresh_ref": "リスト更新",
        "vc_corpus_section": "### 2. コーパス",
        "vc_corpus_tab_file": "ファイル選択",
        "vc_corpus_tab_upload": "アップロード",
        "vc_corpus_file_label": "コーパスファイル",
        "vc_corpus_lang_label": "コーパス言語",
        "vc_corpus_upload_label": "テキストファイル（1行1文の.txt）",
        "vc_corpus_count_label": "使用する文数（0=すべて）",
        "vc_corpus_total_lines_label": "総文数",
        "vc_corpus_total_chars_label": "総文字数",
        "vc_btn_corpus_refresh": "コーパス情報を更新",
        "vc_settings_section": "### 3. 設定",
        "vc_model_label": "モデル",
        "vc_lang_label": "言語",
        "vc_sr_label": "出力サンプルレート (Hz)",
        "vc_output_section": "### 出力先（output/）",
        "vc_output_folder_label": "フォルダ名",
        "vc_wavs_folder_label": "音声サブフォルダ名",
        "vc_esd_filename_label": "テキストリスト名（.txt自動付与）",
        "vc_btn_start": "一括生成開始",
        "vc_btn_stop": "■ 停止",
        "vc_progress_section": "### 4. 進捗",
        "vc_progress_label": "ステータス",
        "vc_result_label": "結果",
        # vc messages
        "vc_err_no_ref": "エラー: 参照音声がありません",
        "vc_err_ref_not_found": "エラー: 参照音声が見つかりません",
        "vc_err_empty_ref_text": "エラー: 書き起こしテキストが空です",
        "vc_err_no_text": "エラー: テキストがありません",
        "vc_err_text_load_fail": "エラー: テキスト読み込み失敗 ({})",
        "vc_err_upload_path": "アップロードされたファイルのパスを解決できませんでした",
        "vc_ok_done": "完了!",
        "vc_result_files": "ファイル数: {}\n総音声時間: {}\n出力先: {}\nテキストリスト: {}",
        "vc_err_file_select": "ファイル選択",
        "vc_err_file_load": "エラー: {}",
        "vc_stopped": "停止しました",
        "vc_clone_fail": "エラー: {}",
        # ── Tools tab ──
        "tools_resample_section": "### リサンプル",
        "tools_resample_desc": "outputフォルダの raw/ 内WAVを一括リサンプルして resampled/ に出力します。",
        "tools_resample_folder_label": "フォルダ選択",
        "tools_resample_sr_label": "出力サンプルレート (Hz)",
        "tools_btn_resample": "リサンプル実行",
        "tools_resample_status_label": "ステータス",
        "tools_btn_resample_refresh": "更新",
        "tools_esd_section": "### esd.list 生成",
        "tools_esd_desc": "outputフォルダを選択して raw/*.wav とテキストリストから esd.list を生成します。",
        "tools_esd_folder_label": "フォルダ選択",
        "tools_esd_speaker_label": "話者名（esd.listのspeaker列）",
        "tools_esd_lang_label": "言語コード（esd.listのlang列）",
        "tools_btn_esd": "esd.list 生成",
        "tools_esd_status_label": "ステータス",
        "tools_btn_esd_refresh": "更新",
        "tools_audio_info_section": "### 音声情報",
        "tools_audio_info_desc": "WAVファイルをアップロードして秒数・サンプルレートを確認します。",
        "tools_audio_files_label": "WAVファイル（複数可）",
        "tools_audio_info_label": "ファイル情報",
        # tools messages
        "tools_err_no_folder": "エラー: フォルダを選択してください",
        "tools_err_raw_not_found": "エラー: {} が見つかりません",
        "tools_err_no_wavs": "エラー: raw/ にWAVファイルがありません",
        "tools_err_folder_not_exist": "エラー: {} が存在しません",
        "tools_err_no_text": "エラー: テキストが見つかりません。Neutral.txt等が必要です",
        "tools_resample_done": "完了: {}ファイルをリサンプル ({:.1f}秒)\n出力先: {}",
        "tools_esd_done": "完了: {}行の esd.list を生成\n保存先: {}",
        "tools_esd_skip": "\n⚠ テキスト未対応のためスキップ ({}件): {}",
        "tools_audio_files": "ファイル数: {} / 合計: {:.1f}秒 ({:.1f}分)",
        "tools_audio_all_match": "\n全ファイル一致: {}Hz / {} / {}",
        "tools_audio_sr_mismatch": "\n⚠ サンプルレート不一致: {}",
        "tools_audio_ch_mismatch": "\n⚠ チャンネル数不一致: {}",
        "tools_audio_bit_mismatch": "\n⚠ ビット深度不一致: {}",
        "tools_audio_mono": "モノラル",
        "tools_audio_multi_ch": "{}ch",
        "tools_audio_unreadable": "  {}: 読み取れません",
        # ── Settings tab ──
        "settings_lang_section": "### 表示言語",
        "settings_lang_label": "言語 / Language / 语言 / 언어",
        "settings_lang_note": "変更後はアプリを再起動してください。",
        "settings_lang_saved": "言語を {} に設定しました。再起動すると反映されます。",
        "settings_lang_save_fail": "エラー: {}",
        "settings_backend_section": "### 推論バックエンド",
        "settings_backend_desc": "**faster**: Qwen3-TTS の CUDA Graph 高速化（6-10倍速、GPU専用）\n\n**Qwen3-TTS**: 標準推論（CPU/GPU両対応）\n\n**Irodori-TTS**: 日本語特化の48kHz拡散モデル（GPU必須）",
        "settings_backend_label": "バックエンド",
        "settings_backend_status_label": "ステータス",
        "settings_backend_current": "現在: {}",
        "settings_backend_no_faster": "（faster未インストール）",
        "settings_backend_err": "エラー: {}",
        "settings_backend_restart": "バックエンドを切り替えました。再起動中...",
        "settings_sysinfo_section": "### システム情報",
        "settings_gpu_label": "GPU",
        "settings_vram_label": "VRAM",
        "settings_faster_label": "faster-qwen3-tts",
        "settings_faster_installed": "インストール済み",
        "settings_faster_not_installed": "未インストール（pip install faster-qwen3-tts）",
        "settings_irodori_installed": "インストール済み",
        "settings_irodori_not_installed": "未インストール（setup.bat を再実行してください）",
        "settings_btn_refresh": "更新",
        # ── Voice Clone: LoRA + auto-train ──
        "vc_lora_label": "LoRA アダプタ",
        "vc_btn_lora_refresh": "更新",
        "vc_autotrain_section": "### LoRA 自動学習",
        "vc_autotrain_label": "クローン完了後にLoRA学習を実行",
        "vc_autotrain_done": "LoRA学習完了!",
        # ── LoRA tab ──
        "lora_source_section": "### 1. 学習データ（クローン出力）",
        "lora_source_label": "出力フォルダ",
        "lora_settings_section": "### 2. 学習設定",
        "lora_speaker_label": "話者名（LoRA識別子）",
        "lora_steps_label": "学習ステップ数",
        "lora_advanced_section": "詳細設定",
        "lora_steps_override_label": "ステップ数（プリセット上書き）",
        "lora_batch_label": "バッチサイズ",
        "lora_workers_label": "DataLoader workers",
        "lora_lr_label": "学習率",
        "lora_existing_section": "### 既存のLoRA",
        "lora_existing_label": "保存済みLoRA一覧",
        "lora_existing_none": "（まだありません）",
        "lora_progress_section": "### 3. 進捗",
        "lora_status_label": "ステータス",
        "lora_log_label": "ログ",
        "lora_btn_refresh": "更新",
        "lora_btn_start": "学習開始",
        "lora_btn_stop": "■ 停止",
        "lora_irodori_only_note": "_LoRA学習はバックエンドが Irodori-TTS のときのみ利用できます。_",
        "lora_err_not_irodori": "エラー: バックエンドを Irodori-TTS に切り替えてください",
        "lora_err_no_source": "エラー: 学習データ（クローン出力フォルダ）を選択してください",
        "lora_err_no_speaker": "エラー: 話者名を入力してください",
        "lora_err_failed": "エラー: {}",
        "lora_ok_done": "完了: speaker={} 出力先={}",
        # ── Irodori Inference tab ──
        "ii_ref_section": "### 1. 参照音声",
        "ii_model_section": "### 2. LoRA",
        "ii_text_section": "### 3. テキスト",
        "ii_params_section": "### 4. パラメータ",
        "ii_preview_section": "### 5. プレビュー",
        "ii_save_section": "### 6. 保存",
        "ii_caption_label": "キャプション（任意）",
        "ii_caption_placeholder": "例: 落ち着いた女性の声で",
        "ii_text_label": "読み上げテキスト（絵文字スタイル制御可）",
        "ii_text_placeholder": "例: こんにちは。😆 はじめまして！",
        "ii_seed_label": "シード（空でランダム）",
        "ii_btn_seed_random": "ランダム",
        "ii_irodori_only_note": "_Irodori推論はバックエンドが Irodori-TTS のときのみ利用できます。_",
        "ii_err_not_irodori": "エラー: バックエンドを Irodori-TTS に切り替えてください",
        "ii_err_no_ref": "エラー: 参照音声を選択してください",
        "ii_err_ref_not_found": "エラー: 参照音声が見つかりません",
        "ii_err_no_text": "エラー: テキストを入力してください",
        # ── Manual tab ──
        "manual_intro": (
            "## VoiceDesignCloner とは\n\n"
            "**録音不要**でオリジナルの声をテキストプロンプトから作成し、"
            "コーパスを用いてその声で大量の音声を自動生成する一貫したGUIツールです。\n"
            "出力は Style-Bert-VITS2（SBV2）などのTTSモデル学習にそのまま使える教師データ形式になっています。\n\n"
            "音声合成の学習で地味に面倒な**コーパスの用意・音声の量産・リサンプル**などが、これ一つで完結します。"
        ),
        "manual_voice_design": (
            "### ボイスデザイン タブ — 声を作る\n\n"
            "1. **ボイスプロンプト** に作りたい声の特徴を書く\n"
            "   - 日本語・英語・中国語で入力できます\n"
            "   - 翻訳ボタンで日本語／中国語／英語に相互変換できます\n"
            "   - 「プリセットから選ぶ」に日本語・中国語・英語のサンプルがあります\n"
            "2. **生成パラメータ** はデフォルトのままでもOK、好みに合わせて調整も可能\n"
            "3. **読み上げテキスト** にプレビュー用の文章を入力\n"
            "   - **音声生成言語** で読み上げる言語を選択（10言語対応）\n"
            "   - デフォルトは設定タブで選択中のUI言語\n"
            "4. **生成** → プレビュー再生 → 気に入らなければ **再生成**\n"
            "5. 気に入ったら **保存名** を付けて **保存**\n"
            "   - `output/voice_design/` に `{保存名}.wav` と `{保存名}.txt` がセットで保存されます\n"
            "   - 同名が存在する場合は `_1`, `_2`... が自動付与されます\n"
            "   - ボイスクローン の「ショートカット」は保存済み音声を対象にします"
        ),
        "manual_voice_clone": (
            "### ボイスクローン タブ — 声を量産する\n\n"
            "1. **参照音声** を選ぶ\n"
            "   - ショートカット: ボイスデザインで保存した声を番号で選択（書き起こしは自動入力）\n"
            "   - アップロード: 自前の音声を使う場合（その声の書き起こしを手動入力）\n"
            "2. **コーパス言語** を選ぶ（JA / EN / ZH）\n"
            "   - 選択した言語のコーパスフォルダに切り替わります\n"
            "   - 梱包コーパス（JA/EN/ZH）を使う場合はこちらで言語が自動連動します\n"
            "3. **コーパスファイル** を選ぶ\n"
            "   - ita_emotion100（100文）、ita_recitation324（324文）、mana652（652文）、rohan4600（4600文）\n"
            "   - アップロード: 自作の1行1文の .txt ファイルも使えます\n"
            "   - 「使用する文数」で先頭N文だけ生成可（0=すべて）\n"
            "4. **モデル**・**音声生成言語**・**サンプルレート** を選択\n"
            "   - **音声生成言語** はテキストの言語を10言語から指定（梱包コーパス使用時は自動連動）\n"
            "   - 自前コーパスを持ち込む場合は必ずこちらで言語を指定してください\n"
            "   - デフォルトは設定タブで選択中のUI言語\n"
            "   - SBV2 で使うことを想定してサンプルレートのデフォルトは 44100Hz\n"
            "5. **出力先** のフォルダ名を設定\n"
            "6. **一括生成開始**\n\n"
            "> **■ 停止** ボタンで途中停止できます。"
        ),
        "manual_tools": (
            "### Tools タブ — 後処理\n\n"
            "- **リサンプル**: フォルダの `raw/` 内WAVを一括変換 → `resampled/` に出力\n"
            "- **esd.list 生成**: `raw/` のWAVと `Neutral.txt` から SBV2用リストを作成（言語コード選択可）\n"
            "- **音声情報**: WAVファイルの秒数・サンプルレートを確認"
        ),
        "manual_sbv2": (
            "### SBV2 への受け渡し\n\n"
            "1. `output/{フォルダ名}/raw/` → SBV2 の `Data/{モデル名}/raw/` にコピー\n"
            "2. Tools タブで esd.list を生成 → `Data/{モデル名}/esd.list` として配置\n"
            "3. SBV2 の WebUI で前処理 → 学習を実行"
        ),
        "manual_vram": (
            "### VRAM 目安\n\n"
            "| モデル | VRAM (bf16) |\n"
            "|---|---|\n"
            "| 1.7B-VoiceDesign | ~7-8 GB |\n"
            "| 1.7B-Base | ~7-8 GB |\n"
            "| 0.6B-Base | ~3-4 GB |"
        ),
        "manual_settings": (
            "### 設定 タブ\n\n"
            "**バックエンド選択**\n\n"
            "| バックエンド | エンジン | 速度 | 対応言語 | 備考 |\n"
            "|---|---|---|---|---|\n"
            "| **faster** | Qwen3-TTS | 約6-10倍速 | 10言語 | GPU必須・0.6B-Base非対応 |\n"
            "| **Qwen3-TTS** | Qwen3-TTS | 標準速度 | 10言語 | CPU/GPU両対応 |\n"
            "| **Irodori-TTS** | Irodori-TTS | 6-7秒/文 | 日本語のみ | GPU必須・48kHz拡散モデル |\n\n"
            "バックエンドを切り替えるとアプリが自動再起動し、各タブのUIが対応する状態になります。\n\n"
            "**GPU 情報**\n\n"
            "現在使用中の GPU 名と VRAM 使用量をリアルタイムで確認できます。\n\n"
            "**表示言語**\n\n"
            "UI の表示言語を日本語 / 英語 / 中国語 / 韓国語から選択できます。\n"
            "「Apply & Restart」ボタンを押すとアプリが再起動し、選択した言語で表示されます。"
        ),
        "manual_irodori": (
            "### Irodori-TTS について\n\n"
            "[Irodori-TTS](https://github.com/Aratako/Irodori-TTS) は日本語特化の48kHz拡散ベースTTSモデルです。\n\n"
            "**特徴**\n\n"
            "- **48kHz・日本語特化**: Qwen3-TTSより高サンプルレートで日本語の自然さを重視\n"
            "- **キャプション制御**: ボイスデザインでは「落ち着いた女性の声で」のような自然言語で声質を指示\n"
            "- **ゼロショットクローン**: ボイスクローンでは参照音声1つから声色を再現（書き起こし不要）\n\n"
            "**使い方**\n\n"
            "1. 設定タブで **Irodori-TTS** を選択（自動再起動）\n"
            "2. ボイスデザイン / ボイスクローンタブで通常通り使用\n"
            "   - 日本語以外の言語、生成パラメータ、参照音声書き起こし等はロックされます\n"
            "   - 内部的にデザインは `v2-VoiceDesign`、クローンは `v3` を使用\n\n"
            "**初回起動時の注意**\n\n"
            "- 初めて生成する時、Hugging Face からモデルを自動DLします（数百MB、5-10分程度）\n"
            "- 以降はキャッシュから即起動\n\n"
            "**インストール**\n\n"
            "`setup.bat` / `setup.sh` 実行時に GPU が検出されると自動でインストールされます。\n"
            "インストール先は `%USERPROFILE%\\.vdc-engines\\Irodori-TTS\\`（Linux: `~/.vdc-engines/`）。"
        ),
        "manual_lora": (
            "### LoRA学習 タブ — 声を学習させる\n\n"
            "ボイスクローン で生成した音声を使って Irodori-TTS の LoRA を学習します。\n"
            "学習はvdc本体のバックエンドが何でも実行可能ですが、できあがったLoRAを使うには Irodori-TTS バックエンドが必要です。\n\n"
            "1. **学習データ** にボイスクローンの出力フォルダを選択（`output/{フォルダ名}/raw/`）\n"
            "2. **話者名** を入力（LoRAの識別子、後でクローンタブやIrodori推論タブでこの名前で選択可能）\n"
            "3. **学習ステップ数** を選ぶ:\n"
            "   - `quick (3000)`: お試し用、約20分（RTX 4060 Ti 目安）\n"
            "   - `normal (10000)`: 標準\n"
            "   - `full (30000)`: 本格学習\n"
            "4. **詳細設定**（任意）: バッチサイズ、DataLoader workers、学習率を個別調整\n"
            "5. **学習開始** → 自動的に `lab形式変換 → jsonl → 潜在エンコード → train.py --lora` の順に実行\n\n"
            "**シームレス学習**: ボイスクローンタブで「クローン完了後にLoRA学習を実行」をONにすると、"
            "クローン生成完了から学習までを一気通貫で実行できます。\n\n"
            "**保存先**: `output/lora/{話者名}/` 配下に PEFT 形式のアダプタが保存されます。\n\n"
            "**注意**: LoRAは「ベースモデル + 参照音声」の上に重ねる適応層なので、"
            "推論時にも参照音声が必要です（Irodori推論タブではLoRA選択時に学習データから自動で1つピックされます）。"
        ),
        "manual_irodori_infer": (
            "### Irodori推論 タブ — 学習済LoRAを試す\n\n"
            "学習済LoRAを使って1文ずつ生成・確認・保存する対話的なプレイグラウンドです。\n"
            "ボイスクローンタブ（一括生成）の前に、まずはここでLoRAの仕上がりを確認するのに便利。\n\n"
            "1. **参照音声** を選択（ショートカット or アップロード）\n"
            "   - LoRA選択時は学習データから自動で参照が設定されます（変更可）\n"
            "2. **LoRA** を選択（学習済 or 「—」でLoRAなし＝ベースモデルのみ）\n"
            "3. **テキスト** を入力（絵文字でスタイル制御可: 😆😢😱⏩🐢 等）\n"
            "4. **シード** 任意（空ならランダム、固定すると再現可能）\n"
            "5. **生成** → プレビュー → 気に入ったら **保存名** を付けて保存\n\n"
            "保存先: `output/irodori_infer/{保存名}.wav`"
        ),
    },
    "en": {
        # ── App ──
        "app_title": "VoiceDesignCloner",
        # ── Tab names ──
        "tab_voice_design": "Voice Design",
        "tab_voice_clone": "Voice Clone",
        "tab_lora": "LoRA",
        "tab_irodori_infer": "Irodori Infer",
        "tab_tools": "Tools",
        "tab_settings": "Settings",
        "tab_manual": "Manual",
        # ── Voice Design tab ──
        "vd_prompt_section": "### 1. Voice Prompt",
        "vd_prompt_desc": "Describe the voice you want to generate (any language)",
        "vd_prompt_label": "LLM Prompt",
        "vd_prompt_placeholder": "e.g. A calm adult female voice with a low tone",
        "vd_btn_translate_ja": "Translate to Japanese",
        "vd_btn_translate_zh": "Translate to Chinese",
        "vd_btn_translate_en": "Translate to English",
        "vd_preset_accordion": "Choose from Presets",
        "vd_preset_ja_label": "Japanese",
        "vd_preset_zh_label": "Chinese",
        "vd_preset_en_label": "English",
        "vd_btn_clear_preset": "Clear",
        "vd_params_section": "### 2. Generation Parameters",
        "vd_temperature_label": "Temperature (high=expressive / low=stable)",
        "vd_top_p_label": "Top-P (lower=more stable quality)",
        "vd_top_k_label": "Top-K (candidate token count)",
        "vd_rep_penalty_label": "Repetition Penalty",
        "vd_btn_reset_params": "Reset to Defaults",
        "vd_sample_section": "### 3. Sample Text",
        "vd_sample_desc": "Text to be spoken in this voice",
        "vd_sample_label": "Sample Text",
        "vd_tts_lang_label": "Generation Language",
        "vd_preview_section": "### 4. Preview",
        "vd_preview_label": "Preview",
        "vd_status_label": "Status",
        "vd_btn_generate": "Generate",
        "vd_btn_reroll": "Re-roll",
        "vd_save_section": "### 5. Save",
        "vd_save_name_label": "Save Name",
        "vd_btn_save": "Save",
        # vd messages
        "vd_err_empty_prompt": "Voice prompt is empty",
        "vd_err_translate_empty": "Please enter text",
        "vd_err_translate_fail": "Translation error: {}",
        "vd_err_generate_fail": "Error: {}",
        "vd_ok_generated": "Generated ({}Hz)",
        "vd_err_no_audio": "No audio to save",
        "vd_ok_saved": "Saved: {}",
        "vd_err_save_fail": "Error: {}",
        # ── Voice Clone tab ──
        "vc_ref_section": "### 1. Reference Voice",
        "vc_ref_tab_shortcut": "Shortcut",
        "vc_ref_tab_upload": "Upload",
        "vc_shortcut_label": "voice_design number",
        "vc_upload_audio_label": "Audio File",
        "vc_ref_text_label": "Reference voice transcript",
        "vc_ref_text_placeholder": "Auto-filled for shortcut",
        "vc_btn_refresh_ref": "Refresh List",
        "vc_corpus_section": "### 2. Corpus",
        "vc_corpus_tab_file": "Select File",
        "vc_corpus_tab_upload": "Upload",
        "vc_corpus_file_label": "Corpus File",
        "vc_corpus_lang_label": "Corpus Language",
        "vc_corpus_upload_label": "Text file (one sentence per line .txt)",
        "vc_corpus_count_label": "Sentences to use (0=all)",
        "vc_corpus_total_lines_label": "Total sentences",
        "vc_corpus_total_chars_label": "Total characters",
        "vc_btn_corpus_refresh": "Refresh corpus info",
        "vc_settings_section": "### 3. Settings",
        "vc_model_label": "Model",
        "vc_lang_label": "Language",
        "vc_sr_label": "Output Sample Rate (Hz)",
        "vc_output_section": "### Output (output/)",
        "vc_output_folder_label": "Folder Name",
        "vc_wavs_folder_label": "Audio Subfolder Name",
        "vc_esd_filename_label": "Text List Name (auto .txt)",
        "vc_btn_start": "Start Batch Generation",
        "vc_btn_stop": "■ Stop",
        "vc_progress_section": "### 4. Progress",
        "vc_progress_label": "Status",
        "vc_result_label": "Result",
        # vc messages
        "vc_err_no_ref": "Error: No reference audio",
        "vc_err_ref_not_found": "Error: Reference audio not found",
        "vc_err_empty_ref_text": "Error: Transcript is empty",
        "vc_err_no_text": "Error: No text available",
        "vc_err_text_load_fail": "Error: Failed to load text ({})",
        "vc_err_upload_path": "Could not resolve uploaded file path",
        "vc_ok_done": "Done!",
        "vc_result_files": "Files: {}\nTotal duration: {}\nOutput: {}\nText list: {}",
        "vc_err_file_select": "Select File",
        "vc_err_file_load": "Error: {}",
        "vc_stopped": "Stopped",
        "vc_clone_fail": "Error: {}",
        # ── Tools tab ──
        "tools_resample_section": "### Resample",
        "tools_resample_desc": "Batch resample WAVs in raw/ to resampled/.",
        "tools_resample_folder_label": "Select Folder",
        "tools_resample_sr_label": "Output Sample Rate (Hz)",
        "tools_btn_resample": "Run Resample",
        "tools_resample_status_label": "Status",
        "tools_btn_resample_refresh": "Refresh",
        "tools_esd_section": "### Generate esd.list",
        "tools_esd_desc": "Generate esd.list from raw/*.wav and text list.",
        "tools_esd_folder_label": "Select Folder",
        "tools_esd_speaker_label": "Speaker name (speaker column)",
        "tools_esd_lang_label": "Language code (lang column)",
        "tools_btn_esd": "Generate esd.list",
        "tools_esd_status_label": "Status",
        "tools_btn_esd_refresh": "Refresh",
        "tools_audio_info_section": "### Audio Info",
        "tools_audio_info_desc": "Upload WAV files to check duration and sample rate.",
        "tools_audio_files_label": "WAV files (multiple)",
        "tools_audio_info_label": "File Info",
        # tools messages
        "tools_err_no_folder": "Error: Please select a folder",
        "tools_err_raw_not_found": "Error: {} not found",
        "tools_err_no_wavs": "Error: No WAV files in raw/",
        "tools_err_folder_not_exist": "Error: {} does not exist",
        "tools_err_no_text": "Error: No text found. Neutral.txt is required",
        "tools_resample_done": "Done: {} files resampled ({:.1f}s)\nOutput: {}",
        "tools_esd_done": "Done: {} lines written to esd.list\nSaved: {}",
        "tools_esd_skip": "\n⚠ Skipped (no text, {} files): {}",
        "tools_audio_files": "Files: {} / Total: {:.1f}s ({:.1f}min)",
        "tools_audio_all_match": "\nAll match: {}Hz / {} / {}",
        "tools_audio_sr_mismatch": "\n⚠ Sample rate mismatch: {}",
        "tools_audio_ch_mismatch": "\n⚠ Channel count mismatch: {}",
        "tools_audio_bit_mismatch": "\n⚠ Bit depth mismatch: {}",
        "tools_audio_mono": "Mono",
        "tools_audio_multi_ch": "{}ch",
        "tools_audio_unreadable": "  {}: unreadable",
        # ── Settings tab ──
        "settings_lang_section": "### Display Language",
        "settings_lang_label": "言語 / Language / 语言 / 언어",
        "settings_lang_note": "Restart the app to apply changes.",
        "settings_lang_saved": "Language set to {}. Restart to apply.",
        "settings_lang_save_fail": "Error: {}",
        "settings_backend_section": "### Inference Backend",
        "settings_backend_desc": "**faster**: Qwen3-TTS with CUDA Graph (6-10x, GPU only)\n\n**Qwen3-TTS**: Standard inference (CPU/GPU)\n\n**Irodori-TTS**: Japanese-only 48kHz diffusion model (GPU required)",
        "settings_backend_label": "Backend",
        "settings_backend_status_label": "Status",
        "settings_backend_current": "Current: {}",
        "settings_backend_no_faster": " (faster not installed)",
        "settings_backend_err": "Error: {}",
        "settings_backend_restart": "Backend switched. Restarting...",
        "settings_sysinfo_section": "### System Info",
        "settings_gpu_label": "GPU",
        "settings_vram_label": "VRAM",
        "settings_faster_label": "faster-qwen3-tts",
        "settings_faster_installed": "Installed",
        "settings_faster_not_installed": "Not installed (pip install faster-qwen3-tts)",
        "settings_irodori_installed": "Installed",
        "settings_irodori_not_installed": "Not installed (re-run setup.bat)",
        "settings_btn_refresh": "Refresh",
        # ── Voice Clone: LoRA + auto-train ──
        "vc_lora_label": "LoRA adapter",
        "vc_btn_lora_refresh": "Refresh",
        "vc_autotrain_section": "### LoRA auto-train",
        "vc_autotrain_label": "Train a LoRA after the clone finishes",
        "vc_autotrain_done": "LoRA training complete!",
        # ── LoRA tab ──
        "lora_source_section": "### 1. Training data (clone output)",
        "lora_source_label": "Output folder",
        "lora_settings_section": "### 2. Training settings",
        "lora_speaker_label": "Speaker name (LoRA id)",
        "lora_steps_label": "Training steps",
        "lora_advanced_section": "Advanced",
        "lora_steps_override_label": "Steps (override preset)",
        "lora_batch_label": "Batch size",
        "lora_workers_label": "DataLoader workers",
        "lora_lr_label": "Learning rate",
        "lora_existing_section": "### Existing LoRAs",
        "lora_existing_label": "Saved LoRAs",
        "lora_existing_none": "(none yet)",
        "lora_progress_section": "### 3. Progress",
        "lora_status_label": "Status",
        "lora_log_label": "Log",
        "lora_btn_refresh": "Refresh",
        "lora_btn_start": "Start training",
        "lora_btn_stop": "■ Stop",
        "lora_irodori_only_note": "_LoRA training is only available when the Irodori-TTS backend is selected._",
        "lora_err_not_irodori": "Error: switch backend to Irodori-TTS first",
        "lora_err_no_source": "Error: select a clone output folder",
        "lora_err_no_speaker": "Error: enter a speaker name",
        "lora_err_failed": "Error: {}",
        "lora_ok_done": "Done: speaker={} output={}",
        # ── Irodori Inference tab ──
        "ii_ref_section": "### 1. Reference voice",
        "ii_model_section": "### 2. LoRA",
        "ii_text_section": "### 3. Text",
        "ii_params_section": "### 4. Parameters",
        "ii_preview_section": "### 5. Preview",
        "ii_save_section": "### 6. Save",
        "ii_caption_label": "Caption (optional)",
        "ii_caption_placeholder": "e.g. A calm female voice",
        "ii_text_label": "Text to speak (emoji style control supported)",
        "ii_text_placeholder": "e.g. Hello. 😆 Nice to meet you!",
        "ii_seed_label": "Seed (empty = random)",
        "ii_btn_seed_random": "Random",
        "ii_irodori_only_note": "_Irodori Inference is only available when the Irodori-TTS backend is selected._",
        "ii_err_not_irodori": "Error: switch backend to Irodori-TTS first",
        "ii_err_no_ref": "Error: select a reference voice",
        "ii_err_ref_not_found": "Error: reference voice not found",
        "ii_err_no_text": "Error: enter some text",
        # ── Manual tab ──
        "manual_intro": (
            "## What is VoiceDesignCloner?\n\n"
            "A GUI tool that creates original voices from text prompts **without any recording**, "
            "and uses a corpus to auto-generate large amounts of audio in that voice.\n"
            "Output is in a training data format compatible with Style-Bert-VITS2 (SBV2) and other TTS engines.\n\n"
            "Everything from corpus preparation, audio generation, and resampling is handled in one place."
        ),
        "manual_voice_design": (
            "### Voice Design Tab — Create a Voice\n\n"
            "1. Enter voice characteristics in **Voice Prompt**\n"
            "   - Japanese, English, and Chinese are all supported\n"
            "   - Use translation buttons to convert between Japanese / Chinese / English\n"
            "   - Presets are available in Japanese, Chinese, and English\n"
            "2. **Generation Parameters** can be left at defaults\n"
            "3. Enter preview text in **Sample Text**\n"
            "   - **Generation Language**: select the language to speak (10 languages supported)\n"
            "   - Defaults to the UI language selected in Settings\n"
            "4. **Generate** → Preview → **Re-roll** if unsatisfied\n"
            "5. Enter a **Save Name** and click **Save**\n"
            "   - Saved as `{name}.wav` + `{name}.txt` under `output/voice_design/`\n"
            "   - Auto-appends `_1`, `_2`... if name already exists\n"
            "   - Saved voices appear as shortcuts in the Voice Clone tab"
        ),
        "manual_voice_clone": (
            "### Voice Clone Tab — Mass-Produce Audio\n\n"
            "1. Choose a **Reference Voice**\n"
            "   - Shortcut: select by number from saved Voice Design voices (transcript auto-filled)\n"
            "   - Upload: use your own audio (enter transcript manually)\n"
            "2. Select **Corpus Language** (JA / EN / ZH)\n"
            "   - Switches the corpus folder for the bundled corpus\n"
            "   - Language is auto-linked when using bundled corpora (JA/EN/ZH)\n"
            "3. Choose a **Corpus File**\n"
            "   - ita_emotion100 (100), ita_recitation324 (324), mana652 (652), rohan4600 (4600)\n"
            "   - Upload: use a custom one-sentence-per-line .txt file\n"
            "   - Set sentences to use (0 = all)\n"
            "4. Choose **Model**, **Generation Language**, and **Sample Rate**\n"
            "   - **Generation Language**: specify the language of the text (10 languages supported)\n"
            "   - Required when bringing your own corpus — set this to match your text\n"
            "   - Defaults to the UI language selected in Settings\n"
            "5. Set **Output Folder** name\n"
            "6. Click **Start Batch Generation**\n\n"
            "> Use **■ Stop** to halt mid-generation."
        ),
        "manual_tools": (
            "### Tools Tab — Post-Processing\n\n"
            "- **Resample**: Batch convert WAVs in `raw/` → `resampled/`\n"
            "- **Generate esd.list**: Create SBV2 training list from `raw/` + `Neutral.txt` (language selectable)\n"
            "- **Audio Info**: Check duration and sample rate of WAV files"
        ),
        "manual_sbv2": (
            "### Passing to Style-Bert-VITS2\n\n"
            "1. Copy `output/{folder}/raw/` → `Data/{model}/raw/` in SBV2\n"
            "2. Generate esd.list in Tools tab → place as `Data/{model}/esd.list`\n"
            "3. Run preprocessing → training in SBV2 WebUI"
        ),
        "manual_vram": (
            "### VRAM Reference\n\n"
            "| Model | VRAM (bf16) |\n"
            "|---|---|\n"
            "| 1.7B-VoiceDesign | ~7-8 GB |\n"
            "| 1.7B-Base | ~7-8 GB |\n"
            "| 0.6B-Base | ~3-4 GB |"
        ),
        "manual_backend": "",
        "manual_settings": (
            "### Settings Tab\n\n"
            "**Backend**\n\n"
            "| Backend | Engine | Speed | Languages | Notes |\n"
            "|---|---|---|---|---|\n"
            "| **faster** | Qwen3-TTS | ~6-10x | 10 langs | GPU required, 0.6B-Base unsupported |\n"
            "| **Qwen3-TTS** | Qwen3-TTS | Normal | 10 langs | CPU/GPU |\n"
            "| **Irodori-TTS** | Irodori-TTS | ~6-7s/sentence | Japanese only | GPU required, 48kHz diffusion |\n\n"
            "Switching backends auto-restarts the app so each tab renders with the appropriate lock state.\n\n"
            "**GPU Info**\n\n"
            "Displays the current GPU name and real-time VRAM usage.\n\n"
            "**Display Language**\n\n"
            "Switch the UI language between Japanese, English, Chinese, and Korean.\n"
            "Click \"Apply & Restart\" to relaunch the app in the selected language."
        ),
        "manual_irodori": (
            "### About Irodori-TTS\n\n"
            "[Irodori-TTS](https://github.com/Aratako/Irodori-TTS) is a Japanese-specialized 48kHz diffusion TTS model.\n\n"
            "**Features**\n\n"
            "- **48kHz / Japanese-specialized**: higher sample rate than Qwen3-TTS, focused on natural Japanese\n"
            "- **Caption control**: in Voice Design, describe the voice in natural language (e.g. \"a calm female voice\")\n"
            "- **Zero-shot clone**: in Voice Clone, mimics a voice from one reference audio (no transcript needed)\n\n"
            "**Usage**\n\n"
            "1. Select **Irodori-TTS** in the Settings tab (auto-restarts)\n"
            "2. Use the Voice Design / Voice Clone tabs as usual\n"
            "   - Non-Japanese languages, sampling parameters, and reference transcript are locked\n"
            "   - Internally Design uses `v2-VoiceDesign`, Clone uses `v3`\n\n"
            "**First-run note**\n\n"
            "- The first generation downloads checkpoints from Hugging Face (~ a few hundred MB, ~5-10 min)\n"
            "- Subsequent runs load from cache instantly\n\n"
            "**Installation**\n\n"
            "`setup.bat` / `setup.sh` installs Irodori-TTS automatically when a GPU is detected.\n"
            "It is placed under `%USERPROFILE%\\.vdc-engines\\Irodori-TTS\\` (Linux: `~/.vdc-engines/`)."
        ),
        "manual_lora": (
            "### LoRA Tab — Train a Voice\n\n"
            "Fine-tunes Irodori-TTS with a LoRA adapter using audio generated by the Voice Clone tab.\n"
            "Training runs regardless of the active backend, but the resulting LoRA can only be used with the Irodori-TTS backend.\n\n"
            "1. Pick a **clone output folder** (`output/{folder}/raw/`)\n"
            "2. Enter a **speaker name** (used as the LoRA id; will appear in Voice Clone and Irodori Inference tabs)\n"
            "3. Choose **steps**:\n"
            "   - `quick (3000)` — try-out, ~20 min on an RTX 4060 Ti\n"
            "   - `normal (10000)` — standard\n"
            "   - `full (30000)` — full training\n"
            "4. **Advanced** (optional): override batch size, DataLoader workers, learning rate\n"
            "5. **Start** → runs `lab convert → jsonl → encode latents → train.py --lora` end-to-end\n\n"
            "**Seamless training**: enabling \"train a LoRA after clone\" on the Voice Clone tab "
            "chains clone generation directly into LoRA training.\n\n"
            "**Output**: PEFT adapter under `output/lora/{speaker}/`.\n\n"
            "**Note**: a LoRA layers on top of base model + reference audio, so inference still needs a reference. "
            "The Irodori Inference tab auto-picks one from the training data when you select a LoRA."
        ),
        "manual_irodori_infer": (
            "### Irodori Inference Tab — Try out a LoRA\n\n"
            "Interactive playground for testing a trained LoRA one line at a time. "
            "Useful for previewing a LoRA before running a full corpus batch in the Voice Clone tab.\n\n"
            "1. Pick a **reference voice** (shortcut or upload)\n"
            "   - Selecting a LoRA auto-fills a sample from its training data (can be replaced)\n"
            "2. Pick a **LoRA** (trained adapter or \"—\" for base-only)\n"
            "3. Enter **text** (emoji style control supported: 😆😢😱⏩🐢 etc.)\n"
            "4. **Seed** is optional — empty for random, fixed for reproducibility\n"
            "5. **Generate** → preview → name and save\n\n"
            "Output: `output/irodori_infer/{name}.wav`"
        ),
    },
    "zh": {
        # ── App ──
        "app_title": "VoiceDesignCloner",
        # ── Tab names ──
        "tab_voice_design": "声音设计",
        "tab_voice_clone": "声音克隆",
        "tab_lora": "LoRA训练",
        "tab_irodori_infer": "Irodori 推理",
        "tab_tools": "工具",
        "tab_settings": "设置",
        "tab_manual": "手册",
        # ── Voice Design tab ──
        "vd_prompt_section": "### 1. 声音提示词",
        "vd_prompt_desc": "描述您想生成的声音特征（任何语言均可）",
        "vd_prompt_label": "LLM提示词",
        "vd_prompt_placeholder": "例: 平静成熟的女声，低沉的音调",
        "vd_btn_translate_ja": "翻译为日文",
        "vd_btn_translate_zh": "翻译为中文",
        "vd_btn_translate_en": "翻译为英文",
        "vd_preset_accordion": "从预设中选择",
        "vd_preset_ja_label": "日文",
        "vd_preset_zh_label": "中文",
        "vd_preset_en_label": "英文",
        "vd_btn_clear_preset": "清除",
        "vd_params_section": "### 2. 生成参数",
        "vd_temperature_label": "Temperature（高=表现力强 / 低=稳定）",
        "vd_top_p_label": "Top-P（越低越稳定）",
        "vd_top_k_label": "Top-K（候选token数）",
        "vd_rep_penalty_label": "重复惩罚",
        "vd_btn_reset_params": "恢复默认",
        "vd_sample_section": "### 3. 示例文本",
        "vd_sample_desc": "用该声音朗读的文章",
        "vd_sample_label": "示例文本",
        "vd_tts_lang_label": "音频生成语言",
        "vd_preview_section": "### 4. 预览",
        "vd_preview_label": "预览",
        "vd_status_label": "状态",
        "vd_btn_generate": "生成",
        "vd_btn_reroll": "重新生成",
        "vd_save_section": "### 5. 保存",
        "vd_save_name_label": "保存名称",
        "vd_btn_save": "保存",
        # vd messages
        "vd_err_empty_prompt": "声音指令为空",
        "vd_err_translate_empty": "请输入文本",
        "vd_err_translate_fail": "翻译错误: {}",
        "vd_err_generate_fail": "错误: {}",
        "vd_ok_generated": "生成完成 ({}Hz)",
        "vd_err_no_audio": "没有可保存的音频",
        "vd_ok_saved": "保存完成: {}",
        "vd_err_save_fail": "错误: {}",
        # ── Voice Clone tab ──
        "vc_ref_section": "### 1. 参考音频",
        "vc_ref_tab_shortcut": "快捷方式",
        "vc_ref_tab_upload": "上传",
        "vc_shortcut_label": "voice_design 编号",
        "vc_upload_audio_label": "音频文件",
        "vc_ref_text_label": "参考音频转录文本",
        "vc_ref_text_placeholder": "快捷方式可自动填充",
        "vc_btn_refresh_ref": "刷新列表",
        "vc_corpus_section": "### 2. 语料库",
        "vc_corpus_tab_file": "选择文件",
        "vc_corpus_tab_upload": "上传",
        "vc_corpus_file_label": "语料库文件",
        "vc_corpus_lang_label": "语料库语言",
        "vc_corpus_upload_label": "文本文件（每行一句 .txt）",
        "vc_corpus_count_label": "使用句数（0=全部）",
        "vc_corpus_total_lines_label": "总句数",
        "vc_corpus_total_chars_label": "总字符数",
        "vc_btn_corpus_refresh": "刷新语料库信息",
        "vc_settings_section": "### 3. 设置",
        "vc_model_label": "模型",
        "vc_lang_label": "语言",
        "vc_sr_label": "输出采样率 (Hz)",
        "vc_output_section": "### 输出目录（output/）",
        "vc_output_folder_label": "文件夹名称",
        "vc_wavs_folder_label": "音频子文件夹名称",
        "vc_esd_filename_label": "文本列表名称（自动添加 .txt）",
        "vc_btn_start": "开始批量生成",
        "vc_btn_stop": "■ 停止",
        "vc_progress_section": "### 4. 进度",
        "vc_progress_label": "状态",
        "vc_result_label": "结果",
        # vc messages
        "vc_err_no_ref": "错误: 没有参考音频",
        "vc_err_ref_not_found": "错误: 找不到参考音频",
        "vc_err_empty_ref_text": "错误: 转录文本为空",
        "vc_err_no_text": "错误: 没有文本",
        "vc_err_text_load_fail": "错误: 文本加载失败 ({})",
        "vc_err_upload_path": "无法解析上传文件路径",
        "vc_ok_done": "完成!",
        "vc_result_files": "文件数: {}\n总时长: {}\n输出目录: {}\n文本列表: {}",
        "vc_err_file_select": "选择文件",
        "vc_err_file_load": "错误: {}",
        "vc_stopped": "已停止",
        "vc_clone_fail": "错误: {}",
        # ── Tools tab ──
        "tools_resample_section": "### 重采样",
        "tools_resample_desc": "将 raw/ 内的WAV文件批量重采样输出到 resampled/。",
        "tools_resample_folder_label": "选择文件夹",
        "tools_resample_sr_label": "输出采样率 (Hz)",
        "tools_btn_resample": "执行重采样",
        "tools_resample_status_label": "状态",
        "tools_btn_resample_refresh": "刷新",
        "tools_esd_section": "### 生成 esd.list",
        "tools_esd_desc": "从 raw/*.wav 和文本列表生成 esd.list。",
        "tools_esd_folder_label": "选择文件夹",
        "tools_esd_speaker_label": "说话人名称（speaker列）",
        "tools_esd_lang_label": "语言代码（lang列）",
        "tools_btn_esd": "生成 esd.list",
        "tools_esd_status_label": "状态",
        "tools_btn_esd_refresh": "刷新",
        "tools_audio_info_section": "### 音频信息",
        "tools_audio_info_desc": "上传WAV文件查看时长和采样率。",
        "tools_audio_files_label": "WAV文件（可多选）",
        "tools_audio_info_label": "文件信息",
        # tools messages
        "tools_err_no_folder": "错误: 请选择文件夹",
        "tools_err_raw_not_found": "错误: 找不到 {}",
        "tools_err_no_wavs": "错误: raw/ 中没有WAV文件",
        "tools_err_folder_not_exist": "错误: {} 不存在",
        "tools_err_no_text": "错误: 找不到文本。需要 Neutral.txt 等文件",
        "tools_resample_done": "完成: {}个文件已重采样 ({:.1f}秒)\n输出目录: {}",
        "tools_esd_done": "完成: 已生成{}行 esd.list\n保存至: {}",
        "tools_esd_skip": "\n⚠ 因缺少文本而跳过 ({}个): {}",
        "tools_audio_files": "文件数: {} / 合计: {:.1f}秒 ({:.1f}分)",
        "tools_audio_all_match": "\n全部一致: {}Hz / {} / {}",
        "tools_audio_sr_mismatch": "\n⚠ 采样率不一致: {}",
        "tools_audio_ch_mismatch": "\n⚠ 声道数不一致: {}",
        "tools_audio_bit_mismatch": "\n⚠ 位深不一致: {}",
        "tools_audio_mono": "单声道",
        "tools_audio_multi_ch": "{}声道",
        "tools_audio_unreadable": "  {}: 无法读取",
        # ── Settings tab ──
        "settings_lang_section": "### 显示语言",
        "settings_lang_label": "言語 / Language / 语言 / 언어",
        "settings_lang_note": "更改后请重启应用。",
        "settings_lang_saved": "语言已设置为 {}。重启后生效。",
        "settings_lang_save_fail": "错误: {}",
        "settings_backend_section": "### 推理后端",
        "settings_backend_desc": "**faster**: Qwen3-TTS 的 CUDA Graph 加速（6-10倍速，仅GPU）\n\n**Qwen3-TTS**: 标准推理（CPU/GPU均可）\n\n**Irodori-TTS**: 日语专用48kHz扩散模型（需GPU）",
        "settings_backend_label": "后端",
        "settings_backend_status_label": "状态",
        "settings_backend_current": "当前: {}",
        "settings_backend_no_faster": "（faster未安装）",
        "settings_backend_err": "错误: {}",
        "settings_backend_restart": "后端已切换，正在重启...",
        "settings_sysinfo_section": "### 系统信息",
        "settings_gpu_label": "GPU",
        "settings_vram_label": "显存",
        "settings_faster_label": "faster-qwen3-tts",
        "settings_faster_installed": "已安装",
        "settings_faster_not_installed": "未安装（pip install faster-qwen3-tts）",
        "settings_irodori_installed": "已安装",
        "settings_irodori_not_installed": "未安装（请重新运行 setup.bat）",
        "settings_btn_refresh": "刷新",
        # ── 克隆: LoRA + 自动训练 ──
        "vc_lora_label": "LoRA 适配器",
        "vc_btn_lora_refresh": "刷新",
        "vc_autotrain_section": "### LoRA 自动训练",
        "vc_autotrain_label": "克隆完成后自动训练 LoRA",
        "vc_autotrain_done": "LoRA 训练完成!",
        # ── LoRA 标签 ──
        "lora_source_section": "### 1. 训练数据（克隆输出）",
        "lora_source_label": "输出文件夹",
        "lora_settings_section": "### 2. 训练设置",
        "lora_speaker_label": "说话人名称（LoRA 标识）",
        "lora_steps_label": "训练步数",
        "lora_advanced_section": "高级设置",
        "lora_steps_override_label": "步数（覆盖预设）",
        "lora_batch_label": "批次大小",
        "lora_workers_label": "DataLoader workers",
        "lora_lr_label": "学习率",
        "lora_existing_section": "### 已有的 LoRA",
        "lora_existing_label": "已保存的 LoRA 列表",
        "lora_existing_none": "（暂无）",
        "lora_progress_section": "### 3. 进度",
        "lora_status_label": "状态",
        "lora_log_label": "日志",
        "lora_btn_refresh": "刷新",
        "lora_btn_start": "开始训练",
        "lora_btn_stop": "■ 停止",
        "lora_irodori_only_note": "_仅在后端为 Irodori-TTS 时可用 LoRA 训练。_",
        "lora_err_not_irodori": "错误: 请先切换到 Irodori-TTS 后端",
        "lora_err_no_source": "错误: 请选择训练数据（克隆输出文件夹）",
        "lora_err_no_speaker": "错误: 请输入说话人名称",
        "lora_err_failed": "错误: {}",
        "lora_ok_done": "完成: speaker={} 输出={}",
        # ── Irodori 推理标签 ──
        "ii_ref_section": "### 1. 参考音频",
        "ii_model_section": "### 2. LoRA",
        "ii_text_section": "### 3. 文本",
        "ii_params_section": "### 4. 参数",
        "ii_preview_section": "### 5. 预览",
        "ii_save_section": "### 6. 保存",
        "ii_caption_label": "Caption（可选）",
        "ii_caption_placeholder": "例: 平静的女声",
        "ii_text_label": "朗读文本（支持 emoji 风格控制）",
        "ii_text_placeholder": "例: 你好。😆 初次见面！",
        "ii_seed_label": "种子（留空 = 随机）",
        "ii_btn_seed_random": "随机",
        "ii_irodori_only_note": "_仅当后端为 Irodori-TTS 时可用。_",
        "ii_err_not_irodori": "错误: 请先切换到 Irodori-TTS 后端",
        "ii_err_no_ref": "错误: 请选择参考音频",
        "ii_err_ref_not_found": "错误: 找不到参考音频",
        "ii_err_no_text": "错误: 请输入文本",
        # ── Manual tab ──
        "manual_intro": (
            "## 什么是 VoiceDesignCloner？\n\n"
            "一款**无需录音**、通过文本提示词创建原创声音，并利用语料库自动批量生成音频的一体化GUI工具。\n"
            "输出格式兼容 Style-Bert-VITS2（SBV2）等TTS模型训练所需的教学数据格式。\n\n"
            "语料库准备、音频批量生成、重采样等繁琐工作，一个工具全部搞定。"
        ),
        "manual_voice_design": (
            "### 声音设计 标签 — 创建声音\n\n"
            "1. 在**声音提示词**中描述想要的声音特征\n"
            "   - 支持日语、英语、中文输入\n"
            "   - 可使用翻译按钮在日语／中文／英语之间相互转换\n"
            "   - 预设提供日语、中文、英语三种版本\n"
            "2. **生成参数**保持默认即可，也可根据喜好调整\n"
            "3. 在**示例文本**中输入预览用的文章\n"
            "   - **音频生成语言**：选择朗读所用的语言（支持10种语言）\n"
            "   - 默认为设置标签中选择的UI语言\n"
            "4. **生成** → 预览播放 → 不满意则**重新生成**\n"
            "5. 满意后填写**保存名称**并**保存**\n"
            "   - 保存在 `output/voice_design/` 下，格式为 `{名称}.wav` + `{名称}.txt`\n"
            "   - 若同名已存在，自动添加 `_1`, `_2`...\n"
            "   - 保存的声音可在声音克隆标签的快捷方式中选择"
        ),
        "manual_voice_clone": (
            "### 声音克隆 标签 — 批量生产音频\n\n"
            "1. 选择**参考音频**\n"
            "   - 快捷方式：按编号选择声音设计中保存的声音（转写自动填入）\n"
            "   - 上传：使用自有音频（需手动输入转写文本）\n"
            "2. 选择**语料库语言**（JA / EN / ZH）\n"
            "   - 切换语料库文件夹\n"
            "   - 使用内置语料库（JA/EN/ZH）时，语言会自动联动\n"
            "3. 选择**语料库文件**\n"
            "   - ita_emotion100（100句）、ita_recitation324（324句）、mana652（652句）、rohan4600（4600句）\n"
            "   - 上传：也可使用自制的每行一句 .txt 文件\n"
            "   - 可设置使用句数（0=全部）\n"
            "4. 选择**模型**、**音频生成语言**和**采样率**\n"
            "   - **音频生成语言**：指定文本所用语言（支持10种语言）\n"
            "   - 自带语料库时使用时语言自动联动；使用自有语料库时请手动指定\n"
            "   - 默认为设置标签中选择的UI语言\n"
            "5. 设置**输出文件夹**名称\n"
            "6. 点击**开始批量生成**\n\n"
            "> 可使用**■ 停止**按钮中途暂停。"
        ),
        "manual_tools": (
            "### Tools 标签 — 后处理\n\n"
            "- **重采样**: 批量转换 `raw/` 内的WAV → 输出到 `resampled/`\n"
            "- **生成 esd.list**: 从 `raw/` 和 `Neutral.txt` 创建SBV2训练列表（可选语言代码）\n"
            "- **音频信息**: 查看WAV文件的时长和采样率"
        ),
        "manual_sbv2": (
            "### 传递给 Style-Bert-VITS2\n\n"
            "1. 将 `output/{文件夹}/raw/` 复制到SBV2的 `Data/{模型名}/raw/`\n"
            "2. 在Tools标签生成 esd.list → 放置为 `Data/{模型名}/esd.list`\n"
            "3. 在SBV2 WebUI中执行前处理 → 训练"
        ),
        "manual_vram": (
            "### 显存参考\n\n"
            "| 模型 | 显存 (bf16) |\n"
            "|---|---|\n"
            "| 1.7B-VoiceDesign | ~7-8 GB |\n"
            "| 1.7B-Base | ~7-8 GB |\n"
            "| 0.6B-Base | ~3-4 GB |"
        ),
        "manual_backend": "",
        "manual_settings": (
            "### 设置 标签\n\n"
            "**推理后端**\n\n"
            "| 后端 | 引擎 | 速度 | 支持语言 | 备注 |\n"
            "|---|---|---|---|---|\n"
            "| **faster** | Qwen3-TTS | ~6-10倍速 | 10种 | 需GPU，0.6B-Base不支持 |\n"
            "| **Qwen3-TTS** | Qwen3-TTS | 标准速度 | 10种 | CPU/GPU均可 |\n"
            "| **Irodori-TTS** | Irodori-TTS | 6-7秒/句 | 仅日语 | 需GPU，48kHz扩散模型 |\n\n"
            "切换后端会自动重启应用，各标签会根据所选后端进入相应锁定状态。\n\n"
            "**GPU信息**\n\n"
            "可实时查看当前使用的GPU名称和显存占用情况。\n\n"
            "**显示语言**\n\n"
            "可在日语、英语、中文、韩语之间切换UI显示语言。\n"
            "点击「Apply & Restart」重启应用，以所选语言显示。"
        ),
        "manual_irodori": (
            "### 关于 Irodori-TTS\n\n"
            "[Irodori-TTS](https://github.com/Aratako/Irodori-TTS) 是一个日语专用的48kHz扩散TTS模型。\n\n"
            "**特点**\n\n"
            "- **48kHz・日语专用**：比 Qwen3-TTS 更高的采样率，注重日语自然度\n"
            "- **Caption 控制**：在声音设计中用自然语言描述声音（如「平静的女声」）\n"
            "- **零样本克隆**：在声音克隆中通过一段参考音频复制声色（无需转录）\n\n"
            "**用法**\n\n"
            "1. 在设置标签选择 **Irodori-TTS**（会自动重启）\n"
            "2. 在声音设计 / 声音克隆标签中照常使用\n"
            "   - 非日语、生成参数、参考音频转录等会被锁定\n"
            "   - 内部：设计使用 `v2-VoiceDesign`，克隆使用 `v3`\n\n"
            "**首次运行注意**\n\n"
            "- 首次生成时会从 Hugging Face 自动下载模型（数百 MB，约5-10分钟）\n"
            "- 之后从缓存即时加载\n\n"
            "**安装**\n\n"
            "运行 `setup.bat` / `setup.sh` 时，检测到 GPU 会自动安装 Irodori-TTS。\n"
            "安装路径：`%USERPROFILE%\\.vdc-engines\\Irodori-TTS\\`（Linux：`~/.vdc-engines/`）。"
        ),
        "manual_lora": (
            "### LoRA训练 标签 — 训练声音\n\n"
            "使用声音克隆生成的音频对 Irodori-TTS 进行 LoRA 微调。\n"
            "训练本身在任何后端下都可运行，但训练好的 LoRA 只能在 Irodori-TTS 后端使用。\n\n"
            "1. 选择**克隆输出文件夹**（`output/{文件夹}/raw/`）\n"
            "2. 输入**说话人名称**（作为 LoRA 标识符）\n"
            "3. 选择**步数**：`quick (3000)` / `normal (10000)` / `full (30000)`\n"
            "4. **高级设置**（可选）：批次大小、DataLoader workers、学习率\n"
            "5. **开始训练** → 自动执行 `lab格式转换 → jsonl → 潜在编码 → train.py --lora`\n\n"
            "**无缝训练**：在声音克隆标签开启「克隆完成后训练 LoRA」即可一气呵成。\n\n"
            "**输出**：`output/lora/{说话人}/`。\n\n"
            "**注意**：LoRA 是叠加在基础模型+参考音频上的适配层，推理时仍需要参考音频。"
        ),
        "manual_irodori_infer": (
            "### Irodori推理 标签 — 试用 LoRA\n\n"
            "用训练好的 LoRA 逐句生成、试听、保存的交互式调试环境。\n\n"
            "1. 选择**参考音频**（快捷或上传，选择 LoRA 时自动填充）\n"
            "2. 选择 **LoRA**（或选 \"—\" 仅使用基础模型）\n"
            "3. 输入**文本**（支持 emoji 风格控制）\n"
            "4. **种子** 可选，留空为随机\n"
            "5. **生成** → 预览 → 命名保存\n\n"
            "输出：`output/irodori_infer/{名称}.wav`"
        ),
    },
    "ko": {
        # ── App ──
        "app_title": "VoiceDesignCloner",
        # ── Tab names ──
        "tab_voice_design": "보이스 디자인",
        "tab_voice_clone": "보이스 클론",
        "tab_lora": "LoRA 학습",
        "tab_irodori_infer": "Irodori 추론",
        "tab_tools": "도구",
        "tab_settings": "설정",
        "tab_manual": "매뉴얼",
        # ── Voice Design tab ──
        "vd_prompt_section": "### 1. 보이스 프롬프트",
        "vd_prompt_desc": "생성하고 싶은 목소리의 특징을 설명하세요 (어떤 언어도 가능)",
        "vd_prompt_label": "LLM 프롬프트",
        "vd_prompt_placeholder": "예: 차분한 성인 여성의 목소리, 낮은 톤",
        "vd_btn_translate_ja": "일본어로 번역",
        "vd_btn_translate_zh": "중국어로 번역",
        "vd_btn_translate_en": "영어로 번역",
        "vd_preset_accordion": "프리셋에서 선택",
        "vd_preset_ja_label": "일본어",
        "vd_preset_zh_label": "중국어",
        "vd_preset_en_label": "영어",
        "vd_btn_clear_preset": "지우기",
        "vd_params_section": "### 2. 생성 파라미터",
        "vd_temperature_label": "Temperature (높음=표현력 / 낮음=안정)",
        "vd_top_p_label": "Top-P (낮을수록 품질 안정)",
        "vd_top_k_label": "Top-K (후보 토큰 수)",
        "vd_rep_penalty_label": "반복 패널티",
        "vd_btn_reset_params": "기본값으로 초기화",
        "vd_sample_section": "### 3. 샘플 텍스트",
        "vd_sample_desc": "이 목소리로 읽을 문장",
        "vd_sample_label": "샘플 텍스트",
        "vd_tts_lang_label": "음성 생성 언어",
        "vd_preview_section": "### 4. 미리 듣기",
        "vd_preview_label": "미리 듣기",
        "vd_status_label": "상태",
        "vd_btn_generate": "생성",
        "vd_btn_reroll": "재생성",
        "vd_save_section": "### 5. 저장",
        "vd_save_name_label": "저장 이름",
        "vd_btn_save": "저장",
        # vd messages
        "vd_err_empty_prompt": "보이스 지시가 비어 있습니다",
        "vd_err_translate_empty": "텍스트를 입력해 주세요",
        "vd_err_translate_fail": "번역 오류: {}",
        "vd_err_generate_fail": "오류: {}",
        "vd_ok_generated": "생성 완료 ({}Hz)",
        "vd_err_no_audio": "저장할 오디오가 없습니다",
        "vd_ok_saved": "저장 완료: {}",
        "vd_err_save_fail": "오류: {}",
        # ── Voice Clone tab ──
        "vc_ref_section": "### 1. 참조 음성",
        "vc_ref_tab_shortcut": "바로가기",
        "vc_ref_tab_upload": "업로드",
        "vc_shortcut_label": "voice_design 번호",
        "vc_upload_audio_label": "오디오 파일",
        "vc_ref_text_label": "참조 음성 전사",
        "vc_ref_text_placeholder": "바로가기는 자동 입력",
        "vc_btn_refresh_ref": "목록 새로고침",
        "vc_corpus_section": "### 2. 코퍼스",
        "vc_corpus_tab_file": "파일 선택",
        "vc_corpus_tab_upload": "업로드",
        "vc_corpus_file_label": "코퍼스 파일",
        "vc_corpus_lang_label": "코퍼스 언어",
        "vc_corpus_upload_label": "텍스트 파일 (한 줄에 한 문장 .txt)",
        "vc_corpus_count_label": "사용할 문장 수 (0=전체)",
        "vc_corpus_total_lines_label": "총 문장 수",
        "vc_corpus_total_chars_label": "총 문자 수",
        "vc_btn_corpus_refresh": "코퍼스 정보 새로고침",
        "vc_settings_section": "### 3. 설정",
        "vc_model_label": "모델",
        "vc_lang_label": "언어",
        "vc_sr_label": "출력 샘플레이트 (Hz)",
        "vc_output_section": "### 출력 경로 (output/)",
        "vc_output_folder_label": "폴더 이름",
        "vc_wavs_folder_label": "오디오 하위 폴더 이름",
        "vc_esd_filename_label": "텍스트 목록 이름 (.txt 자동 추가)",
        "vc_btn_start": "일괄 생성 시작",
        "vc_btn_stop": "■ 정지",
        "vc_progress_section": "### 4. 진행 상황",
        "vc_progress_label": "상태",
        "vc_result_label": "결과",
        # vc messages
        "vc_err_no_ref": "오류: 참조 음성이 없습니다",
        "vc_err_ref_not_found": "오류: 참조 음성을 찾을 수 없습니다",
        "vc_err_empty_ref_text": "오류: 전사 텍스트가 비어 있습니다",
        "vc_err_no_text": "오류: 텍스트가 없습니다",
        "vc_err_text_load_fail": "오류: 텍스트 로드 실패 ({})",
        "vc_err_upload_path": "업로드된 파일 경로를 확인할 수 없습니다",
        "vc_ok_done": "완료!",
        "vc_result_files": "파일 수: {}\n총 재생 시간: {}\n출력 경로: {}\n텍스트 목록: {}",
        "vc_err_file_select": "파일 선택",
        "vc_err_file_load": "오류: {}",
        "vc_stopped": "정지했습니다",
        "vc_clone_fail": "오류: {}",
        # ── Tools tab ──
        "tools_resample_section": "### 리샘플",
        "tools_resample_desc": "output 폴더의 raw/ 내 WAV 파일을 일괄 리샘플하여 resampled/ 에 출력합니다.",
        "tools_resample_folder_label": "폴더 선택",
        "tools_resample_sr_label": "출력 샘플레이트 (Hz)",
        "tools_btn_resample": "리샘플 실행",
        "tools_resample_status_label": "상태",
        "tools_btn_resample_refresh": "새로고침",
        "tools_esd_section": "### esd.list 생성",
        "tools_esd_desc": "output 폴더를 선택하여 raw/*.wav 와 텍스트 목록에서 esd.list 를 생성합니다.",
        "tools_esd_folder_label": "폴더 선택",
        "tools_esd_speaker_label": "화자 이름 (speaker 열)",
        "tools_esd_lang_label": "언어 코드 (lang 열)",
        "tools_btn_esd": "esd.list 생성",
        "tools_esd_status_label": "상태",
        "tools_btn_esd_refresh": "새로고침",
        "tools_audio_info_section": "### 오디오 정보",
        "tools_audio_info_desc": "WAV 파일을 업로드하여 재생 시간 및 샘플레이트를 확인합니다.",
        "tools_audio_files_label": "WAV 파일 (복수 가능)",
        "tools_audio_info_label": "파일 정보",
        # tools messages
        "tools_err_no_folder": "오류: 폴더를 선택해 주세요",
        "tools_err_raw_not_found": "오류: {} 를 찾을 수 없습니다",
        "tools_err_no_wavs": "오류: raw/ 에 WAV 파일이 없습니다",
        "tools_err_folder_not_exist": "오류: {} 가 존재하지 않습니다",
        "tools_err_no_text": "오류: 텍스트를 찾을 수 없습니다. Neutral.txt 등이 필요합니다",
        "tools_resample_done": "완료: {}개 파일 리샘플 ({:.1f}초)\n출력 경로: {}",
        "tools_esd_done": "완료: {}줄의 esd.list 생성\n저장 경로: {}",
        "tools_esd_skip": "\n⚠ 텍스트 없음으로 건너뜀 ({}개): {}",
        "tools_audio_files": "파일 수: {} / 합계: {:.1f}초 ({:.1f}분)",
        "tools_audio_all_match": "\n전체 일치: {}Hz / {} / {}",
        "tools_audio_sr_mismatch": "\n⚠ 샘플레이트 불일치: {}",
        "tools_audio_ch_mismatch": "\n⚠ 채널 수 불일치: {}",
        "tools_audio_bit_mismatch": "\n⚠ 비트 깊이 불일치: {}",
        "tools_audio_mono": "모노",
        "tools_audio_multi_ch": "{}ch",
        "tools_audio_unreadable": "  {}: 읽을 수 없음",
        # ── Settings tab ──
        "settings_lang_section": "### 표시 언어",
        "settings_lang_label": "言語 / Language / 语言 / 언어",
        "settings_lang_note": "변경 후 앱을 재시작해 주세요.",
        "settings_lang_saved": "언어를 {} 로 설정했습니다. 재시작하면 적용됩니다.",
        "settings_lang_save_fail": "오류: {}",
        "settings_backend_section": "### 추론 백엔드",
        "settings_backend_desc": "**faster**: Qwen3-TTS의 CUDA Graph 가속 (6-10배 속도, GPU 전용)\n\n**Qwen3-TTS**: 표준 추론 (CPU/GPU 모두 지원)\n\n**Irodori-TTS**: 일본어 전용 48kHz 확산 모델 (GPU 필수)",
        "settings_backend_label": "백엔드",
        "settings_backend_status_label": "상태",
        "settings_backend_current": "현재: {}",
        "settings_backend_no_faster": " (faster 미설치)",
        "settings_backend_err": "오류: {}",
        "settings_backend_restart": "백엔드를 전환했습니다. 재시작 중...",
        "settings_sysinfo_section": "### 시스템 정보",
        "settings_gpu_label": "GPU",
        "settings_vram_label": "VRAM",
        "settings_faster_label": "faster-qwen3-tts",
        "settings_faster_installed": "설치됨",
        "settings_faster_not_installed": "미설치 (pip install faster-qwen3-tts)",
        "settings_irodori_installed": "설치됨",
        "settings_irodori_not_installed": "미설치 (setup.bat 다시 실행)",
        "settings_btn_refresh": "새로고침",
        # ── 보이스 클론: LoRA + 자동 학습 ──
        "vc_lora_label": "LoRA 어댑터",
        "vc_btn_lora_refresh": "새로고침",
        "vc_autotrain_section": "### LoRA 자동 학습",
        "vc_autotrain_label": "클론 완료 후 LoRA 학습 실행",
        "vc_autotrain_done": "LoRA 학습 완료!",
        # ── LoRA 탭 ──
        "lora_source_section": "### 1. 학습 데이터 (클론 출력)",
        "lora_source_label": "출력 폴더",
        "lora_settings_section": "### 2. 학습 설정",
        "lora_speaker_label": "화자 이름 (LoRA 식별자)",
        "lora_steps_label": "학습 스텝 수",
        "lora_advanced_section": "고급 설정",
        "lora_steps_override_label": "스텝 수 (프리셋 덮어쓰기)",
        "lora_batch_label": "배치 사이즈",
        "lora_workers_label": "DataLoader workers",
        "lora_lr_label": "학습률",
        "lora_existing_section": "### 기존 LoRA",
        "lora_existing_label": "저장된 LoRA 목록",
        "lora_existing_none": "(아직 없음)",
        "lora_progress_section": "### 3. 진행 상황",
        "lora_status_label": "상태",
        "lora_log_label": "로그",
        "lora_btn_refresh": "새로고침",
        "lora_btn_start": "학습 시작",
        "lora_btn_stop": "■ 정지",
        "lora_irodori_only_note": "_LoRA 학습은 Irodori-TTS 백엔드일 때만 사용 가능합니다._",
        "lora_err_not_irodori": "오류: 백엔드를 Irodori-TTS 로 전환해 주세요",
        "lora_err_no_source": "오류: 학습 데이터 (클론 출력 폴더)를 선택해 주세요",
        "lora_err_no_speaker": "오류: 화자 이름을 입력해 주세요",
        "lora_err_failed": "오류: {}",
        "lora_ok_done": "완료: speaker={} 출력={}",
        # ── Irodori 추론 탭 ──
        "ii_ref_section": "### 1. 참조 음성",
        "ii_model_section": "### 2. LoRA",
        "ii_text_section": "### 3. 텍스트",
        "ii_params_section": "### 4. 파라미터",
        "ii_preview_section": "### 5. 미리듣기",
        "ii_save_section": "### 6. 저장",
        "ii_caption_label": "캡션 (선택)",
        "ii_caption_placeholder": "예: 차분한 여성 목소리",
        "ii_text_label": "읽을 텍스트 (이모지 스타일 제어 지원)",
        "ii_text_placeholder": "예: 안녕하세요. 😆 반갑습니다!",
        "ii_seed_label": "시드 (비우면 랜덤)",
        "ii_btn_seed_random": "랜덤",
        "ii_irodori_only_note": "_Irodori 추론은 Irodori-TTS 백엔드일 때만 사용할 수 있습니다._",
        "ii_err_not_irodori": "오류: 백엔드를 Irodori-TTS 로 전환해 주세요",
        "ii_err_no_ref": "오류: 참조 음성을 선택해 주세요",
        "ii_err_ref_not_found": "오류: 참조 음성을 찾을 수 없습니다",
        "ii_err_no_text": "오류: 텍스트를 입력해 주세요",
        # ── Manual tab ──
        "manual_intro": (
            "## VoiceDesignCloner 란?\n\n"
            "**녹음 없이** 텍스트 프롬프트로 오리지널 목소리를 만들고, "
            "코퍼스를 이용해 그 목소리로 대량의 음성을 자동 생성하는 GUI 도구입니다.\n"
            "출력은 Style-Bert-VITS2 (SBV2) 등의 TTS 모델 학습에 바로 사용할 수 있는 교사 데이터 형식입니다.\n\n"
            "코퍼스 준비, 음성 양산, 리샘플 등의 번거로운 작업을 이 하나로 완결할 수 있습니다."
        ),
        "manual_voice_design": (
            "### 보이스 디자인 탭 — 목소리 만들기\n\n"
            "1. **보이스 프롬프트**에 만들고 싶은 목소리의 특징을 입력\n"
            "   - 한국어, 일본어, 영어, 중국어로 입력 가능합니다\n"
            "   - 번역 버튼으로 일본어/중국어/영어로 상호 변환 가능\n"
            "   - '프리셋에서 선택'에 일본어/중국어/영어 샘플이 있습니다\n"
            "2. **생성 파라미터**는 기본값 그대로도 OK, 취향에 맞게 조정 가능\n"
            "3. **샘플 텍스트**에 미리 듣기용 문장을 입력\n"
            "   - **음성 생성 언어**: 읽어줄 언어를 선택 (10개 언어 지원)\n"
            "   - 기본값은 설정 탭에서 선택한 UI 언어\n"
            "4. **생성** → 미리 듣기 → 마음에 들지 않으면 **재생성**\n"
            "5. 마음에 들면 **저장 이름**을 입력하고 **저장**\n"
            "   - `output/voice_design/` 에 `{저장명}.wav` + `{저장명}.txt` 세트로 저장됩니다\n"
            "   - 동일한 이름이 있으면 `_1`, `_2`... 가 자동으로 붙습니다\n"
            "   - 보이스 클론의 '바로가기'는 저장된 음성을 대상으로 합니다"
        ),
        "manual_voice_clone": (
            "### 보이스 클론 탭 — 목소리 양산하기\n\n"
            "1. **참조 음성**을 선택\n"
            "   - 바로가기: 보이스 디자인에서 저장한 목소리를 번호로 선택 (전사 자동 입력)\n"
            "   - 업로드: 직접 가진 음성 파일을 사용 (전사를 수동 입력)\n"
            "2. **코퍼스 언어**를 선택 (JA / EN / ZH)\n"
            "   - 해당 언어의 코퍼스 폴더로 전환됩니다\n"
            "   - 내장 코퍼스 (JA/EN/ZH) 사용 시 언어가 자동 연동됩니다\n"
            "3. **코퍼스 파일**을 선택\n"
            "   - ita_emotion100 (100문), ita_recitation324 (324문), mana652 (652문), rohan4600 (4600문)\n"
            "   - 업로드: 직접 만든 한 줄에 한 문장 .txt 파일도 사용 가능\n"
            "   - '사용할 문장 수'로 앞에서 N문만 생성 가능 (0=전체)\n"
            "4. **모델**·**음성 생성 언어**·**샘플레이트**를 선택\n"
            "   - **음성 생성 언어**: 텍스트 언어를 10개 언어에서 지정\n"
            "   - 직접 준비한 코퍼스를 사용할 때는 반드시 언어를 지정해 주세요\n"
            "   - 기본값은 설정 탭에서 선택한 UI 언어\n"
            "5. **출력 폴더** 이름을 설정\n"
            "6. **일괄 생성 시작**\n\n"
            "> **■ 정지** 버튼으로 도중에 중단할 수 있습니다."
        ),
        "manual_tools": (
            "### 도구 탭 — 후처리\n\n"
            "- **리샘플**: 폴더의 `raw/` 내 WAV를 일괄 변환 → `resampled/` 에 출력\n"
            "- **esd.list 생성**: `raw/` 의 WAV와 `Neutral.txt` 에서 SBV2용 목록 생성 (언어 코드 선택 가능)\n"
            "- **오디오 정보**: WAV 파일의 재생 시간·샘플레이트를 확인"
        ),
        "manual_sbv2": (
            "### Style-Bert-VITS2 에 전달하기\n\n"
            "1. `output/{폴더명}/raw/` → SBV2 의 `Data/{모델명}/raw/` 에 복사\n"
            "2. 도구 탭에서 esd.list 생성 → `Data/{모델명}/esd.list` 로 배치\n"
            "3. SBV2 의 WebUI에서 전처리 → 학습 실행"
        ),
        "manual_vram": (
            "### VRAM 참고\n\n"
            "| 모델 | VRAM (bf16) |\n"
            "|---|---|\n"
            "| 1.7B-VoiceDesign | ~7-8 GB |\n"
            "| 1.7B-Base | ~7-8 GB |\n"
            "| 0.6B-Base | ~3-4 GB |"
        ),
        "manual_backend": "",
        "manual_settings": (
            "### 설정 탭\n\n"
            "**추론 백엔드**\n\n"
            "| 백엔드 | 엔진 | 속도 | 지원 언어 | 비고 |\n"
            "|---|---|---|---|---|\n"
            "| **faster** | Qwen3-TTS | ~6-10배 속도 | 10개 언어 | GPU 필수, 0.6B-Base 미지원 |\n"
            "| **Qwen3-TTS** | Qwen3-TTS | 표준 속도 | 10개 언어 | CPU/GPU 모두 지원 |\n"
            "| **Irodori-TTS** | Irodori-TTS | 6-7초/문장 | 일본어만 | GPU 필수, 48kHz 확산 모델 |\n\n"
            "백엔드를 전환하면 앱이 자동 재시작되어, 각 탭이 해당 백엔드에 맞는 상태로 표시됩니다.\n\n"
            "**GPU 정보**\n\n"
            "현재 사용 중인 GPU 이름과 VRAM 사용량을 실시간으로 확인할 수 있습니다.\n\n"
            "**표시 언어**\n\n"
            "UI 표시 언어를 일본어 / 영어 / 중국어 / 한국어에서 선택할 수 있습니다.\n"
            "「Apply & Restart」버튼을 누르면 앱이 재시작되어 선택한 언어로 표시됩니다."
        ),
        "manual_irodori": (
            "### Irodori-TTS 정보\n\n"
            "[Irodori-TTS](https://github.com/Aratako/Irodori-TTS) 는 일본어 전용의 48kHz 확산 기반 TTS 모델입니다.\n\n"
            "**특징**\n\n"
            "- **48kHz・일본어 전용**: Qwen3-TTS 보다 높은 샘플레이트, 일본어 자연스러움에 중점\n"
            "- **캡션 제어**: 보이스 디자인에서 「차분한 여성 목소리」 등 자연어로 음색 지정\n"
            "- **제로샷 클론**: 보이스 클론에서 참조 음성 하나로 음색을 재현 (전사 불필요)\n\n"
            "**사용법**\n\n"
            "1. 설정 탭에서 **Irodori-TTS** 선택 (자동 재시작)\n"
            "2. 보이스 디자인 / 보이스 클론 탭을 평소처럼 사용\n"
            "   - 일본어 외 언어, 생성 파라미터, 참조 음성 전사 등은 잠금\n"
            "   - 내부적으로 디자인은 `v2-VoiceDesign`, 클론은 `v3` 사용\n\n"
            "**최초 실행 시 주의**\n\n"
            "- 첫 생성 시 Hugging Face 에서 모델을 자동 다운로드 (수백 MB, 약 5-10분)\n"
            "- 이후는 캐시에서 즉시 로드\n\n"
            "**설치**\n\n"
            "`setup.bat` / `setup.sh` 실행 시 GPU 가 감지되면 Irodori-TTS 가 자동 설치됩니다.\n"
            "설치 경로: `%USERPROFILE%\\.vdc-engines\\Irodori-TTS\\` (Linux: `~/.vdc-engines/`)."
        ),
        "manual_lora": (
            "### LoRA 학습 탭 — 음성 학습\n\n"
            "보이스 클론으로 생성한 음성을 사용해 Irodori-TTS 의 LoRA 를 학습합니다.\n"
            "학습 자체는 어느 백엔드에서도 실행 가능하지만, 학습된 LoRA 는 Irodori-TTS 백엔드에서만 사용 가능합니다.\n\n"
            "1. **학습 데이터** 로 보이스 클론 출력 폴더 선택\n"
            "2. **화자 이름** 입력 (LoRA 식별자)\n"
            "3. **스텝 수** 선택: `quick (3000)` / `normal (10000)` / `full (30000)`\n"
            "4. **고급 설정** (선택): 배치 사이즈, DataLoader workers, 학습률 조정 가능\n"
            "5. **학습 시작** → `lab 변환 → jsonl → 잠재 인코드 → train.py --lora` 자동 실행\n\n"
            "**원활한 학습**: 보이스 클론 탭의 「클론 완료 후 LoRA 학습 실행」 을 ON 하면 일괄 처리됩니다.\n\n"
            "**출력**: `output/lora/{화자명}/`.\n\n"
            "**주의**: LoRA 는 베이스 모델 + 참조 음성 위에 얹는 적응층이므로 추론 시에도 참조 음성이 필요합니다."
        ),
        "manual_irodori_infer": (
            "### Irodori 추론 탭 — 학습된 LoRA 시연\n\n"
            "학습된 LoRA 로 한 문장씩 생성·확인·저장하는 인터랙티브 플레이그라운드입니다.\n\n"
            "1. **참조 음성** 선택 (LoRA 선택 시 학습 데이터에서 자동 입력)\n"
            "2. **LoRA** 선택 (또는 \"—\" 베이스만)\n"
            "3. **텍스트** 입력 (이모지 스타일 제어 지원)\n"
            "4. **시드** 선택 (비우면 랜덤)\n"
            "5. **생성** → 미리듣기 → 이름 붙여 저장\n\n"
            "출력: `output/irodori_infer/{이름}.wav`"
        ),
    },
}

# Language display names for the settings dropdown
LANG_OPTIONS = {
    "ja": "日本語",
    "en": "English",
    "zh": "中文",
    "ko": "한국어",
}

# Maps UI language code to Qwen3-TTS language name
QWEN_LANG_MAP = {
    "JP": "Japanese",
    "EN": "English",
    "ZH": "Chinese",
    "KO": "Korean",
}

# Maps app language to default corpus language folder
CORPUS_LANG_FOLDER = {
    "ja": "japanese",
    "en": "english",
    "zh": "chinese",
    "ko": "korean",
}

# Maps app language to esd.list language code
APP_TO_ESD_LANG = {
    "ja": "JP",
    "en": "EN",
    "zh": "ZH",
    "ko": "KO",
}

# Default sample text per language
DEFAULT_SAMPLE_TEXTS = {
    "ja": "こんにちは、はじめまして。私の声はいかがですか？",
    "en": "Hello, nice to meet you. How do you like my voice?",
    "zh": "你好，很高兴认识你。你觉得我的声音怎么样？",
    "ko": "안녕하세요, 처음 뵙겠습니다. 제 목소리는 어떠세요?",
}


def t(key: str, lang: str | None = None) -> str:
    """Return the UI string for the given key in the current language."""
    from config import LANG as _lang
    use_lang = lang or _lang
    strings = _STRINGS.get(use_lang, _STRINGS["ja"])
    return strings.get(key, _STRINGS["ja"].get(key, key))
