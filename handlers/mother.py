from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from data.life_map import translate_name
from keyboards import KB_PACKAGES
from utils import send_screen, t


# Yagya lists per stage (language-independent keys)
MOTHER_STAGES = {
    "plan":    ["Сантана Гопала", "Скандамата", "Нага"],
    "preg":    ["Сантана Гопала", "Дханвантарі", "Скандамата"],
    "birth":   ["Дурга", "Маха Мрітюнджая", "Скандамата", "Ганапаті"],
    "newborn": ["Дханвантарі", "Скандамата", "Сарасваті", "Сатья Нараяна", "Пітрі", "Кришна"],
    "name":    ["Сарасваті", "Наваграха", "Ганапаті"],
    "year":    ["Дханвантарі", "Скандамата", "Сарасваті", "Ганапаті"],
}

_STAGE_LABELS = {
    'lang_uk': {
        "plan":    "Плануємо дитину",
        "preg":    "Вагітність",
        "birth":   "Скоро пологи",
        "newborn": "Дитина вже народилась",
        "name":    "Ім'я та доля дитини",
        "year":    "Перший рік життя",
    },
    'lang_ru': {
        "plan":    "Планируем ребёнка",
        "preg":    "Беременность",
        "birth":   "Скоро роды",
        "newborn": "Ребёнок уже родился",
        "name":    "Имя и судьба ребёнка",
        "year":    "Первый год жизни",
    },
    'lang_en': {
        "plan":    "Planning a child",
        "preg":    "Pregnancy",
        "birth":   "Birth approaching",
        "newborn": "The child has been born",
        "name":    "Name and the child's destiny",
        "year":    "First year of life",
    },
}

_MOTHER_INTRO = {
    'lang_uk': (
        "*Яг'ї для матері та дитини*\n\n"
        "_Зачаття, вагітність, пологи, народження, ім'я та перший рік життя_\n\n"
        "Я допоможу підібрати яг'ю для вашого етапу — від підготовки до зачаття "
        "до першого року життя дитини."
    ),
    'lang_ru': (
        "*Ягьи для матери и ребёнка*\n\n"
        "_Зачатие, беременность, роды, рождение, имя и первый год жизни_\n\n"
        "Я помогу подобрать ягью для вашего этапа — от подготовки к зачатию "
        "до первого года жизни ребёнка."
    ),
    'lang_en': (
        "*Yagyas for mother and child*\n\n"
        "_Conception, pregnancy, birth, newborn, name and the first year of life_\n\n"
        "I will help you choose a Yagya for your stage — from preparation for conception "
        "to the first year of the child's life."
    ),
}

