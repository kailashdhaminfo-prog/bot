import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from data.yagyas import format_yagya_screen, format_yagya_chunks
from data.life_map import translate_name
from utils import send_screen, t


def _yagya_kb(ctx) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t(ctx, 'yagya_select_btn'), callback_data="packages")],
        [InlineKeyboardButton(t(ctx, 'btn_back'), callback_data="back_from_yagya_to_list")],
    ])


async def handle_yagya(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    yagya_name = q.data.replace("yagya_", "")
    ctx.user_data['current_yagya'] = yagya_name

    lang = ctx.user_data.get('lang', 'lang_uk')
    chunks = format_yagya_chunks(yagya_name, lang)
    kb = _yagya_kb(ctx)

    if len(chunks) == 1:
        await send_screen(q, chunks[0], parse_mode="Markdown", reply_markup=kb)
    else:
        await send_screen(q, chunks[0], parse_mode="Markdown")
        for chunk in chunks[1:-1]:
            await asyncio.sleep(2)
            await q.message.reply_text(chunk, parse_mode="Markdown")
        await asyncio.sleep(2)
        await q.message.reply_text(chunks[-1], parse_mode="Markdown", reply_markup=kb)


async def handle_back_from_yagya(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    lang = ctx.user_data.get('lang', 'lang_uk')
    back_source = ctx.user_data.get('back_source', '')

    if back_source == 'mother':
        stage_key = ctx.user_data.get('mother_stage', '')
        if stage_key:
            from handlers.mother import mother_stage_screen
            text, kb = mother_stage_screen(stage_key, lang, ctx)
            await send_screen(q, text, parse_mode="Markdown", reply_markup=kb)
            return

    yagya_name = ctx.user_data.get('current_yagya')
    if yagya_name:
        text = format_yagya_screen(yagya_name, lang)
        await send_screen(q, text, parse_mode="Markdown", reply_markup=_yagya_kb(ctx))
        return

    await send_screen(q, t(ctx, 'main_menu_prompt'), reply_markup=__import__('keyboards').KB_MAIN(lang))


async def handle_back_from_yagya_to_list(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    back_source = ctx.user_data.get('back_source', '')
    sub_key = ctx.user_data.get('sub_key')
    life_cat = ctx.user_data.get('life_cat')
    recommended = ctx.user_data.get('recommended_yagyas', [])
    lang = ctx.user_data.get('lang', 'lang_uk')

    if back_source == 'life' and life_cat and sub_key:
        from data.life_map import LIFE_MAP
        cat = LIFE_MAP.get(life_cat, {})
        sub_data = cat.get("subcategories", {}).get(sub_key)
        if sub_data:
            _, yagyas = sub_data
            sub_label = t(ctx, f'sub_{sub_key}')
            rows = [
                [InlineKeyboardButton(f"🔥 {translate_name(y, lang)}", callback_data=f"yagya_{y}")]
                for y in yagyas
            ]
            rows.append([InlineKeyboardButton(t(ctx, 'btn_back'), callback_data=f"life_{life_cat}")])
            await send_screen(
                q,
                f"*{sub_label}*\n\n{t(ctx, 'life_choose_yagya')}",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(rows)
            )
            return

    if back_source == 'nakshatra':
        if len(recommended) > 1:
            rows = [
                [InlineKeyboardButton(f"🔥 {translate_name(y, lang)}", callback_data=f"yagya_{y}")]
                for y in recommended
            ]
            rows.append([InlineKeyboardButton(t(ctx, 'btn_back'), callback_data="nakshatra")])
            await send_screen(q, t(ctx, 'life_choose_yagya'), reply_markup=InlineKeyboardMarkup(rows))
        else:
            from data.life_map import NAKSHATRA_MAP
            rows = [[InlineKeyboardButton(translate_name(n, lang), callback_data=f"naksh_{n}")] for n in NAKSHATRA_MAP]
            rows.append([InlineKeyboardButton(t(ctx, 'nakshatra_unknown_btn'), callback_data="consult")])
            rows.append([InlineKeyboardButton(t(ctx, 'btn_back'), callback_data="main_menu")])
            await send_screen(
                q,
                t(ctx, 'nakshatra_prompt'),
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(rows)
            )
        return

    if back_source == 'planets':
        from data.life_map import PLANETS
        rows = [[InlineKeyboardButton(translate_name(p, lang), callback_data=f"yagya_{p}")] for p in PLANETS]
        rows.append([InlineKeyboardButton(t(ctx, 'btn_back'), callback_data="main_menu")])
        await send_screen(q, t(ctx, 'planets_prompt'), reply_markup=InlineKeyboardMarkup(rows))
        return

    if back_source == 'deities':
        from data.life_map import DEITY_GROUPS
        grp_key = ctx.user_data.get('dgrp_key')
        group = DEITY_GROUPS.get(grp_key, {})
        if group:
            grp_label = t(ctx, f'dgrp_{grp_key}')
            rows = [[InlineKeyboardButton(translate_name(y, lang), callback_data=f"yagya_{y}")] for y in group.get('yagyas', [])]
            rows.append([InlineKeyboardButton(t(ctx, 'btn_back'), callback_data="deities")])
            await send_screen(
                q,
                f"*{grp_label}*\n\n{t(ctx, 'deities_choose_yagya')}",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(rows)
            )
            return

    if back_source == 'schedule':
        from data.schedule import EVENTS
        evt_id = ctx.user_data.get('current_event')
        page = ctx.user_data.get('sched_page', 0)
        evt = next((e for e in EVENTS if e["id"] == evt_id), None)
        if evt:
            text = (
                f"*{evt['name']}*\n\n"
                f"{t(ctx, 'schedule_date')} {evt['date']}\n"
                f"{t(ctx, 'schedule_time')} {evt['time']}\n"
                f"{t(ctx, 'schedule_price')} {evt['price']}\n"
                f"_{t(ctx, 'schedule_hryvnia_note')}_"
            )
            rows = [[InlineKeyboardButton(t(ctx, 'schedule_pay_btn'), url=evt["payment_url"])]]
            if evt.get("yagya_key"):
                rows.append([InlineKeyboardButton(t(ctx, 'schedule_practice_btn'), callback_data=f"yagya_{evt['yagya_key']}")])
            rows.append([InlineKeyboardButton(t(ctx, 'schedule_consult_btn'), callback_data="consult")])
            rows.append([InlineKeyboardButton(t(ctx, 'btn_back'), callback_data=f"sched_page_{page}")])
            await send_screen(q, text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(rows))
            return

    from keyboards import KB_MAIN
    await send_screen(q, t(ctx, 'main_menu_prompt'), reply_markup=KB_MAIN(lang))
