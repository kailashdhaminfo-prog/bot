from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils import send_screen, t


async def handle_practices(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton(t(ctx, 'rit_yagya_btn'), callback_data="rit_yagya")],
        [InlineKeyboardButton(t(ctx, 'rit_puja_btn'), callback_data="rit_puja")],
        [InlineKeyboardButton(t(ctx, 'rit_abhishek_btn'), callback_data="rit_abhishek")],
        [InlineKeyboardButton(t(ctx, 'rit_tarpana_btn'), callback_data="rit_tarpana")],
        [InlineKeyboardButton(t(ctx, 'rit_shraddha_btn'), callback_data="rit_shraddha")],
        [InlineKeyboardButton(t(ctx, 'rit_compare_btn'), callback_data="rit_compare")],
        [InlineKeyboardButton(t(ctx, 'btn_back'), callback_data="main_menu")],
    ])

    await send_screen(q, t(ctx, 'practices_prompt'), reply_markup=kb)


async def _handle_rit_yagya(update, ctx):
    q = update.callback_query
    await q.answer()

    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton(t(ctx, 'rit_sankalpa_btn'), callback_data="rit_sankalpa")],
        [InlineKeyboardButton(t(ctx, 'rit_sankalpa_how_btn'), callback_data="rit_sankalpa_how")],
        [InlineKeyboardButton(t(ctx, 'rit_group_btn'), callback_data="rit_yagya_group")],
        [InlineKeyboardButton(t(ctx, 'rit_ind_btn'), callback_data="rit_yagya_ind")],
        [InlineKeyboardButton(t(ctx, 'rit_select_btn'), callback_data="life")],
        [InlineKeyboardButton(t(ctx, 'btn_back'), callback_data="practices")],
    ])

    await send_screen(q, t(ctx, 'rit_yagya_text'), parse_mode="Markdown", reply_markup=kb)


async def _handle_rit_sankalpa(update, ctx):
    q = update.callback_query
    await q.answer()

    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton(t(ctx, 'rit_sankalpa_how_btn'), callback_data="rit_sankalpa_how")],
        [InlineKeyboardButton(t(ctx, 'btn_back'), callback_data="rit_yagya")],
    ])

    await send_screen(q, t(ctx, 'rit_sankalpa_text'), parse_mode="Markdown", reply_markup=kb)


async def _handle_rit_sankalpa_how(update, ctx):
    q = update.callback_query
    await q.answer()

    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton(t(ctx, 'schedule_consult_btn'), callback_data="consult")],
        [InlineKeyboardButton(t(ctx, 'btn_back'), callback_data="rit_sankalpa")],
    ])

    await send_screen(q, t(ctx, 'rit_sankalpa_how_text'), parse_mode="Markdown", reply_markup=kb)


async def _handle_rit_yagya_group(update, ctx):
    q = update.callback_query
    await q.answer()

    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton(t(ctx, 'rit_schedule_btn'), callback_data="schedule")],
        [InlineKeyboardButton(t(ctx, 'btn_back'), callback_data="rit_yagya")],
    ])

    await send_screen(q, t(ctx, 'rit_group_text'), parse_mode="Markdown", reply_markup=kb)


async def _handle_rit_yagya_ind(update, ctx):
    q = update.callback_query
    await q.answer()

    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton(t(ctx, 'rit_select_btn'), callback_data="life")],
        [InlineKeyboardButton(t(ctx, 'btn_back'), callback_data="rit_yagya")],
    ])

    await send_screen(q, t(ctx, 'rit_ind_text'), parse_mode="Markdown", reply_markup=kb)


async def _handle_rit_puja(update, ctx):
    q = update.callback_query
    await q.answer()

    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton(t(ctx, 'btn_back'), callback_data="practices")],
    ])

    await send_screen(q, t(ctx, 'rit_puja_text'), parse_mode="Markdown", reply_markup=kb)


async def _handle_rit_puja_req(update, ctx):
    q = update.callback_query
    await q.answer()
    ctx.user_data['practice_form'] = 'puja'
    kb = InlineKeyboardMarkup([[InlineKeyboardButton(t(ctx, 'btn_back'), callback_data="rit_puja")]])
    await send_screen(q, t(ctx, 'rit_puja_req_text'), reply_markup=kb)


async def _handle_rit_abhishek(update, ctx):
    q = update.callback_query
    await q.answer()

    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton(t(ctx, 'btn_back'), callback_data="practices")],
    ])

    await send_screen(q, t(ctx, 'rit_abhishek_text'), parse_mode="Markdown", reply_markup=kb)


async def _handle_rit_abhishek_req(update, ctx):
    q = update.callback_query
    await q.answer()
    ctx.user_data['practice_form'] = 'abhishek'
    kb = InlineKeyboardMarkup([[InlineKeyboardButton(t(ctx, 'btn_back'), callback_data="rit_abhishek")]])
    await send_screen(q, t(ctx, 'rit_abhishek_req_text'), reply_markup=kb)


async def _handle_rit_tarpana(update, ctx):
    q = update.callback_query
    await q.answer()

    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton(t(ctx, 'btn_back'), callback_data="practices")],
    ])

    await send_screen(q, t(ctx, 'rit_tarpana_text'), parse_mode="Markdown", reply_markup=kb)


