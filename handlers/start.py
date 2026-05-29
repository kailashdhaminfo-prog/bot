from telegram import Update
from telegram.ext import ContextTypes
from keyboards import KB_LANG, KB_WELCOME, KB_MAIN
from utils import send_screen, t


async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    args = ctx.args
    if args and args[0] == 'schedule':
        from handlers.schedule import handle_schedule
        await handle_schedule(update, ctx, from_start=True)
        return
    await update.message.reply_text("🙏", reply_markup=KB_LANG)


async def handle_lang(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    ctx.user_data['lang'] = q.data
    await send_screen(
        q,
        t(ctx, 'welcome'),
        reply_markup=KB_WELCOME(q.data),
        parse_mode="Markdown"
    )


async def handle_main_menu(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    lang = ctx.user_data.get('lang', 'lang_uk')
    await send_screen(q, t(ctx, 'main_menu_prompt'), reply_markup=KB_MAIN(lang))
