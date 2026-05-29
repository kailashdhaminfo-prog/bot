from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from keyboards import KB_LIFE
from data.life_map import LIFE_MAP, translate_name
from utils import send_screen, t


async def handle_life(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    lang = ctx.user_data.get('lang', 'lang_uk')
    await send_screen(q, t(ctx, 'life_choose_sphere'), reply_markup=KB_LIFE(lang))


async def handle_life_category(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    cat_key = q.data.replace("life_", "")
    cat = LIFE_MAP.get(cat_key)
    if not cat:
        return

    ctx.user_data['life_cat'] = cat_key
    lang = ctx.user_data.get('lang', 'lang_uk')

    rows = [
        [InlineKeyboardButton(t(ctx, f'sub_{sub_key}'), callback_data=f"sub_{sub_key}")]
        for sub_key in cat["subcategories"]
    ]
    rows.append([InlineKeyboardButton(t(ctx, 'btn_back'), callback_data="life")])

    await send_screen(q, t(ctx, 'life_choose_sub'), reply_markup=InlineKeyboardMarkup(rows))


async def handle_subcategory(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    sub_key = q.data.replace("sub_", "")

    for cat_key, cat in LIFE_MAP.items():
        if sub_key in cat["subcategories"]:
            _, yagyas = cat["subcategories"][sub_key]

            ctx.user_data['back_source'] = 'life'
            ctx.user_data['recommended_yagyas'] = yagyas
            ctx.user_data['sub_key'] = sub_key
            ctx.user_data['life_cat'] = cat_key

            sub_label = t(ctx, f'sub_{sub_key}')

            lang = ctx.user_data.get('lang', 'lang_uk')
            rows = [
                [InlineKeyboardButton(f"🔥 {translate_name(y, lang)}", callback_data=f"yagya_{y}")]
                for y in yagyas
            ]
            rows.append([InlineKeyboardButton(t(ctx, 'btn_back'), callback_data=f"life_{cat_key}")])

            await send_screen(
                q,
                f"*{sub_label}*\n\n{t(ctx, 'life_choose_yagya')}",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(rows)
            )
            return
