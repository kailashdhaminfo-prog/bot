import httpx
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import MANAGER_CHAT_ID, SUPABASE_URL, SUPABASE_SECRET_KEY
from utils import send_screen, t

# (field_key, string_key, optional)
FIELDS_GROUP = [
    ("full_name",   "yf_full_name",   False),
    ("spirit_name", "yf_spirit_name", True),
    ("birth_year",  "yf_birth_year",  False),
    ("nakshatra",   "yf_nakshatra",   True),
    ("phone",       "yf_phone",       True),
    ("photo",       "yf_photo",       True),
]

FIELDS_INDIVIDUAL = [
    ("full_name",   "yf_full_name",   False),
    ("spirit_name", "yf_spirit_name", True),
    ("birth_year",  "yf_birth_year",  False),
    ("nakshatra",   "yf_nakshatra",   True),
    ("sankalpa",    "yf_sankalpa",    False),
    ("phone",       "yf_phone",       True),
    ("photo",       "yf_photo",       True),
]

_GROUP_PKGS = {"pkg_group", "pkg_puja"}


def _fields_for(pkg_id: str) -> list:
    return FIELDS_GROUP if pkg_id in _GROUP_PKGS else FIELDS_INDIVIDUAL


def _pay_url(pkg_id: str) -> str:
    from keyboards import _PAY_URLS
    return _PAY_URLS.get(pkg_id, "")


def _step_kb(step: int, ctx, pkg_id: str, optional: bool, is_last: bool) -> InlineKeyboardMarkup:
    """Keyboard for each form step: optional skip + pay button only on last step."""
    rows = []
    if optional:
        rows.append([InlineKeyboardButton(t(ctx, 'yf_skip_btn'), callback_data=f"yagya_form_skip_{step}")])
    if is_last:
        rows.append([InlineKeyboardButton(t(ctx, 'yf_pay_btn'), url=_pay_url(pkg_id))])
    return InlineKeyboardMarkup(rows) if rows else None