_STAGE_TEXTS = {
    'lang_uk': {
        "plan": (
            "Цей розділ підходить парі, яка готується до зачаття і хоче запросити душу дитини "
            "в поле любові, чистого наміру і благословення.\n\n"
            "*Яг'ї для цього етапу:*\n\n"
            "🔥 *Сантана Гопала Яг'я* — для благословення дитини, теми потомства і м'якого "
            "запрошення душі в сім'ю.\n\n"
            "🔥 *Скандамата Яг'я* — для материнського благословення, захисту та м'якої підтримки "
            "на шляху до народження дитини.\n\n"
            "🔥 *Нага Яг'я* — для зняття перешкод, пов'язаних із темою зачаття, і гармонізації "
            "тонкого поля."
        ),
        "preg": (
            "Вагітність — це час, коли жінка стає живим храмом для нової душі. Яг'я допомагає "
            "наповнити цей шлях молитвою, спокоєм, захистом і благословенням.\n\n"
            "*Яг'ї для цього етапу:*\n\n"
            "🔥 *Сантана Гопала Яг'я* — для благословення матері й дитини та м'якої підтримки "
            "вагітності.\n\n"
            "🔥 *Дханвантари Яг'я* — для теми здоров'я, відновлення, життєвої сили та "
            "благополучного проходження цього періоду.\n\n"
            "🔥 *Скандамата Яг'я* — для материнського захисту, м'якості, підтримки і "
            "благословення дитини."
        ),
        "birth": (
            "Пологи — це великий перехід. Яг'я перед пологами допомагає жінці увійти в цей етап "
            "із силою, довірою, молитвою і благословенням.\n\n"
            "*Яг'ї для цього етапу:*\n\n"
            "🔥 *Дурга Яг'я* — для сили матері, захисту і внутрішньої стійкості перед пологами.\n\n"
            "🔥 *Маха Мрітюнджая Яг'я* — для захисту, життєвої сили і благополучного проходження "
            "переходу.\n\n"
            "🔥 *Скандамата Яг'я* — для материнського благословення, захисту і м'якої духовної "
            "підтримки перед народженням дитини.\n\n"
            "🔥 *Ганеша Яг'я* — для усунення перешкод і сприятливого проходження важливого етапу."
        ),
        "newborn": (
            "Після народження важливо подякувати за прихід душі, благословити дитину, підтримати "
            "матір і наповнити дім світлом та спокоєм.\n\n"
            "*Яг'ї для цього етапу:*\n\n"
            "🔥 *Дханвантари Яг'я* — для теми здоров'я, відновлення і життєвої сили дитини.\n\n"
            "🔥 *Скандамата Яг'я* — для благословення матері й дитини, м'якого материнського "
            "захисту і підтримки.\n\n"
            "🔥 *Сарасваті Яг'я* — для чистого розвитку, світлого простору і благословення на "
            "зростання дитини.\n\n"
            "🔥 *Сатья Нараяна Яг'я* — для сімейної гармонії, благополуччя і праведного "
            "сімейного шляху.\n\n"
            "🔥 *Пітрі Яг'я* — для зв'язку з родом, шани до предків і підтримки родової лінії.\n\n"
            "🔥 *Кришна Яг'я* — для любові, м'якості, радості та гармонії у стосунках."
        ),
        "name": (
            "Ім'я — це перший звук, яким сім'я звертається до душі дитини. Через ім'я дитина "
            "отримує вібрацію, образ і благословення шляху.\n\n"
            "*Яг'ї для цього етапу:*\n\n"
            "🔥 *Сарасваті Яг'я* — для чистоти імені, мови, знання і благого звуку.\n\n"
            "🔥 *Наваграха Яг'я* — для гармонізації планетарного поля і підтримки долі дитини.\n\n"
            "🔥 *Ганапаті Яг'я* — для благословення початку шляху і усунення перешкод."
        ),
        "year": (
            "У перший рік життя дитина вчиться відчуттю світу: тут мене люблять, тут мене "
            "бережуть, тут мені раді. Яг'я допомагає сім'ї створити поле здоров'я, росту і "
            "благословення.\n\n"
            "*Яг'ї для цього етапу:*\n\n"
            "🔥 *Дханвантари Яг'я* — для здоров'я, життєвої сили і підтримки розвитку дитини.\n\n"
            "🔥 *Скандамата Яг'я* — для материнського благословення, захисту і м'якого супроводу "
            "першого року життя.\n\n"
            "🔥 *Сарасваті Яг'я* — для світлого розвитку, чистоти сприйняття і благословення на "
            "ріст.\n\n"
            "🔥 *Ганапаті Яг'я* — для захисту, сприятливого початку і благословення шляху."
        ),
    },
    'lang_ru': {
        "plan": (
            "Этот раздел подходит паре, которая готовится к зачатию и хочет пригласить душу "
            "ребёнка в поле любви, чистого намерения и благословения.\n\n"
            "*Ягьи для этого этапа:*\n\n"
            "🔥 *Сантана Гопала Ягья* — для благословения ребёнка, темы потомства и мягкого "
            "приглашения души в семью.\n\n"
            "🔥 *Скандамата Ягья* — для материнского благословения, защиты и мягкой поддержки "
            "на пути к рождению ребёнка.\n\n"
            "🔥 *Нага Ягья* — для снятия препятствий, связанных с темой зачатия, и гармонизации "
            "тонкого поля."
        ),
        "preg": (
            "Беременность — это время, когда женщина становится живым храмом для новой души. "
            "Ягья помогает наполнить этот путь молитвой, спокойствием, защитой и благословением.\n\n"
            "*Ягьи для этого этапа:*\n\n"
            "🔥 *Сантана Гопала Ягья* — для благословения матери и ребёнка и мягкой поддержки "
            "беременности.\n\n"
            "🔥 *Дханвантари Ягья* — для темы здоровья, восстановления, жизненной силы и "
            "благополучного прохождения этого периода.\n\n"
            "🔥 *Скандамата Ягья* — для материнской защиты, мягкости, поддержки и благословения "
            "ребёнка."
        ),
        "birth": (
            "Роды — это великий переход. Ягья перед родами помогает женщине войти в этот этап "
            "с силой, доверием, молитвой и благословением.\n\n"
            "*Ягьи для этого этапа:*\n\n"
            "🔥 *Дурга Ягья* — для силы матери, защиты и внутренней стойкости перед родами.\n\n"
            "🔥 *Маха Мритьюнджая Ягья* — для защиты, жизненной силы и благополучного "
            "прохождения перехода.\n\n"
            "🔥 *Скандамата Ягья* — для материнского благословения, защиты и мягкой духовной "
            "поддержки перед рождением ребёнка.\n\n"
            "🔥 *Ганеша Ягья* — для устранения препятствий и благоприятного прохождения "
            "важного этапа."
        ),
        "newborn": (
            "После рождения важно поблагодарить за приход души, благословить ребёнка, "
            "поддержать мать и наполнить дом светом и покоем.\n\n"
            "*Ягьи для этого этапа:*\n\n"
            "🔥 *Дханвантари Ягья* — для темы здоровья, восстановления и жизненной силы "
            "ребёнка.\n\n"
            "🔥 *Скандамата Ягья* — для благословения матери и ребёнка, мягкой материнской "
            "защиты и поддержки.\n\n"
            "🔥 *Сарасвати Ягья* — для чистого развития, светлого пространства и благословения "
            "на рост ребёнка.\n\n"
            "🔥 *Сатья Нараяна Ягья* — для семейной гармонии, благополучия и праведного "
            "семейного пути.\n\n"
            "🔥 *Питри Ягья* — для связи с родом, почитания предков и поддержки родовой "
            "линии.\n\n"
            "🔥 *Кришна Ягья* — для любви, мягкости, радости и гармонии в отношениях."
        ),
        "name": (
            "Имя — это первый звук, которым семья обращается к душе ребёнка. Через имя ребёнок "
            "получает вибрацию, образ и благословение пути.\n\n"
            "*Ягьи для этого этапа:*\n\n"
            "🔥 *Сарасвати Ягья* — для чистоты имени, речи, знания и благого звука.\n\n"
            "🔥 *Наваграха Ягья* — для гармонизации планетарного поля и поддержки судьбы "
            "ребёнка.\n\n"
            "🔥 *Ганапати Ягья* — для благословения начала пути и устранения препятствий."
        ),
        "year": (
            "В первый год жизни ребёнок учится ощущению мира: здесь меня любят, здесь меня "
            "берегут, здесь мне рады. Ягья помогает семье создать поле здоровья, роста и "
            "благословения.\n\n"
            "*Ягьи для этого этапа:*\n\n"
            "🔥 *Дханвантари Ягья* — для здоровья, жизненной силы и поддержки развития "
            "ребёнка.\n\n"
            "🔥 *Скандамата Ягья* — для материнского благословения, защиты и мягкого "
            "сопровождения первого года жизни.\n\n"
            "🔥 *Сарасвати Ягья* — для светлого развития, чистоты восприятия и благословения "
            "на рост.\n\n"
            "🔥 *Ганапати Ягья* — для защиты, благоприятного начала и благословения пути."
        ),
    },
    'lang_en': {
        "plan": (
            "This section is for couples preparing for conception who wish to invite the soul of a "
            "child into a field of love, pure intention and blessing.\n\n"
            "*Yagyas for this stage:*\n\n"
            "🔥 *Santana Gopala Yagya* — for blessing the child, the theme of offspring and gently "
            "inviting the soul into the family.\n\n"
            "🔥 *Skandamata Yagya* — for maternal blessing, protection and gentle support on the "
            "path to the birth of a child.\n\n"
            "🔥 *Naga Yagya* — for removing obstacles related to conception and harmonising the "
            "subtle field."
        ),
        "preg": (
            "Pregnancy is a time when a woman becomes a living temple for a new soul. Yagya helps "
            "fill this journey with prayer, calm, protection and blessing.\n\n"
            "*Yagyas for this stage:*\n\n"
            "🔥 *Santana Gopala Yagya* — for blessing the mother and child and gently supporting "
            "the pregnancy.\n\n"
            "🔥 *Dhanvantari Yagya* — for health, recovery, vitality and a smooth passage through "
            "this period.\n\n"
            "🔥 *Skandamata Yagya* — for maternal protection, gentleness, support and blessing of "
            "the child."
        ),
        "birth": (
            "Childbirth is a great transition. A yagya before labour helps the woman enter this "
            "stage with strength, trust, prayer and blessing.\n\n"
            "*Yagyas for this stage:*\n\n"
            "🔥 *Durga Yagya* — for the mother's strength, protection and inner steadiness before "
            "childbirth.\n\n"
            "🔥 *Maha Mrityunjaya Yagya* — for protection, vitality and a safe passage through "
            "the transition.\n\n"
            "🔥 *Skandamata Yagya* — for maternal blessing, protection and gentle spiritual "
            "support before the birth of the child.\n\n"
            "🔥 *Ganesha Yagya* — for removing obstacles and ensuring a favourable passage through "
            "this important stage."
        ),
        "newborn": (
            "After the birth it is important to give thanks for the arrival of the soul, bless the "
            "child, support the mother and fill the home with light and peace.\n\n"
            "*Yagyas for this stage:*\n\n"
            "🔥 *Dhanvantari Yagya* — for the health, recovery and vitality of the child.\n\n"
            "🔥 *Skandamata Yagya* — for blessing the mother and child, gentle maternal protection "
            "and support.\n\n"
            "🔥 *Sarasvati Yagya* — for pure development, a bright space and a blessing for the "
            "child's growth.\n\n"
            "🔥 *Satya Narayana Yagya* — for family harmony, wellbeing and a righteous family "
            "path.\n\n"
            "🔥 *Pitri Yagya* — for connection with the lineage, reverence for ancestors and "
            "support of the ancestral line.\n\n"
            "🔥 *Krishna Yagya* — for love, gentleness, joy and harmony in relationships."
        ),
        "name": (
            "A name is the first sound by which the family addresses the soul of the child. "
            "Through the name the child receives a vibration, an image and a blessing for the "
            "path.\n\n"
            "*Yagyas for this stage:*\n\n"
            "🔥 *Sarasvati Yagya* — for the purity of the name, speech, knowledge and auspicious "
            "sound.\n\n"
            "🔥 *Navagraha Yagya* — for harmonising the planetary field and supporting the "
            "child's destiny.\n\n"
            "🔥 *Ganapati Yagya* — for blessing the beginning of the path and removing obstacles."
        ),
        "year": (
            "In the first year of life a child learns to feel: I am loved here, I am cared for "
            "here, I am welcome here. Yagya helps the family create a field of health, growth and "
            "blessing.\n\n"
            "*Yagyas for this stage:*\n\n"
            "🔥 *Dhanvantari Yagya* — for the health, vitality and developmental support of the "
            "child.\n\n"
            "🔥 *Skandamata Yagya* — for maternal blessing, protection and gentle accompaniment "
            "through the first year of life.\n\n"
            "🔥 *Sarasvati Yagya* — for bright development, purity of perception and a blessing "
            "for growth.\n\n"
            "🔥 *Ganapati Yagya* — for protection, an auspicious beginning and a blessing for "
            "the path."
        ),
    },
}


