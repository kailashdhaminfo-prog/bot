from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from data.schedule import EVENTS, EVENTS_PER_PAGE
from utils import send_screen, t


def _events_keyboard(page: int, ctx) -> InlineKeyboardMarkup:
    start = page * EVENTS_PER_PAGE
    chunk = EVENTS[start:start + EVENTS_PER_PAGE]

    rows = []
    for evt in chunk:
        rows.append([InlineKeyboardButton(
            f"📅 {evt['name']} — {evt['date']} {evt['time']}",
            callback_data=f"evt_{evt['id']}"
        )])

    nav = []
    if start + EVENTS_PER_PAGE < len(EVENTS):
        nav.append(InlineKeyboardButton(t(ctx, 'btn_more_dates'), callback_data=f"sched_page_{page + 1}"))
    if page > 0:
        nav.append(InlineKeyboardButton(t(ctx, 'btn_back_list'), callback_data=f"sched_page_{page - 1}"))
    if nav:
        rows.append(nav)

    rows.append([InlineKeyboardButton(t(ctx, 'btn_back'), callback_data="main_menu")])
    return InlineKeyboardMarkup(rows)


async def handle_schedule(update: Update, ctx: ContextTypes.DEFAULT_TYPE, from_start: bool = False):
    ctx.user_data['sched_page'] = 0
    if from_start:
        await update.message.reply_text(t(ctx, 'schedule_prompt'), reply_markup=_events_keyboard(0, ctx))
        return
    q = update.callback_query
    await q.answer()
    await send_screen(q, t(ctx, 'schedule_prompt'), reply_markup=_events_keyboard(0, ctx))


async def handle_schedule_page(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    page = int(q.data.replace("sched_page_", ""))
    ctx.user_data['sched_page'] = page
    await send_screen(q, t(ctx, 'schedule_prompt'), reply_markup=_events_keyboard(page, ctx))


async def handle_event_detail(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    evt_id = q.data.replace("evt_", "")
    evt = next((e for e in EVENTS if e["id"] == evt_id), None)
    if not evt:
        return

    ctx.user_data['current_event'] = evt_id
    ctx.user_data['back_source'] = 'schedule'
    page = ctx.user_data.get('sched_page', 0)

    text = (
        f"*{evt['name']}*\n\n"
        f"{t(ctx, 'schedule_date')} {evt['date']}\n"
        f"{t(ctx, 'schedule_time')} {evt['time']}\n"
        f"{t(ctx, 'schedule_price')} {evt['price']}\n"
        f"_{t(ctx, 'schedule_hryvnia_note')}_"
    )

    rows = [[InlineKeyboardButton(t(ctx, 'schedule_pay_btn'), url=evt["payment_url"])]]
    if evt.get("pkg_key"):
        rows.append([InlineKeyboardButton(t(ctx, 'schedule_order_btn'), callback_data=f"order_{evt['pkg_key']}")])
    if evt.get("yagya_key"):
        rows.append([InlineKeyboardButton(t(ctx, 'schedule_practice_btn'), callback_data=f"yagya_{evt['yagya_key']}")])
    rows.append([InlineKeyboardButton(t(ctx, 'schedule_consult_btn'), callback_data="consult")])
    rows.append([InlineKeyboardButton(t(ctx, 'btn_back'), callback_data=f"sched_page_{page}")])

    await send_screen(q, text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(rows))
