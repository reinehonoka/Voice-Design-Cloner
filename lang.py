"""Internationalization strings for VoiceDesignCloner.

Supported languages: ja (Japanese), en (English), zh (Chinese)
"""

_STRINGS: dict[str, dict[str, str]] = {
    "ja": {
        # ── App ──
        "app_title": "VoiceDesignCloner",
        # ── Tab names ──
        "tab_voice_design": "ボイスデザイン",
        "tab_voice_clone": "ボイスクローン",
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
        "settings_lang_label": "言語 / Language / 语言",
        "settings_lang_note": "変更後はアプリを再起動してください。",
        "settings_lang_saved": "言語を {} に設定しました。再起動すると反映されます。",
        "settings_lang_save_fail": "エラー: {}",
        "settings_backend_section": "### 推論バックエンド",
        "settings_backend_desc": "**faster**: CUDA Graph高速化（6-10倍速、GPU専用）\n\n**standard**: 標準推論（CPU/GPU両対応）",
        "settings_backend_label": "バックエンド",
        "settings_backend_status_label": "ステータス",
        "settings_backend_current": "現在: {}",
        "settings_backend_no_faster": "（faster未インストール）",
        "settings_backend_err": "エラー: {}",
        "settings_sysinfo_section": "### システム情報",
        "settings_gpu_label": "GPU",
        "settings_vram_label": "VRAM",
        "settings_faster_label": "faster-qwen3-tts",
        "settings_faster_installed": "インストール済み",
        "settings_faster_not_installed": "未インストール（pip install faster-qwen3-tts）",
        "settings_btn_refresh": "更新",
        # ── Manual tab ──
        "manual_intro": (
            "## VoiceDesignCloner とは\n\n"
            "**録音不要**でオリジナルの声をテキストプロンプトから作成し、"
            "コーパスを用いてその声で大量の音声を自動生成する一貫したGUIツールです。\n"
            "出力は Style-Bert-VITS2（SBV2）などのTTSモデル学習にそのまま使える教師データ形式になっています。\n\n"
            "音声合成の学習で地味に面倒な**コーパスの用意・音声の量産・リサンプル**などが、これ一つで完結します。"
        ),
        "manual_voice_design": (
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
        ),
        "manual_voice_clone": (
            "### Voice Clone タブ — 声を量産する\n\n"
            "1. **参照音声** を選ぶ\n"
            "   - ショートカット: Voice Design で保存した声を番号で選択（書き起こしは自動入力）\n"
            "   - アップロード: 自前の音声を使う場合（その声の書き起こしを手動入力）\n"
            "2. **コーパス** を選ぶ（Settings の言語設定に応じて JP/EN/ZH コーパスが切り替わります）\n"
            "   - ita_emotion100（100文）、ita_recitation324（324文）、mana652（652文）、rohan4600（4600文）\n"
            "   - all は上記すべてを結合したもの（5676文）\n"
            "   - アップロード: 自作の1行1文の .txt ファイルも使えます\n"
            "   - 「使用する文数」で先頭N文だけ生成可（0=すべて）\n"
            "3. **言語** を選択（JP/EN/ZH） — モデルへの言語指示に使用\n"
            "4. **モデル** と **サンプルレート** を選択\n"
            "   - SBV2 で使うことを想定してデフォルトは 44100Hz\n"
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
        "manual_backend": (
            "### 推論バックエンド（Settings タブ）\n\n"
            "Settings タブでバックエンドと表示言語を切り替えられます。\n\n"
            "| バックエンド | 速度 | 対応モデル | 備考 |\n"
            "|---|---|---|---|\n"
            "| **faster** | 約6-10倍速（RTF ~2.0） | 1.7B-VoiceDesign / 1.7B-Base | GPU必須 |\n"
            "| **standard** | 標準速度 | すべて | CPU/GPU両対応 |\n\n"
            "**0.6B-Base は faster 非対応**です。"
        ),
    },
    "en": {
        # ── App ──
        "app_title": "VoiceDesignCloner",
        # ── Tab names ──
        "tab_voice_design": "Voice Design",
        "tab_voice_clone": "Voice Clone",
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
        "settings_lang_label": "言語 / Language / 语言",
        "settings_lang_note": "Restart the app to apply changes.",
        "settings_lang_saved": "Language set to {}. Restart to apply.",
        "settings_lang_save_fail": "Error: {}",
        "settings_backend_section": "### Inference Backend",
        "settings_backend_desc": "**faster**: CUDA Graph acceleration (6-10x, GPU only)\n\n**standard**: Standard inference (CPU/GPU)",
        "settings_backend_label": "Backend",
        "settings_backend_status_label": "Status",
        "settings_backend_current": "Current: {}",
        "settings_backend_no_faster": " (faster not installed)",
        "settings_backend_err": "Error: {}",
        "settings_sysinfo_section": "### System Info",
        "settings_gpu_label": "GPU",
        "settings_vram_label": "VRAM",
        "settings_faster_label": "faster-qwen3-tts",
        "settings_faster_installed": "Installed",
        "settings_faster_not_installed": "Not installed (pip install faster-qwen3-tts)",
        "settings_btn_refresh": "Refresh",
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
            "   - Any language works, but English or Chinese is recommended\n"
            "   - Use translation buttons to convert to Chinese/English\n"
            "   - Presets are available in the accordion\n"
            "2. **Generation Parameters** can be left at defaults\n"
            "3. Enter preview text in **Sample Text**\n"
            "4. **Generate** → Preview → **Re-roll** if unsatisfied\n"
            "5. Enter a **Save Name** and click **Save**\n"
            "   - Saved as `{name}.wav` + `{name}.txt` under `output/voice_design/`\n"
            "   - Auto-appends `_1`, `_2`... if name already exists"
        ),
        "manual_voice_clone": (
            "### Voice Clone Tab — Mass-Produce Audio\n\n"
            "1. Choose a **Reference Voice**\n"
            "   - Shortcut: select by number from saved Voice Design voices\n"
            "   - Upload: use your own audio (enter transcript manually)\n"
            "2. Choose a **Corpus** (switches between JP/EN/ZH based on Settings language)\n"
            "   - ita_emotion100 (100), ita_recitation324 (324), mana652 (652), rohan4600 (4600)\n"
            "   - all = all combined (5676 sentences)\n"
            "   - Upload: use a custom one-sentence-per-line .txt file\n"
            "3. Select **Language** (JP/EN/ZH) — passed to the model\n"
            "4. Choose **Model** and **Sample Rate**\n"
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
        "manual_backend": (
            "### Inference Backend (Settings Tab)\n\n"
            "Switch backend and display language from the Settings tab.\n\n"
            "| Backend | Speed | Models | Notes |\n"
            "|---|---|---|---|\n"
            "| **faster** | ~6-10x (RTF ~2.0) | 1.7B-VoiceDesign / 1.7B-Base | GPU required |\n"
            "| **standard** | Normal | All | CPU/GPU |\n\n"
            "**0.6B-Base does not support faster** — auto falls back to standard."
        ),
    },
    "zh": {
        # ── App ──
        "app_title": "VoiceDesignCloner",
        # ── Tab names ──
        "tab_voice_design": "声音设计",
        "tab_voice_clone": "声音克隆",
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
        "settings_lang_label": "言語 / Language / 语言",
        "settings_lang_note": "更改后请重启应用。",
        "settings_lang_saved": "语言已设置为 {}。重启后生效。",
        "settings_lang_save_fail": "错误: {}",
        "settings_backend_section": "### 推理后端",
        "settings_backend_desc": "**faster**: CUDA Graph加速（6-10倍速，仅GPU）\n\n**standard**: 标准推理（CPU/GPU均可）",
        "settings_backend_label": "后端",
        "settings_backend_status_label": "状态",
        "settings_backend_current": "当前: {}",
        "settings_backend_no_faster": "（faster未安装）",
        "settings_backend_err": "错误: {}",
        "settings_sysinfo_section": "### 系统信息",
        "settings_gpu_label": "GPU",
        "settings_vram_label": "显存",
        "settings_faster_label": "faster-qwen3-tts",
        "settings_faster_installed": "已安装",
        "settings_faster_not_installed": "未安装（pip install faster-qwen3-tts）",
        "settings_btn_refresh": "刷新",
        # ── Manual tab ──
        "manual_intro": (
            "## 什么是 VoiceDesignCloner？\n\n"
            "一款**无需录音**、通过文本提示词创建原创声音，并利用语料库自动批量生成音频的一体化GUI工具。\n"
            "输出格式兼容 Style-Bert-VITS2（SBV2）等TTS模型训练所需的教学数据格式。\n\n"
            "语料库准备、音频批量生成、重采样等繁琐工作，一个工具全部搞定。"
        ),
        "manual_voice_design": (
            "### Voice Design 标签 — 创建声音\n\n"
            "1. 在**声音提示词**中描述想要的声音特征\n"
            "   - 支持任何语言，推荐使用英文或中文\n"
            "   - 可使用翻译按钮转换为中文/英文\n"
            "   - 也可从预设中选择\n"
            "2. **生成参数**保持默认即可，也可根据喜好调整\n"
            "3. 在**示例文本**中输入预览用的文章\n"
            "4. **生成** → 预览播放 → 不满意则**重新生成**\n"
            "5. 满意后填写**保存名称**并**保存**"
        ),
        "manual_voice_clone": (
            "### Voice Clone 标签 — 批量生产音频\n\n"
            "1. 选择**参考音频**\n"
            "2. 选择**语料库**（根据Settings中的语言设置切换JP/EN/ZH语料库）\n"
            "3. 选择**语言**（JP/EN/ZH）— 传递给模型的语言指示\n"
            "4. 选择**模型**和**采样率**\n"
            "5. 设置**输出文件夹**名称\n"
            "6. 点击**开始批量生成**"
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
        "manual_backend": (
            "### 推理后端（Settings标签）\n\n"
            "可在Settings标签中切换后端和显示语言。\n\n"
            "| 后端 | 速度 | 支持模型 | 备注 |\n"
            "|---|---|---|---|\n"
            "| **faster** | ~6-10倍速 | 1.7B-VoiceDesign / 1.7B-Base | 需要GPU |\n"
            "| **standard** | 标准速度 | 全部 | CPU/GPU均可 |\n\n"
            "**0.6B-Base 不支持faster**，会自动使用standard。"
        ),
    },
}

# Language display names for the settings dropdown
LANG_OPTIONS = {
    "ja": "日本語",
    "en": "English",
    "zh": "中文",
}

# Maps UI language code to Qwen3-TTS language name
QWEN_LANG_MAP = {
    "JP": "Japanese",
    "EN": "English",
    "ZH": "Chinese",
}

# Maps app language to default corpus language folder
CORPUS_LANG_FOLDER = {
    "ja": "japanese",
    "en": "english",
    "zh": "chinese",
}

# Maps app language to esd.list language code
APP_TO_ESD_LANG = {
    "ja": "JP",
    "en": "EN",
    "zh": "ZH",
}

# Default sample text per language
DEFAULT_SAMPLE_TEXTS = {
    "ja": "こんにちは、はじめまして。私の声はいかがですか？",
    "en": "Hello, nice to meet you. How do you like my voice?",
    "zh": "你好，很高兴认识你。你觉得我的声音怎么样？",
}


def t(key: str, lang: str | None = None) -> str:
    """Return the UI string for the given key in the current language."""
    from config import LANG as _lang
    use_lang = lang or _lang
    strings = _STRINGS.get(use_lang, _STRINGS["ja"])
    return strings.get(key, _STRINGS["ja"].get(key, key))
