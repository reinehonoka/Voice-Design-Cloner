"""Emoji style-control palette for Irodori-TTS.

Irodori-TTS reads emojis inline with the text to bias the speaking style
(emotion, pace, breath, etc.). The reference for these mappings is
``master/clone/clone.py`` in the upstream Irodori-TTS repo.
"""

from __future__ import annotations

# Ordered (emoji, japanese description) per category so the UI can lay them out
# the same way the user already knows from the CLI cheat sheet.
EMOJI_CATEGORIES: dict[str, list[tuple[str, str]]] = {
    "感情・表情": [
        ("😆", "喜びながら、明るく"),
        ("😰", "慌てて、動揺、緊張、どもり"),
        ("😠", "怒って、不機嫌"),
        ("😢", "悲しくて、泣きながら"),
        ("😱", "驚いて、恐怖"),
        ("😮", "感心して、感銘を受けて"),
        ("😤", "得意げに、鼻息を荒く"),
        ("🤤", "恍惚として、うっとりと"),
        ("😏", "ニヤリと、含み笑い、煽るような"),
        ("😋", "おどけて、ぺろりと舌を出して"),
        ("🥴", "酔ったように、意識が朦朧として"),
        ("🥵", "暑くて、息を切らして、のぼせて"),
        ("🥶", "寒くて、震えながら"),
        ("😴", "眠そうに、寝ぼけて"),
        ("🫠", "とろけるような、メロメロになって"),
        ("💗", "好き、愛を込めて、ドキドキして"),
        ("💢", "苛立って、強調して"),
        ("❓", "疑問、問いかけ（語尾を上げる）"),
        ("🤭", "笑い（くすくす、含み笑い）"),
        ("🥺", "声を震わせながら、自信なさげに"),
        ("🤔", "疑問の声"),
        ("😌", "安堵、満足げに"),
        ("🥱", "あくび"),
        ("😖", "苦しげに"),
    ],
    "発話スタイル・速度": [
        ("🎵", "鼻歌"),
        ("⏩", "早口、まくしたてる"),
        ("🐢", "ゆっくりと"),
        ("👂", "囁き、耳元の音"),
        ("⏸️", "間、沈黙"),
    ],
    "特殊な発話・状態": [
        ("😮‍💨", "吐息、溜息、寝息"),
        ("🌬️", "息切れ、荒い息遣い"),
        ("🥤", "唾を飲み込む音"),
        ("🤧", "咳き込み、鼻すすり、くしゃみ"),
        ("🤐", "口を塞がれたような声"),
        ("📞", "電話越し・スピーカー越しの音"),
        ("😒", "舌打ち"),
    ],
}


def append_emoji(current: str | None, emoji: str) -> str:
    """Append the emoji to ``current``. Empty input becomes just the emoji."""
    return (current or "") + emoji