async def handle_yagya_order(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    """Triggered by order_{pkg_id} — shows intro with first form question."""
    q = update.callback_query
    await q.answer()

    pkg_id = q.data.replace("order_", "")
    ctx.user_data['yf_pkg'] = pkg_id
    ctx.user_data['yf_data'] = {}
    ctx.user_data['yf_step'] = 0

    fields = _fields_for(pkg_id)
    total = len(fields)
    _, str_key, optional = fields[0]
    is_last = (total == 1)

    intro = t(ctx, 'yf_form_intro')
    label = t(ctx, str_key)
    text = f"{intro}\n\n*1/{total}* — *{label}:*"

    kb = _step_kb(0, ctx, pkg_id, optional, is_last)
    await q.message.reply_text(text, parse_mode="Markdown", reply_markup=kb)


async def _ask_step(update: Update, ctx: ContextTypes.DEFAULT_TYPE, step: int):
    pkg_id = ctx.user_data.get('yf_pkg', 'pkg_group')
    fields = _fields_for(pkg_id)
    total = len(fields)
    field_key, str_key, optional = fields[step]
    is_last = (step == total - 1)

    label = t(ctx, str_key)
    text = f"*{step + 1}/{total}* — *{label}:*"
    kb = _step_kb(step, ctx, pkg_id, optional, is_last)

    if update.callback_query:
        await update.callback_query.message.reply_text(text, parse_mode="Markdown", reply_markup=kb)
    else:
        await update.message.reply_text(text, parse_mode="Markdown", reply_markup=kb)


async def handle_yagya_form_skip(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    """Skip button pressed for optional field."""
    q = update.callback_query
    await q.answer()

    step = int(q.data.replace("yagya_form_skip_", ""))
    pkg_id = ctx.user_data.get('yf_pkg', 'pkg_group')
    fields = _fields_for(pkg_id)
    field_key = fields[step][0]

    ctx.user_data['yf_data'][field_key] = None
    await _advance(update, ctx, step)


async def handle_yagya_form_text(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    """Process text answer for current form step."""
    step = ctx.user_data.get('yf_step')
    if step is None:
        return

    pkg_id = ctx.user_data.get('yf_pkg', 'pkg_group')
    fields = _fields_for(pkg_id)
    field_key = fields[step][0]

    ctx.user_data['yf_data'][field_key] = update.message.text
    await _advance(update, ctx, step)


async def handle_yagya_form_photo(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    """Process photo for current form step."""
    step = ctx.user_data.get('yf_step')
    if step is None:
        return

    pkg_id = ctx.user_data.get('yf_pkg', 'pkg_group')
    fields = _fields_for(pkg_id)
    field_key = fields[step][0]

    if field_key != 'photo':
        await update.message.reply_text("📎")
        return

    # Accept both compressed photos and files sent as documents
    if update.message.photo:
        file_id = update.message.photo[-1].file_id
    elif update.message.document:
        file_id = update.message.document.file_id
    else:
        return

    ctx.user_data['yf_data']['photo_file_id'] = file_id

    # Upload to Supabase Storage and store public URL
    photo_url = await _upload_photo(ctx, file_id, update.effective_user.id)
    ctx.user_data['yf_data']['photo_url'] = photo_url
    ctx.user_data['yf_data']['photo'] = "✅"
    await _advance(update, ctx, step)


async def _advance(update: Update, ctx: ContextTypes.DEFAULT_TYPE, step: int):
    pkg_id = ctx.user_data.get('yf_pkg', 'pkg_group')
    fields = _fields_for(pkg_id)
    next_step = step + 1

    if next_step >= len(fields):
        ctx.user_data['yf_step'] = None
        await _save_to_supabase(update, ctx)
        await _notify_manager(update, ctx)
        await _form_done(update, ctx)
    else:
        ctx.user_data['yf_step'] = next_step
        await _ask_step(update, ctx, next_step)


async def _form_done(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    pkg_id = ctx.user_data.get('yf_pkg', 'pkg_group')

    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton(t(ctx, 'yf_pay_btn'), url=_pay_url(pkg_id))],
        [InlineKeyboardButton(t(ctx, 'btn_home'), callback_data="main_menu")],
    ])

    msg = update.message if update.message else update.callback_query.message
    await msg.reply_text(t(ctx, 'yf_done'), parse_mode="Markdown", reply_markup=kb)


async def _upload_photo(ctx, file_id: str, user_id: int) -> str | None:
    """Download photo from Telegram and upload to Supabase Storage. Returns public URL."""
    try:
        tg_file = await ctx.bot.get_file(file_id)
        async with httpx.AsyncClient() as client:
            # Download from Telegram
            resp = await client.get(tg_file.file_path, timeout=30)
            if resp.status_code != 200:
                return None

            filename = f"{user_id}_{file_id[-8:]}.jpg"
            upload = await client.post(
                f"{SUPABASE_URL}/storage/v1/object/order-photos/{filename}",
                content=resp.content,
                headers={
                    "apikey": SUPABASE_SECRET_KEY,
                    "Authorization": f"Bearer {SUPABASE_SECRET_KEY}",
                    "Content-Type": "image/jpeg",
                },
                timeout=30,
            )
            if upload.status_code in (200, 201):
                return f"{SUPABASE_URL}/storage/v1/object/public/order-photos/{filename}"
    except Exception:
        pass
    return None


async def _save_to_supabase(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    pkg_id = ctx.user_data.get('yf_pkg', '—')
    data = ctx.user_data.get('yf_data', {})

    payload = {
        "tg_user_id":    user.id,
        "tg_username":   user.username or None,
        "tg_name":       user.full_name or user.first_name or None,
        "pkg_id":        pkg_id,
        "yagya":         ctx.user_data.get('current_yagya') or None,
        "lang":          ctx.user_data.get('lang', 'lang_uk'),
        "full_name":     data.get('full_name') or None,
        "spirit_name":   data.get('spirit_name') or None,
        "birth_year":    data.get('birth_year') or None,
        "nakshatra":     data.get('nakshatra') or None,
        "sankalpa":      data.get('sankalpa') or None,
        "phone":         data.get('phone') or None,
        "photo_file_id": data.get('photo_file_id') or None,
        "photo_url":     data.get('photo_url') or None,
    }

    try:
        async with httpx.AsyncClient() as client:
            await client.post(
                f"{SUPABASE_URL}/rest/v1/kailashdham_orders",
                json=payload,
                headers={
                    "apikey": SUPABASE_SECRET_KEY,
                    "Authorization": f"Bearer {SUPABASE_SECRET_KEY}",
                    "Content-Type": "application/json",
                    "Prefer": "return=minimal",
                },
                timeout=10,
            )
    except Exception:
        pass


async def _notify_manager(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not MANAGER_CHAT_ID:
        return

    user = update.effective_user
    pkg_id = ctx.user_data.get('yf_pkg', '—')
    yagya = ctx.user_data.get('current_yagya', '—')
    data = ctx.user_data.get('yf_data', {})
    lang = ctx.user_data.get('lang', 'lang_uk')

    name = user.full_name or user.first_name or "—"
    username = f"@{user.username}" if user.username else "—"

    pkg_titles = {
        'pkg_group':      {'lang_uk': 'Групова', 'lang_ru': 'Групповая', 'lang_en': 'Group'},
        'pkg_individual': {'lang_uk': 'Індивідуальна', 'lang_ru': 'Индивидуальная', 'lang_en': 'Individual'},
        'pkg_horoscope':  {'lang_uk': 'З гороскопом', 'lang_ru': 'С гороскопом', 'lang_en': 'With horoscope'},
        'pkg_vip':        {'lang_uk': 'VIP', 'lang_ru': 'VIP', 'lang_en': 'VIP'},
    }
    pkg_label = pkg_titles.get(pkg_id, {}).get(lang, pkg_id)

    lines = [
        t(ctx, 'yf_notify_header'),
        "",
        f"👤 {name} ({username})",
        f"🆔 `{user.id}`",
        f"🔥 Яг'я: *{yagya}*",
        f"📦 Пакет: *{pkg_label}*",
        "",
        f"*ПІБ:* {data.get('full_name') or '—'}",
        f"*Дух. ім'я:* {data.get('spirit_name') or '—'}",
        f"*Рік нар.:* {data.get('birth_year') or '—'}",
        f"*Накшатра:* {data.get('nakshatra') or '—'}",
    ]

    if 'sankalpa' in data:
        lines.append(f"*Санкальпа:* {data.get('sankalpa') or '—'}")

    lines += [
        f"*Телефон:* {data.get('phone') or '—'}",
        f"*Фото:* {data.get('photo') or '—'}",
    ]

    photo_file_id = data.get('photo_file_id')

    try:
        await ctx.bot.send_message(
            MANAGER_CHAT_ID,
            "\n".join(lines),
            parse_mode="Markdown"
        )
        if photo_file_id:
            await ctx.bot.send_photo(MANAGER_CHAT_ID, photo_file_id)
    except Exception:
        pass
