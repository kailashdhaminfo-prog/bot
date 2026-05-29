from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from keyboards import KB_PACKAGES, format_package, kb_package_action
from config import MANAGER_CHAT_ID
from utils import send_screen, t


async def handle_packages(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    lang = ctx.user_data.get('lang', 'lang_uk')
    yagya = ctx.user_data.get('current_yagya', '')
    if yagya:
        from data.life_map import translate_name
        yagya_display = translate_name(yagya, lang)
        text = t(ctx, 'packages_choose_for', yagya=yagya_display)
    else:
        text = t(ctx, 'packages_choose')

    text += '\n' + t(ctx, 'packages_hryvnia')
    await send_screen(q, text, parse_mode="Markdown", reply_markup=KB_PACKAGES(lang))


async def handle_package_detail(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    pkg_id = q.data
    ctx.user_data['selected_package'] = pkg_id
    lang = ctx.user_data.get('lang', 'lang_uk')

    text = format_package(pkg_id, lang)
    await send_screen(q, text, parse_mode="Markdown", reply_markup=kb_package_action(pkg_id, lang))


async def handle_order(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    pkg_id = q.data.replace("order_", "")
    lang = ctx.user_data.get('lang', 'lang_uk')
    yagya = ctx.user_data.get('current_yagya', '—')
    user = update.effective_user

    await send_screen(
        q,
        t(ctx, 'order_thanks'),
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(t(ctx, 'btn_zaochna'), url="https://kailashdham.space/#zaochna-uchast")],
            [InlineKeyboardButton(t(ctx, 'btn_home'), callback_data="main_menu")],
        ])
    )

    if MANAGER_CHAT_ID:
        from keyboards import format_package as _fp, _PKG_PRICES
        title = t(ctx, f'{pkg_id}_title')
        price = _PKG_PRICES.get(pkg_id, {}).get(lang, '—')
        name = user.full_name or user.first_name or "—"
        username = f"@{user.username}" if user.username else "—"
        msg = (
            f"🔔 *New order!*\n\n"
            f"👤 Name: {name}\n"
            f"📱 Username: {username}\n"
            f"🆔 Telegram ID: {user.id}\n"
            f"🔥 Yagya: *{yagya}*\n"
            f"📦 Package: *{title}*\n"
            f"💰 Price: {price}"
        )
        try:
            await ctx.bot.send_message(MANAGER_CHAT_ID, msg, parse_mode="Markdown")
        except Exception:
            pass
