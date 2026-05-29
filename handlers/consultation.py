import httpx
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import MANAGER_CHAT_ID, SUPABASE_URL, SUPABASE_SECRET_KEY
from utils import send_screen, t

FORM_FIELD_KEYS = [
    ("name",      "form_field_name"),
    ("birthday",  "form_field_birthday"),
    ("birthtime", "form_field_birthtime"),
    ("country",   "form_field_country"),
    ("city",      "form_field_city"),
    ("nakshatra", "form_field_nakshatra"),
    ("request",   "form_field_request"),
]


def _skip_kb(field_index: int, ctx) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t(ctx, 'form_skip_btn'), callback_data=f"form_skip_{field_index}")]
    ])


async def handle_consult(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton(t(ctx, 'consult_request_btn'), callback_data="consult_request")],
        [InlineKeyboardButton(t(ctx, 'consult_help_btn'), callback_data="consult_help")],
        [InlineKeyboardButton(t(ctx, 'consult_manual_btn'), callback_data="main_menu")],
        [InlineKeyboardButton(t(ctx, 'btn_back'), callback_data="main_menu")],
    ])

    await send_screen(q, t(ctx, 'consult_prompt'), reply_markup=kb)


async def handle_consult_request(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton(t(ctx, 'consult_form_btn'), callback_data="form_start")],
        [InlineKeyboardButton(t(ctx, 'consult_freetext_btn'), callback_data="consult_freetext")],
        [InlineKeyboardButton(t(ctx, 'btn_back'), callback_data="consult")],
    ])

    await send_screen(q, t(ctx, 'consult_request_text'), reply_markup=kb)


async def handle_form_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    ctx.user_data['form'] = {}
    ctx.user_data['form_step'] = 0
    await _ask_field(update, ctx, 0)


async def _ask_field(update: Update, ctx: ContextTypes.DEFAULT_TYPE, step: int):
    label_key = FORM_FIELD_KEYS[step][1]
    text = f"*{t(ctx, label_key)}:*"

    if update.callback_query:
        await send_screen(update.callback_query, text, parse_mode="Markdown", reply_markup=_skip_kb(step, ctx))
    else:
        await update.message.reply_text(text, parse_mode="Markdown", reply_markup=_skip_kb(step, ctx))


async def handle_form_skip(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    step = int(q.data.replace("form_skip_", ""))
    field_key = FORM_FIELD_KEYS[step][0]
    ctx.user_data.setdefault('form', {})[field_key] = "—"

    next_step = step + 1
    if next_step >= len(FORM_FIELD_KEYS):
        await _form_done(update, ctx)
    else:
        ctx.user_data['form_step'] = next_step
        await _ask_field(update, ctx, next_step)


async def handle_form_text(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    step = ctx.user_data.get('form_step')
    if step is None:
        return

    field_key = FORM_FIELD_KEYS[step][0]
    ctx.user_data.setdefault('form', {})[field_key] = update.message.text

    next_step = step + 1
    if next_step >= len(FORM_FIELD_KEYS):
        await _form_done(update, ctx)
    else:
        ctx.user_data['form_step'] = next_step
        await _ask_field(update, ctx, next_step)


async def _form_done(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    form = ctx.user_data.get('form', {})
    ctx.user_data['form_step'] = None

    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton(t(ctx, 'btn_home'), callback_data="main_menu")],
        [InlineKeyboardButton(t(ctx, 'btn_all_practices'), callback_data="all_practices")],
    ])

    text = t(ctx, 'form_done')

    if update.callback_query:
        await send_screen(update.callback_query, text, reply_markup=kb)
    else:
        await update.message.reply_text(text, reply_markup=kb)

    if MANAGER_CHAT_ID:
        user = update.effective_user
        name = user.full_name or "—"
        username = f"@{user.username}" if user.username else "—"
        lines = [f"📋 *Нова анкета консультації!*\n", f"👤 {name} ({username})\n🆔 {user.id}\n"]
        for fkey, flabel_key in FORM_FIELD_KEYS:
            val = form.get(fkey, "—")
            lines.append(f"*{t(ctx, flabel_key)}:* {val}")
        try:
            await ctx.bot.send_message(MANAGER_CHAT_ID, "\n".join(lines), parse_mode="Markdown")
        except Exception:
            pass


async def handle_consult_help(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton(t(ctx, 'consult_problem_btn'), callback_data="life")],
        [InlineKeyboardButton(t(ctx, 'consult_direction_btn'), callback_data="life")],
        [InlineKeyboardButton(t(ctx, 'consult_unknown_btn'), callback_data="consult_unknown")],
        [InlineKeyboardButton(t(ctx, 'btn_back'), callback_data="consult")],
    ])

    await send_screen(q, t(ctx, 'consult_help_prompt'), reply_markup=kb)


async def handle_consult_unknown(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton(t(ctx, 'consult_form_btn'), callback_data="form_start")],
        [InlineKeyboardButton(t(ctx, 'consult_write_btn'), callback_data="consult_freetext")],
        [InlineKeyboardButton(t(ctx, 'btn_all_practices'), callback_data="all_practices")],
        [InlineKeyboardButton(t(ctx, 'btn_back'), callback_data="consult_help")],
    ])

    await send_screen(q, t(ctx, 'consult_unknown_text'), reply_markup=kb)


async def handle_consult_freetext(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    ctx.user_data['awaiting_freetext'] = True
    await send_screen(q, t(ctx, 'consult_freetext_prompt'))


async def handle_freetext_message(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.user_data.get('awaiting_freetext'):
        return False

    ctx.user_data['awaiting_freetext'] = False
    user = update.effective_user

    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton(t(ctx, 'btn_home'), callback_data="main_menu")],
        [InlineKeyboardButton(t(ctx, 'btn_all_practices'), callback_data="all_practices")],
    ])

    await update.message.reply_text(t(ctx, 'consult_done'), reply_markup=kb)

    # Save to Supabase
    try:
        payload = {
            "tg_user_id":  user.id,
            "tg_username": user.username or None,
            "tg_name":     user.full_name or user.first_name or None,
            "pkg_id":      "consult",
            "lang":        ctx.user_data.get('lang', 'lang_uk'),
            "sankalpa":    update.message.text,
        }
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

    if MANAGER_CHAT_ID:
        name = user.full_name or "—"
        username = f"@{user.username}" if user.username else "—"
        msg = (
            f"✉️ *Запит на консультацію!*\n\n"
            f"👤 {name} ({username})\n"
            f"🆔 {user.id}\n\n"
            f"*Запит:* {update.message.text}"
        )
        try:
            await ctx.bot.send_message(MANAGER_CHAT_ID, msg, parse_mode="Markdown")
        except Exception:
            pass

    return True