async def _handle_rit_tarpana_req(update, ctx):
    q = update.callback_query
    await q.answer()
    ctx.user_data['practice_form'] = 'tarpana'
    kb = InlineKeyboardMarkup([[InlineKeyboardButton(t(ctx, 'btn_back'), callback_data="rit_tarpana")]])
    await send_screen(q, t(ctx, 'rit_tarpana_req_text'), reply_markup=kb)


async def _handle_rit_shraddha(update, ctx):
    q = update.callback_query
    await q.answer()

    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton(t(ctx, 'btn_back'), callback_data="practices")],
    ])

    await send_screen(q, t(ctx, 'rit_shraddha_text'), parse_mode="Markdown", reply_markup=kb)


async def _handle_rit_shraddha_req(update, ctx):
    q = update.callback_query
    await q.answer()
    ctx.user_data['practice_form'] = 'shraddha'
    kb = InlineKeyboardMarkup([[InlineKeyboardButton(t(ctx, 'btn_back'), callback_data="rit_shraddha")]])
    await send_screen(q, t(ctx, 'rit_shraddha_req_text'), reply_markup=kb)


async def _handle_rit_compare(update, ctx):
    q = update.callback_query
    await q.answer()

    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton(t(ctx, 'rit_yagya_btn'), callback_data="rit_yagya")],
        [InlineKeyboardButton(t(ctx, 'rit_puja_btn'), callback_data="rit_puja")],
        [InlineKeyboardButton(t(ctx, 'rit_abhishek_btn'), callback_data="rit_abhishek")],
        [InlineKeyboardButton(t(ctx, 'rit_tarpana_btn'), callback_data="rit_tarpana")],
        [InlineKeyboardButton(t(ctx, 'rit_shraddha_btn'), callback_data="rit_shraddha")],
        [InlineKeyboardButton(t(ctx, 'schedule_consult_btn'), callback_data="consult")],
        [InlineKeyboardButton(t(ctx, 'btn_back'), callback_data="practices")],
    ])

    await send_screen(q, t(ctx, 'rit_compare_text'), parse_mode="Markdown", reply_markup=kb)


_DISPATCH = {
    "rit_yagya":        _handle_rit_yagya,
    "rit_sankalpa":     _handle_rit_sankalpa,
    "rit_sankalpa_how": _handle_rit_sankalpa_how,
    "rit_yagya_group":  _handle_rit_yagya_group,
    "rit_yagya_ind":    _handle_rit_yagya_ind,
    "rit_puja":         _handle_rit_puja,
    "rit_puja_req":     _handle_rit_puja_req,
    "rit_abhishek":     _handle_rit_abhishek,
    "rit_abhishek_req": _handle_rit_abhishek_req,
    "rit_tarpana":      _handle_rit_tarpana,
    "rit_tarpana_req":  _handle_rit_tarpana_req,
    "rit_shraddha":     _handle_rit_shraddha,
    "rit_shraddha_req": _handle_rit_shraddha_req,
    "rit_compare":      _handle_rit_compare,
}


async def handle_rit_dispatch(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    handler = _DISPATCH.get(update.callback_query.data)
    if handler:
        await handler(update, ctx)


_CONFIRM_KEYS = {
    "puja":     "rit_confirm_puja",
    "abhishek": "rit_confirm_abhishek",
    "tarpana":  "rit_confirm_tarpana",
    "shraddha": "rit_confirm_shraddha",
}

_CONFIRM_BACK = {
    "puja":     "rit_puja",
    "abhishek": "rit_abhishek",
    "tarpana":  "rit_tarpana",
    "shraddha": "rit_shraddha",
}

_MANAGER_LABEL = {
    "puja":     "🪔 Запит на пуджу",
    "abhishek": "🫙 Запит на абхішейк",
    "tarpana":  "💧 Запит на тарпану",
    "shraddha": "🕯 Запит на шраддху",
}


async def handle_practice_form_text(update, ctx):
    practice_type = ctx.user_data.pop("practice_form", None)
    if not practice_type:
        return

    user = update.effective_user
    text = update.message.text

    from config import MANAGER_CHAT_ID
    if MANAGER_CHAT_ID:
        label = _MANAGER_LABEL.get(practice_type, "Практикаьний запит")
        try:
            await ctx.bot.send_message(
                chat_id=MANAGER_CHAT_ID,
                text=f"{label}\nВід: {user.full_name} (@{user.username or '—'})\n\n{text}"
            )
        except Exception:
            pass

    confirm = t(ctx, _CONFIRM_KEYS.get(practice_type, 'rit_confirm_puja'))
    back_cb = _CONFIRM_BACK.get(practice_type, "practices")

    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton(t(ctx, 'rit_manager_btn'), url="https://t.me/vitaliykharlamov")],
        [InlineKeyboardButton(t(ctx, 'btn_home'), callback_data="main_menu")],
        [InlineKeyboardButton(t(ctx, 'rit_practices_btn'), callback_data="practices")],
        [InlineKeyboardButton(t(ctx, 'btn_back'), callback_data=back_cb)],
    ])

    await update.message.reply_text(
        t(ctx, 'rit_done', confirm=confirm),
        reply_markup=kb
    )
