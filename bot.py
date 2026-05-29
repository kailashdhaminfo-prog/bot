import logging
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
)
from config import BOT_TOKEN
from handlers.start import cmd_start, handle_lang, handle_main_menu
from handlers.life import handle_life, handle_life_category, handle_subcategory
from handlers.yagya import handle_yagya, handle_back_from_yagya, handle_back_from_yagya_to_list
from handlers.packages import handle_packages, handle_package_detail
from handlers.yagya_form import (
    handle_yagya_order, handle_yagya_form_skip,
    handle_yagya_form_text, handle_yagya_form_photo,
)
from handlers.planets import handle_planets, handle_nakshatra, handle_nakshatra_select
from handlers.deities import handle_deities, handle_deity_group
from handlers.practices import handle_practices, handle_rit_dispatch, handle_practice_form_text
from handlers.consultation import (
    handle_consult, handle_consult_request, handle_form_start,
    handle_form_skip, handle_form_text, handle_consult_help,
    handle_consult_unknown, handle_consult_freetext, handle_freetext_message
)
from handlers.all_yagyas import handle_all_yagyas
from handlers.mother import handle_mother, handle_mother_stage, handle_mother_yagya
from handlers.about import handle_about, handle_about_teachers
from handlers.schedule import handle_schedule, handle_schedule_page, handle_event_detail

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def handle_text(update, ctx):
    """Route incoming text messages."""
    # Yagya order form
    if ctx.user_data.get('yf_step') is not None:
        await handle_yagya_form_text(update, ctx)
        return

    # Consultation form field input
    step = ctx.user_data.get('form_step')
    if step is not None:
        await handle_form_text(update, ctx)
        return

    # Practice personal request input
    if ctx.user_data.get('practice_form'):
        await handle_practice_form_text(update, ctx)
        return

    # Free text consultation
    handled = await handle_freetext_message(update, ctx)
    if handled:
        return


async def handle_photo(update, ctx):
    """Route incoming photos and documents (file sent as photo)."""
    if ctx.user_data.get('yf_step') is not None:
        await handle_yagya_form_photo(update, ctx)


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", cmd_start))

    # Language & welcome
    app.add_handler(CallbackQueryHandler(handle_lang, pattern="^lang_"))
    app.add_handler(CallbackQueryHandler(handle_main_menu, pattern="^main_menu$"))

    # Mother & child branch
    app.add_handler(CallbackQueryHandler(handle_mother, pattern="^mother$"))
    app.add_handler(CallbackQueryHandler(handle_mother_stage, pattern="^mstage_"))
    app.add_handler(CallbackQueryHandler(handle_mother_yagya, pattern="^myagya_"))

    # Life branch
    app.add_handler(CallbackQueryHandler(handle_life, pattern="^life$"))
    app.add_handler(CallbackQueryHandler(handle_life_category, pattern="^life_"))
    app.add_handler(CallbackQueryHandler(handle_subcategory, pattern="^sub_"))

    # Yagya form skip (must be before ^yagya_ pattern)
    app.add_handler(CallbackQueryHandler(handle_yagya_form_skip, pattern="^yagya_form_skip_"))

    # Yagya detail
    app.add_handler(CallbackQueryHandler(handle_yagya, pattern="^yagya_"))
    app.add_handler(CallbackQueryHandler(handle_back_from_yagya, pattern="^back_from_yagya$"))
    app.add_handler(CallbackQueryHandler(handle_back_from_yagya_to_list, pattern="^back_from_yagya_to_list$"))

    # Packages
    app.add_handler(CallbackQueryHandler(handle_packages, pattern="^packages$"))
    app.add_handler(CallbackQueryHandler(handle_package_detail, pattern="^pkg_"))
    app.add_handler(CallbackQueryHandler(handle_yagya_order, pattern="^order_"))

    # Planets & Nakshatra
    app.add_handler(CallbackQueryHandler(handle_planets, pattern="^planets$"))
    app.add_handler(CallbackQueryHandler(handle_nakshatra, pattern="^nakshatra$"))
    app.add_handler(CallbackQueryHandler(handle_nakshatra_select, pattern="^naksh_"))

    # All yagyas
    app.add_handler(CallbackQueryHandler(handle_all_yagyas, pattern="^all_yagyas$"))

    # Deities
    app.add_handler(CallbackQueryHandler(handle_deities, pattern="^deities$"))
    app.add_handler(CallbackQueryHandler(handle_deity_group, pattern="^dgrp_"))

    # Practices section (all_practices = legacy alias from main menu button)
    app.add_handler(CallbackQueryHandler(handle_practices, pattern="^practices$"))
    app.add_handler(CallbackQueryHandler(handle_practices, pattern="^all_practices$"))
    app.add_handler(CallbackQueryHandler(handle_rit_dispatch, pattern="^rit_"))

    # Consultation
    app.add_handler(CallbackQueryHandler(handle_consult, pattern="^consult$"))
    app.add_handler(CallbackQueryHandler(handle_consult_request, pattern="^consult_request$"))
    app.add_handler(CallbackQueryHandler(handle_form_start, pattern="^form_start$"))
    app.add_handler(CallbackQueryHandler(handle_form_skip, pattern="^form_skip_"))
    app.add_handler(CallbackQueryHandler(handle_consult_help, pattern="^consult_help$"))
    app.add_handler(CallbackQueryHandler(handle_consult_unknown, pattern="^consult_unknown$"))
    app.add_handler(CallbackQueryHandler(handle_consult_freetext, pattern="^consult_freetext$"))

    # About
    app.add_handler(CallbackQueryHandler(handle_about, pattern="^about$"))
    app.add_handler(CallbackQueryHandler(handle_about_teachers, pattern="^about_teachers$"))

    # Schedule
    app.add_handler(CallbackQueryHandler(handle_schedule, pattern="^schedule$"))
    app.add_handler(CallbackQueryHandler(handle_schedule_page, pattern="^sched_page_"))
    app.add_handler(CallbackQueryHandler(handle_event_detail, pattern="^evt_"))

    # Text messages — private chats only so bot doesn't react in notification groups
    _private = filters.ChatType.PRIVATE
    app.add_handler(MessageHandler(_private & filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(_private & filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(_private & filters.Document.IMAGE, handle_photo))

    logger.info("Bot started.")
    app.run_polling()


if __name__ == "__main__":
    main()
