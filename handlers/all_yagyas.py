import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from data.life_map import translate_name
from data.strings import t as _st
from utils import send_screen, t

ALL_YAGYAS = [
    "Ганапаті", "Шіва", "Маха Мрітюнджая", "Картікея", "Хануман", "Кала Бхайрава",
    "Вішну", "Нарасімха", "Рама", "Кришна", "Венкатешвара", "Сатья Нараяна",
    "Дханвантарі", "Сударшана", "Сантана Гопала", "Лакшмі", "Кубера", "Сарасваті",
    "Дурга", "Дхумаваті", "Чанді", "Лаліта", "Калі", "Тара", "Шіва-Парваті",
    "Савітрі-Гаятрі", "Наваграха", "Брихаспаті", "Мангала", "Шані", "Будха",
    "Даттатрея", "Саптаріші", "В'яса", "Нага", "Пітрі", "Чандра",
    "Кету", "Панчамукті Ганапаті", "Скандамата", "Дас Махавідья", "Брахма",
    "Ямараджа", "Вішвакарма", "Шукра", "Раху", "Сур'я", "Багаламукхі",
]

_BATCHES = [ALL_YAGYAS[0:12], ALL_YAGYAS[12:24], ALL_YAGYAS[24:36], ALL_YAGYAS[36:]]


def _batch_kb(batch: list, lang: str, add_back: bool) -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(f"🔥 {translate_name(y, lang)}", callback_data=f"yagya_{y}")]
        for y in batch
    ]
    if add_back:
        rows.append([InlineKeyboardButton(_st(lang, 'btn_back'), callback_data="main_menu")])
    return InlineKeyboardMarkup(rows)


async def handle_all_yagyas(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    lang = ctx.user_data.get('lang', 'lang_uk')
    ctx.user_data['back_source'] = None

    header = _st(lang, 'btn_all_yagyas')
    cont = _st(lang, 'all_yagyas_cont')

    await send_screen(q, header, reply_markup=_batch_kb(_BATCHES[0], lang, False))

    for i, batch in enumerate(_BATCHES[1:], start=1):
        await asyncio.sleep(0.5)
        is_last = (i == len(_BATCHES) - 1)
        await q.message.reply_text(
            cont,
            reply_markup=_batch_kb(batch, lang, is_last),
        )
