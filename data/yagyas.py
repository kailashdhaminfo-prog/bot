import json, os

_base = os.path.dirname(__file__)


def _load(path: str) -> dict:
    with open(path, encoding='utf-8') as f:
        return json.load(f)


YAGYAS_DB: dict[str, list[str]] = _load(os.path.join(_base, '..', 'yagyas_raw.json'))
YAGYAS_DB_RU: dict[str, list[str]] = _load(os.path.join(_base, '..', 'yagyas_raw_ru.json'))
YAGYAS_DB_EN: dict[str, list[str]] = _load(os.path.join(_base, '..', 'yagyas_raw_en.json'))

MAX_CHUNK_LEN = 3800


def _db(lang: str) -> dict:
    if lang == 'lang_ru':
        return YAGYAS_DB_RU
    if lang == 'lang_en':
        return YAGYAS_DB_EN
    return YAGYAS_DB


def get_benefits(name: str, lang: str = 'lang_uk') -> list[str]:
    raw = _db(lang).get(name, [])
    return [b.strip() for b in raw if b.strip() and len(b.strip()) >= 4]


def _translated_name(name: str, lang: str) -> str:
    from data.life_map import translate_name
    return translate_name(name, lang)


def _header(name: str, lang: str) -> str:
    tname = _translated_name(name, lang)
    if lang == 'lang_ru':
        return f"*Основные преимущества ягьи {tname}:*"
    if lang == 'lang_en':
        return f"*Main benefits of {tname} yagya:*"
    return f"*Основні переваги яг'ї {name}:*"


def _not_found(name: str, lang: str) -> str:
    tname = _translated_name(name, lang)
    if lang == 'lang_ru':
        return f"🔥 *Ягья {tname}*\n\n_Обратитесь к нашему менеджеру за деталями._"
    if lang == 'lang_en':
        return f"🔥 *{tname} Yagya*\n\n_Please contact our manager for details._"
    return f"🔥 *Яг'я {name}*\n\n_Зверніться за деталями до нашого менеджера._"


def _build_lines(name: str, benefits: list[str], lang: str) -> list[str]:
    lines = [_header(name, lang), ""]

    for item in benefits:
        if item.startswith("Основні переваги") or item.startswith("Основные преимущества") or item.startswith("Main benefits"):
            continue

        if '— -' in item:
            _, first_bullet = item.split('— -', 1)
            lines.append(f"- {first_bullet.strip().rstrip(';')};")
            continue

        if len(item) < 55 and ' — ' not in item and ';' not in item and not item.startswith('- '):
            lines.append("")
            lines.append(f"*{item}*")
            lines.append("")
            continue

        if ' — ' in item and not item.startswith('- '):
            parts = item.split(' — ', 1)
            title = parts[0].strip().rstrip('-').strip()
            desc = parts[1].strip()
            lines.append(f"*{title}* — {desc}")
            lines.append("")
            continue

        if item.startswith('- '):
            item = item[2:]
        item = item.rstrip('.')
        if not item.endswith(';'):
            item += ';'
        lines.append(f"- {item}")

    return lines


def format_yagya_chunks(name: str, lang: str = 'lang_uk') -> list[str]:
    benefits = get_benefits(name, lang)

    if not benefits:
        return [_not_found(name, lang)]

    all_lines = _build_lines(name, benefits, lang)

    chunks = []
    current: list[str] = []
    current_len = 0

    for line in all_lines:
        add_len = len(line) + 1
        if current_len + add_len > MAX_CHUNK_LEN and current:
            chunks.append("\n".join(current).strip())
            current = [line]
            current_len = add_len
        else:
            current.append(line)
            current_len += add_len

    if current:
        chunks.append("\n".join(current).strip())

    return chunks or [_not_found(name, lang)]


def format_yagya_screen(name: str, lang: str = 'lang_uk') -> str:
    chunks = format_yagya_chunks(name, lang)
    return chunks[0] if chunks else _not_found(name, lang)