def _get_text(stage_key: str, lang: str) -> str:
    texts = _STAGE_TEXTS.get(lang) or _STAGE_TEXTS['lang_uk']
    return texts.get(stage_key, "")


def _stage_kb(stage_key: str, lang: str, ctx) -> InlineKeyboardMarkup:
    yagyas = MOTHER_STAGES[stage_key]
    rows = [
        [InlineKeyboardButton(f"🔥 {translate_name(y, lang)}", callback_data=f"myagya_{y}")]
        for y in yagyas
    ]
    rows.append([InlineKeyboardButton(t(ctx, 'consult_help_btn'), callback_data="consult")])
    rows.append([InlineKeyboardButton(t(ctx, 'btn_back'), callback_data="mother")])
    return InlineKeyboardMarkup(rows)


async def handle_mother(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    lang = ctx.user_data.get('lang', 'lang_uk')
    text = _MOTHER_INTRO.get(lang, _MOTHER_INTRO['lang_uk'])
    labels = _STAGE_LABELS.get(lang, _STAGE_LABELS['lang_uk'])

    rows = [
        [InlineKeyboardButton(label, callback_data=f"mstage_{key}")]
        for key, label in labels.items()
    ]
    rows.append([InlineKeyboardButton(t(ctx, 'btn_back'), callback_data="main_menu")])
    await send_screen(q, text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(rows))


async def handle_mother_stage(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    stage_key = q.data.replace("mstage_", "")
    if stage_key not in MOTHER_STAGES:
        return

    ctx.user_data['back_source'] = 'mother'
    ctx.user_data['mother_stage'] = stage_key
    lang = ctx.user_data.get('lang', 'lang_uk')

    await send_screen(
        q, _get_text(stage_key, lang), parse_mode="Markdown",
        reply_markup=_stage_kb(stage_key, lang, ctx)
    )


async def handle_mother_yagya(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    """Yagya tap from mother branch → show packages immediately, no detail card."""
    q = update.callback_query
    await q.answer()

    yagya_name = q.data.replace("myagya_", "")
    ctx.user_data['current_yagya'] = yagya_name
    ctx.user_data['back_source'] = 'mother'
    lang = ctx.user_data.get('lang', 'lang_uk')

    yagya_display = translate_name(yagya_name, lang)
    text = t(ctx, 'packages_choose_for', yagya=yagya_display)
    text += '\n' + t(ctx, 'packages_hryvnia')
    await send_screen(q, text, parse_mode="Markdown", reply_markup=KB_PACKAGES(lang))


def mother_stage_screen(stage_key: str, lang: str, ctx) -> tuple[str, InlineKeyboardMarkup]:
    """Return (text, keyboard) for a stage — used by back-navigation."""
    return _get_text(stage_key, lang), _stage_kb(stage_key, lang, ctx)
