from telegram import InlineKeyboardMarkup
from data.strings import t as _t_base


async def send_screen(q, text: str, reply_markup=None, parse_mode: str = None):
    """Send a new message and remove keyboard from the previous one."""
    kwargs = {}
    if reply_markup:
        kwargs["reply_markup"] = reply_markup
    if parse_mode:
        kwargs["parse_mode"] = parse_mode

    await q.message.reply_text(text, **kwargs)


def t(ctx, key: str, **kwargs) -> str:
    """Get translated string for the current user's language."""
    lang = ctx.user_data.get('lang', 'lang_uk') if ctx and ctx.user_data else 'lang_uk'
    return _t_base(lang, key, **kwargs)
