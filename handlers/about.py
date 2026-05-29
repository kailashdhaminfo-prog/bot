from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils import send_screen, t


async def handle_about(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton(t(ctx, 'about_teachers_btn'), callback_data="about_teachers")],
        [InlineKeyboardButton(t(ctx, 'btn_all_practices'), callback_data="all_practices")],
        [InlineKeyboardButton(t(ctx, 'btn_consult'), callback_data="consult")],
        [InlineKeyboardButton(t(ctx, 'btn_back'), callback_data="main_menu")],
    ])

    await send_screen(q, t(ctx, 'about_text'), parse_mode="Markdown", reply_markup=kb)


async def handle_about_teachers(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton(t(ctx, 'btn_all_practices'), callback_data="all_practices")],
        [InlineKeyboardButton(t(ctx, 'btn_consult'), callback_data="consult")],
        [InlineKeyboardButton(t(ctx, 'btn_back'), callback_data="about")],
    ])

    await send_screen(q, t(ctx, 'about_teachers_text'), parse_mode="Markdown", reply_markup=kb)
