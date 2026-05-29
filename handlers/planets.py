import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from data.life_map import PLANETS, NAKSHATRA_MAP, translate_name
from utils import send_screen, t


async def handle_planets(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    ctx.user_data['back_source'] = 'planets'
    ctx.user_data.pop('sub_key', None)
    ctx.user_data.pop('life_cat', None)
    ctx.user_data['recommended_yagyas'] = []

    lang = ctx.user_data.get('lang', 'lang_uk')
    rows = [[InlineKeyboardButton(translate_name(p, lang), callback_data=f"yagya_{p}")] for p in PLANETS]
    rows.append([InlineKeyboardButton(t(ctx, 'btn_back'), callback_data="main_menu")])

    await send_screen(q, t(ctx, 'planets_prompt'), reply_markup=InlineKeyboardMarkup(rows))


async def handle_nakshatra(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    lang = ctx.user_data.get('lang', 'lang_uk')

    rows = [[InlineKeyboardButton(translate_name(n, lang), callback_data=f"naksh_{n}")] for n in NAKSHATRA_MAP]
    rows.append([InlineKeyboardButton(t(ctx, 'nakshatra_unknown_btn'), callback_data="consult")])
    rows.append([InlineKeyboardButton(t(ctx, 'btn_back'), callback_data="main_menu")])

    await send_screen(q, t(ctx, 'nakshatra_prompt'), parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(rows))


async def handle_nakshatra_select(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    naksh_name = q.data.replace("naksh_", "")
    yagyas = NAKSHATRA_MAP.get(naksh_name, [])

    if not yagyas:
        await send_screen(q, t(ctx, 'nakshatra_not_found', name=naksh_name), parse_mode="Markdown")
        return

    ctx.user_data['back_source'] = 'nakshatra'
    ctx.user_data['recommended_yagyas'] = yagyas
    ctx.user_data.pop('sub_key', None)
    ctx.user_data.pop('life_cat', None)

    lang = ctx.user_data.get('lang', 'lang_uk')

    if len(yagyas) == 1:
        yagya_name = yagyas[0]
        ctx.user_data['current_yagya'] = yagya_name
        from data.yagyas import format_yagya_chunks
        chunks = format_yagya_chunks(yagya_name, lang)
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton(t(ctx, 'yagya_select_btn'), callback_data="packages")],
            [InlineKeyboardButton(t(ctx, 'btn_back'), callback_data="back_from_yagya_to_list")],
        ])
        if len(chunks) == 1:
            await send_screen(q, chunks[0], parse_mode="Markdown", reply_markup=kb)
        else:
            await send_screen(q, chunks[0], parse_mode="Markdown")
            for chunk in chunks[1:-1]:
                await asyncio.sleep(2)
                await q.message.reply_text(chunk, parse_mode="Markdown")
            await asyncio.sleep(2)
            await q.message.reply_text(chunks[-1], parse_mode="Markdown", reply_markup=kb)
    else:
        rows = [[InlineKeyboardButton(f"🔥 {translate_name(y, lang)}", callback_data=f"yagya_{y}")] for y in yagyas]
        rows.append([InlineKeyboardButton(t(ctx, 'btn_back'), callback_data="nakshatra")])
        await send_screen(
            q,
            t(ctx, 'nakshatra_recommended', name=naksh_name),
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(rows)
        )
