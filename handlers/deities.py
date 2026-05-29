from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from data.life_map import DEITY_GROUPS, translate_name
from utils import send_screen, t


async def handle_deities(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    rows = [
        [InlineKeyboardButton(t(ctx, f'dgrp_{key}'), callback_data=f"dgrp_{key}")]
        for key in DEITY_GROUPS
    ]
    rows.append([InlineKeyboardButton(t(ctx, 'btn_back'), callback_data="main_menu")])

    await send_screen(q, t(ctx, 'deities_prompt'), reply_markup=InlineKeyboardMarkup(rows))


async def handle_deity_group(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    grp_key = q.data.replace("dgrp_", "")
    group = DEITY_GROUPS.get(grp_key)
    if not group:
        return

    ctx.user_data['back_source'] = 'deities'
    ctx.user_data['dgrp_key'] = grp_key
    ctx.user_data.pop('sub_key', None)
    ctx.user_data.pop('life_cat', None)
    ctx.user_data['recommended_yagyas'] = []

    grp_label = t(ctx, f'dgrp_{grp_key}')
    lang = ctx.user_data.get('lang', 'lang_uk')
    rows = [[InlineKeyboardButton(translate_name(y, lang), callback_data=f"yagya_{y}")] for y in group["yagyas"]]
    rows.append([InlineKeyboardButton(t(ctx, 'btn_back'), callback_data="deities")])

    await send_screen(
        q,
        f"*{grp_label}*\n\n{t(ctx, 'deities_choose_yagya')}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(rows)
    )


async def handle_all_practices(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton(t(ctx, 'rit_yagya_btn'), callback_data="deities")],
        [InlineKeyboardButton(t(ctx, 'rit_puja_btn'), callback_data="rit_puja"),
         InlineKeyboardButton(t(ctx, 'rit_abhishek_btn'), callback_data="rit_abhishek")],
        [InlineKeyboardButton(t(ctx, 'rit_tarpana_btn'), callback_data="rit_tarpana"),
         InlineKeyboardButton(t(ctx, 'rit_shraddha_btn'), callback_data="rit_shraddha")],
        [InlineKeyboardButton(t(ctx, 'btn_back'), callback_data="main_menu")],
    ])

    await send_screen(q, t(ctx, 'practices_prompt'), reply_markup=kb)


async def handle_practice_info(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    key_map = {
        "info_puji":     "rit_puja_text",
        "info_abhishek": "rit_abhishek_text",
        "info_tarpana":  "rit_tarpana_text",
        "info_shraddha": "rit_shraddha_text",
    }

    text_key = key_map.get(q.data)
    text = t(ctx, text_key) if text_key else t(ctx, 'consult_manager')
    kb = InlineKeyboardMarkup([[InlineKeyboardButton(t(ctx, 'btn_back'), callback_data="all_practices")]])
    await send_screen(q, text, parse_mode="Markdown", reply_markup=kb)
