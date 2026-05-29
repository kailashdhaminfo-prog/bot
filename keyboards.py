from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from data.strings import t as _t


def kb(buttons: list[list[tuple[str, str]]]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(text, callback_data=data) for text, data in row]
        for row in buttons
    ])


# ── Screen 1: Language (no translation needed) ──────────────────────────────
KB_LANG = kb([
    [("Українська", "lang_uk")],
    [("Русский", "lang_ru")],
    [("English", "lang_en")],
])


# ── Screen 2: Welcome ───────────────────────────────────────────────────────
def KB_WELCOME(lang: str) -> InlineKeyboardMarkup:
    return kb([[(_t(lang, 'continue_btn'), "main_menu")]])


# ── Screen 3: Main menu ─────────────────────────────────────────────────────
def KB_MAIN(lang: str) -> InlineKeyboardMarkup:
    return kb([
        [(_t(lang, 'btn_life'), "life")],
        [(_t(lang, 'btn_mother'), "mother")],
        [(_t(lang, 'btn_planets'), "planets")],
        [(_t(lang, 'btn_deities'), "deities")],
        [(_t(lang, 'btn_all_yagyas'), "all_yagyas")],
        [(_t(lang, 'btn_nakshatra'), "nakshatra")],
        [(_t(lang, 'btn_consult_main'), "consult")],
        [(_t(lang, 'btn_practices_main'), "all_practices")],
        [(_t(lang, 'btn_about'), "about")],
        [(_t(lang, 'btn_schedule'), "schedule")],
    ])


# ── Screen 4: Life categories ───────────────────────────────────────────────
def KB_LIFE(lang: str) -> InlineKeyboardMarkup:
    return kb([
        [(_t(lang, 'life_cat_money'), "life_money")],
        [(_t(lang, 'life_cat_luck'), "life_luck")],
        [(_t(lang, 'life_cat_health'), "life_health")],
        [(_t(lang, 'life_cat_protection'), "life_protection")],
        [(_t(lang, 'life_cat_relations'), "life_relations")],
        [(_t(lang, 'life_cat_talents'), "life_talents")],
        [(_t(lang, 'life_cat_wisdom'), "life_wisdom")],
        [(_t(lang, 'life_cat_destiny'), "life_destiny")],
        [(_t(lang, 'life_cat_home'), "life_home")],
        [(_t(lang, 'life_cat_ancestors'), "life_ancestors")],
        [(_t(lang, 'life_cat_spiritual'), "life_spiritual")],
        [(_t(lang, 'btn_back'), "main_menu")],
    ])


# ── Packages keyboard ────────────────────────────────────────────────────────
_PAY_URLS = {
    "pkg_group":      "https://secure.wayforpay.com/button/b4b6640952126",
    "pkg_puja":       "https://secure.wayforpay.com/button/b1239221a1730",
    "pkg_individual": "https://secure.wayforpay.com/button/b615679cea637",
    "pkg_horoscope":  "https://secure.wayforpay.com/button/b86472b1dadcd",
    "pkg_vip":        "https://secure.wayforpay.com/button/be9e776842d5f",
}

_PKG_PRICES = {
    "pkg_group":      {"lang_uk": "від $39",  "lang_ru": "от $39",  "lang_en": "from $39"},
    "pkg_puja":       {"lang_uk": "від $10",  "lang_ru": "от $10",  "lang_en": "from $10"},
    "pkg_individual": {"lang_uk": "$169",      "lang_ru": "$169",    "lang_en": "$169"},
    "pkg_horoscope":  {"lang_uk": "$369",      "lang_ru": "$369",    "lang_en": "$369"},
    "pkg_vip":        {"lang_uk": "$1369",     "lang_ru": "$1369",   "lang_en": "$1369"},
}

_PKG_ITEMS = {
    "pkg_group":      ["pkg_item_participants", "pkg_item_intent", "pkg_item_photo"],
    "pkg_individual": ["pkg_item_personal", "pkg_item_time", "pkg_item_consult_short", "pkg_item_prasad"],
    "pkg_horoscope":  ["pkg_item_personal", "pkg_item_time", "pkg_item_consult_short", "pkg_item_prasad",
                       "pkg_item_horoscope", "pkg_item_mantra", "pkg_item_amulet"],
    "pkg_vip":        ["pkg_item_personal", "pkg_item_time", "pkg_item_consult", "pkg_item_prasad",
                       "pkg_item_horoscope", "pkg_item_mantra", "pkg_item_amulet_personal",
                       "pkg_item_kunda", "pkg_item_video"],
}


def KB_PACKAGES(lang: str) -> InlineKeyboardMarkup:
    def _btn(pkg_id: str) -> str:
        title = _t(lang, f'{pkg_id}_title')
        price = _PKG_PRICES[pkg_id].get(lang, _PKG_PRICES[pkg_id]['lang_uk'])
        return f"🔥 {price} — {title}"

    return InlineKeyboardMarkup([
        [InlineKeyboardButton(_btn("pkg_group"), callback_data="pkg_group")],
        [InlineKeyboardButton(_btn("pkg_individual"), callback_data="pkg_individual")],
        [InlineKeyboardButton(_btn("pkg_horoscope"), callback_data="pkg_horoscope")],
        [InlineKeyboardButton(_btn("pkg_vip"), callback_data="pkg_vip")],
        [InlineKeyboardButton(_t(lang, 'btn_back'), callback_data="back_from_yagya")],
    ])


def format_package(pkg_id: str, lang: str = 'lang_uk') -> str:
    title = _t(lang, f'{pkg_id}_title')
    price = _PKG_PRICES.get(pkg_id, {}).get(lang, '—')
    hryvnia = _t(lang, 'packages_hryvnia')
    desc = _t(lang, f'{pkg_id}_desc')

    lines = [f"🔥 *{title}*", f"💰 *{price}*", f"_{hryvnia}_\n"]
    for item_key in _PKG_ITEMS.get(pkg_id, []):
        lines.append(f"✓ {_t(lang, item_key)}")
    lines.append(f"\n_{desc}_")
    if pkg_id == 'pkg_vip':
        lines.append(f"\n{_t(lang, 'pkg_vip_limit')}")
    return "\n".join(lines)


def kb_package_action(pkg_id: str, lang: str = 'lang_uk') -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(_t(lang, 'packages_select_btn'), callback_data=f"order_{pkg_id}")],
        [InlineKeyboardButton(_t(lang, 'packages_back_btn'), callback_data="packages")],
        [InlineKeyboardButton(_t(lang, 'btn_home'), callback_data="main_menu")],
    ])
