from telegram import (
    Update,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import asyncio

# ================= TOKEN =================
TOKEN = "8528647202:AAHrcOe4Zg6lAaxQweqxiVqljXMuqsD6da8"

# ================= STATES =================
(
    TIL,
    MINTQA,
    MENU,
    TUR,
    TARGET_ID,
    MATN,
    VAQT,
    QAYTA,
    LIST_TYPE,
    TAHRIR_ID,
    TAHRIR_TURI,
    TAHRIR_KIRITISH,
) = range(12)

# Ma'lumotlarni saqlash
users = {}

# ================= TEXTS =================
TEXTS = {
    "O‘zbekcha": {
        "welcome": "👋 Assalomu alaykum!",
        "menu": "📌 Asosiy menyu",
        "new_rem": "➕ Yangi eslatma",
        "list": "📋 Ro‘yxat",
        "back": "⬅️ Orqaga",
        "type_select": "🔔 Eslatma turini tanlang",
        "personal": "👤 Shaxsiy",
        "group": "👥 Guruh",
        "channel": "📢 Kanal",
        "target_id": "🆔 Guruh/Kanal ID yoki @username kiriting",
        "time_format": "⏰ Vaqtni kiriting (DD.MM.YYYY HH:MM)\nMisol: 25.01.2026 18:30",
        "input_text": "✏️ Eslatma matnini kiriting",
        "repeat": "🔁 Takrorlanishni tanlang yoki necha soatda takrorlanishini raqam bilan yozing (masalan: 2)",
        "saved": "✅ Eslatma saqlandi",
        "empty": "📭 Ushbu bo'limda eslatmalar yo‘q",
        "edit_list": "✏️ Tahrirlash uchun eslatmani tanlang:",
        "edit_menu": "⚙️ Boshqarish\n\nHolat: {status}\nMatn: {text}\nVaqt: {time}\nTakror: {rep}",
        "edit_val": "Yangi qiymatni kiriting",
        "error_fmt": "❌ Format noto‘g‘ri, qayta urinib ko'ring",
        "error_region": "❌ Mintaqa topilmadi",
        "region_ask": "🌍 Mintaqangizni yozing (masalan: Tashkent)",
        "btn_text": "📝 Matn",
        "btn_time": "⏰ Vaqt",
        "btn_rep": "🔁 Takrorlash",
        "btn_del": "🗑 O‘chirish",
        "btn_on": "✅ Yoqish (Faol qiling)",
        "btn_off": "💤 O'chirish (Nofaol qiling)",
        "active": "✅ Faol",
        "inactive": "💤 Nofaol",
        "never": "Hech qachon"
    },
    "Русский": {
        "welcome": "👋 Здравствуйте!",
        "menu": "📌 Главное меню",
        "new_rem": "➕ Новое напоминание",
        "list": "📋 Список",
        "back": "⬅️ Назад",
        "type_select": "🔔 Выберите тип",
        "personal": "👤 Личное",
        "group": "👥 Группа",
        "channel": "📢 Канал",
        "target_id": "🆔 Введите ID или @username",
        "time_format": "⏰ Введите дату (DD.MM.YYYY HH:MM)",
        "input_text": "✏️ Введите текст",
        "repeat": "🔁 Выберите интервал или введите числом в часах (например: 2)",
        "saved": "✅ Сохранено",
        "empty": "📭 Пусто",
        "edit_list": "✏️ Выберите напоминание:",
        "edit_menu": "⚙️ Управление\n\nСтатус: {status}\nТекст: {text}\nВремя: {time}\nПовтор: {rep}",
        "edit_val": "Введите новое значение",
        "error_fmt": "❌ Ошибка формата",
        "error_region": "❌ Регион не найден",
        "region_ask": "🌍 Ваш регион (напр: Tashkent)",
        "btn_text": "📝 Текст",
        "btn_time": "⏰ Время",
        "btn_rep": "🔁 Повтор",
        "btn_del": "🗑 Удалить",
        "btn_on": "✅ Включить",
        "btn_off": "💤 Выключить",
        "active": "✅ Активен",
        "inactive": "💤 Выключен",
        "never": "Никогда"
    }
}

ZONE_MAP = {
    "toshkent": "Asia/Tashkent",
    "tashkent": "Asia/Tashkent",
    "ташкент": "Asia/Tashkent",

    "moskva": "Europe/Moscow",
    "moscow": "Europe/Moscow",
    "москва": "Europe/Moscow",

    "samarqand": "Asia/Tashkent",
    "samarkand": "Asia/Tashkent",
    "самарканд": "Asia/Tashkent",

    "buxoro": "Asia/Tashkent",
    "bukhara": "Asia/Tashkent",
    "бухара": "Asia/Tashkent",

    "andijon": "Asia/Tashkent",
    "andijan": "Asia/Tashkent",
    "андижан": "Asia/Tashkent",

    "fargona": "Asia/Tashkent",
    "fergana": "Asia/Tashkent",
    "фергана": "Asia/Tashkent",

    "namangan": "Asia/Tashkent",
    "наманган": "Asia/Tashkent",

    "nukus": "Asia/Tashkent",
    "нукус": "Asia/Tashkent",

    "almata": "Asia/Almaty",
    "almaty": "Asia/Almaty",
    "алматы": "Asia/Almaty",

    "bishkek": "Asia/Bishkek",
    "бишкек": "Asia/Bishkek",

    "dushanbe": "Asia/Dushanbe",
    "душанбе": "Asia/Dushanbe",

    "ashgabat": "Asia/Ashgabat",
    "ашхабад": "Asia/Ashgabat",

    "baku": "Asia/Baku",
    "бакy": "Asia/Baku",

    "istanbul": "Europe/Istanbul",
    "стамбул": "Europe/Istanbul",

    "dubai": "Asia/Dubai",
    "дубай": "Asia/Dubai",

    "tehran": "Asia/Tehran",
    "тегеран": "Asia/Tehran",

    "pekin": "Asia/Shanghai",
    "beijing": "Asia/Shanghai",
    "пекин": "Asia/Shanghai",

    "tokyo": "Asia/Tokyo",
    "токио": "Asia/Tokyo",

    "seul": "Asia/Seoul",
    "seoul": "Asia/Seoul",
    "сеул": "Asia/Seoul",

    "newyork": "America/New_York",
    "ny": "America/New_York",
    "нью-йорк": "America/New_York"
}


# Siz xohlagan takrorlanishlar
REPEAT_OPTIONS = {
    "O‘zbekcha": {
        "Hech qachon": None,
        "Har kuni": timedelta(days=1),
        "Har 2 kunda": timedelta(days=2),
        "Har hafta": timedelta(weeks=1),
        "Har oy": timedelta(days=30),
        "Choraklik (3 oy)": timedelta(days=90),
        "Har 6 oyda": timedelta(days=180),
        "Har yili": timedelta(days=365)
    },
    "Русский": {
        "Никогда": None,
        "Каждый день": timedelta(days=1),
        "Раз в 2 дня": timedelta(days=2),
        "Каждую неделю": timedelta(weeks=1),
        "Каждый месяц": timedelta(days=30),
        "Квартал (3 мес)": timedelta(days=90),
        "Раз в 6 месяцев": timedelta(days=180),
        "Каждый год": timedelta(days=365)
    }
}

def parse_chat_id(text: str):
    text = text.strip()
    if "t.me/" in text: return "@" + text.split("/")[-1]
    if text.startswith("@") or text.startswith("-100"): return text
    try: return int(text)
    except: return None

# ================= HANDLERS =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid not in users:
        users[uid] = {"reminders": [], "tz": None, "lang": None}
    await update.message.reply_text("Tilni tanlang / Выберите язык:", 
        reply_markup=ReplyKeyboardMarkup([["O‘zbekcha", "Русский"]], resize_keyboard=True))
    return TIL

async def change_lang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return await start(update, context)

async def til(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    lang = update.message.text
    if lang not in ["O‘zbekcha", "Русский"]: return TIL
    users[uid]["lang"] = lang
    if users[uid].get("tz"):
        return await menu(update, context)
    await update.message.reply_text(TEXTS[lang]["region_ask"], reply_markup=ReplyKeyboardRemove())
    return MINTQA

async def mintqa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    lang = users[uid]["lang"]
    text = update.message.text.lower()
    if text in ZONE_MAP:
        users[uid]["tz"] = ZoneInfo(ZONE_MAP[text])
        return await menu(update, context)
    await update.message.reply_text(TEXTS[lang]["error_region"])
    return MINTQA

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    lang = users[uid].get("lang", "O‘zbekcha")
    kb = [[TEXTS[lang]["new_rem"]], [TEXTS[lang]["list"]]]
    await update.message.reply_text(TEXTS[lang]["menu"], reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True))
    return MENU

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    lang = users[uid]["lang"]
    text = update.message.text
    if text == TEXTS[lang]["new_rem"]:
        kb = [[TEXTS[lang]["personal"]], [TEXTS[lang]["group"], TEXTS[lang]["channel"]], [TEXTS[lang]["back"]]]
        await update.message.reply_text(TEXTS[lang]["type_select"], reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True))
        return TUR
    elif text == TEXTS[lang]["list"]:
        kb = [[TEXTS[lang]["personal"]], [TEXTS[lang]["group"], TEXTS[lang]["channel"]], [TEXTS[lang]["back"]]]
        await update.message.reply_text(TEXTS[lang]["type_select"], reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True))
        return LIST_TYPE
    return MENU

async def tur(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    lang = users[uid]["lang"]
    text = update.message.text
    if text == TEXTS[lang]["back"]: return await menu(update, context)
    mapping = {TEXTS[lang]["personal"]: "private", TEXTS[lang]["group"]: "group", TEXTS[lang]["channel"]: "channel"}
    if text not in mapping: return TUR
    users[uid]["current"] = {"type": mapping[text], "is_active": True, "id": datetime.now().timestamp()}
    if mapping[text] != "private":
        await update.message.reply_text(TEXTS[lang]["target_id"], reply_markup=ReplyKeyboardMarkup([[TEXTS[lang]["back"]]], resize_keyboard=True))
        return TARGET_ID
    await update.message.reply_text(TEXTS[lang]["input_text"], reply_markup=ReplyKeyboardMarkup([[TEXTS[lang]["back"]]], resize_keyboard=True))
    return MATN

async def target_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    lang = users[uid]["lang"]
    if update.message.text == TEXTS[lang]["back"]: return await menu(update, context)
    cid = parse_chat_id(update.message.text)
    if cid is None: return TARGET_ID
    users[uid]["current"]["target_id"] = cid
    await update.message.reply_text(TEXTS[lang]["input_text"])
    return MATN

async def matn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    lang = users[uid]["lang"]
    if update.message.text == TEXTS[lang]["back"]: return await menu(update, context)
    users[uid]["current"]["text"] = update.message.text
    await update.message.reply_text(TEXTS[lang]["time_format"])
    return VAQT

async def vaqt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    lang = users[uid]["lang"]
    if update.message.text == TEXTS[lang]["back"]: return await menu(update, context)
    try:
        dt = datetime.strptime(update.message.text, "%d.%m.%Y %H:%M").replace(tzinfo=users[uid]["tz"])
        if dt < datetime.now(users[uid]["tz"]):
            await update.message.reply_text("❌ O'tib ketgan vaqt!")
            return VAQT
        users[uid]["current"]["time"] = dt
        opts = REPEAT_OPTIONS[lang]
        # Faqat sizning variantlaringiz qoldi
        kb = [list(opts.keys())[i:i+2] for i in range(0, len(opts), 2)]
        kb.append([TEXTS[lang]["back"]])
        await update.message.reply_text(TEXTS[lang]["repeat"], reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True))
        return QAYTA
    except:
        await update.message.reply_text(TEXTS[lang]["error_fmt"])
        return VAQT

async def qayta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    lang = users[uid]["lang"]
    text = update.message.text
    if text == TEXTS[lang]["back"]: return await menu(update, context)
    
    rep_delta = REPEAT_OPTIONS[lang].get(text, "CUSTOM")
    if rep_delta == "CUSTOM":
        try:
            # Foydalanuvchi "2" yozsa, bu 2 soat deb olinadi
            rep_delta = timedelta(hours=float(text))
        except ValueError:
            await update.message.reply_text(TEXTS[lang]["error_fmt"])
            return QAYTA

    cur = users[uid]["current"]
    cur["repeat"] = rep_delta
    new_rem = {**cur}
    new_rem["task"] = asyncio.create_task(reminder_scheduler(uid, new_rem, context))
    users[uid]["reminders"].append(new_rem)
    users[uid].pop("current", None)
    await update.message.reply_text(TEXTS[lang]["saved"])
    return await menu(update, context)

# ... (qolgan list_type, tahrir_id, send_edit_menu, tahrir_turi kabi funksiyalar avvalgidek qoladi)

async def list_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    lang = users[uid]["lang"]
    text = update.message.text
    if text == TEXTS[lang]["back"]: return await menu(update, context)
    mapping = {TEXTS[lang]["personal"]: "private", TEXTS[lang]["group"]: "group", TEXTS[lang]["channel"]: "channel"}
    turi = mapping.get(text)
    if not turi: return LIST_TYPE
    filtered = [r for r in users[uid]["reminders"] if r["type"] == turi]
    if not filtered:
        await update.message.reply_text(TEXTS[lang]["empty"])
        return await menu(update, context)
    buttons = [[f"{r['text']} | {r['time'].strftime('%H:%M')}"] for r in filtered]
    buttons.append([TEXTS[lang]["back"]])
    await update.message.reply_text(TEXTS[lang]["edit_list"], reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True))
    return TAHRIR_ID

async def tahrir_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    lang = users[uid]["lang"]
    user_input = update.message.text
    if user_input == TEXTS[lang]["back"]: return await menu(update, context)
    for r in users[uid]["reminders"]:
        if f"{r['text']} | {r['time'].strftime('%H:%M')}" == user_input:
            users[uid]["edit_target"] = r
            break
    else: return TAHRIR_ID
    return await send_edit_menu(update, context)

async def send_edit_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    lang = users[uid]["lang"]
    r = users[uid]["edit_target"]
    status = TEXTS[lang]["active"] if r.get("is_active", True) else TEXTS[lang]["inactive"]
    toggle_btn = TEXTS[lang]["btn_off"] if r.get("is_active", True) else TEXTS[lang]["btn_on"]
    
    rep_label = TEXTS[lang]["never"]
    if r['repeat']:
        if r['repeat'].days >= 1:
            rep_label = f"{r['repeat'].days} kun"
        else:
            rep_label = f"{r['repeat'].total_seconds()/3600:.1f} soat"

    msg = TEXTS[lang]["edit_menu"].format(status=status, text=r['text'], time=r['time'].strftime('%d.%m.%Y %H:%M'), rep=rep_label)
    kb = [[TEXTS[lang]["btn_text"], TEXTS[lang]["btn_time"]], [TEXTS[lang]["btn_rep"], toggle_btn], [TEXTS[lang]["btn_del"]], [TEXTS[lang]["back"]]]
    await update.message.reply_text(msg, reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True))
    return TAHRIR_TURI

async def tahrir_turi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    lang = users[uid]["lang"]
    choice = update.message.text
    r = users[uid].get("edit_target")
    if choice == TEXTS[lang]["back"]: return await menu(update, context)
    if choice == TEXTS[lang]["btn_del"]:
        r["task"].cancel()
        users[uid]["reminders"].remove(r)
        return await menu(update, context)
    if choice in [TEXTS[lang]["btn_on"], TEXTS[lang]["btn_off"]]:
        r["is_active"] = not r.get("is_active", True)
        return await send_edit_menu(update, context)
    
    users[uid]["edit_mode"] = choice
    if choice == TEXTS[lang]["btn_rep"]:
        opts = REPEAT_OPTIONS[lang]
        kb = [list(opts.keys())[i:i+2] for i in range(0, len(opts), 2)]
        kb.append([TEXTS[lang]["back"]])
        await update.message.reply_text(TEXTS[lang]["repeat"], reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True))
    else:
        await update.message.reply_text(TEXTS[lang]["edit_val"], reply_markup=ReplyKeyboardRemove())
    return TAHRIR_KIRITISH

async def tahrir_kirit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    lang = users[uid]["lang"]
    r = users[uid]["edit_target"]
    mode = users[uid]["edit_mode"]
    text = update.message.text
    try:
        if mode == TEXTS[lang]["btn_time"]:
            r["time"] = datetime.strptime(text, "%d.%m.%Y %H:%M").replace(tzinfo=users[uid]["tz"])
        elif mode == TEXTS[lang]["btn_rep"]:
            rep_delta = REPEAT_OPTIONS[lang].get(text, "CUSTOM")
            if rep_delta == "CUSTOM": rep_delta = timedelta(hours=float(text))
            r["repeat"] = rep_delta
        else:
            r["text"] = text
        
        r["task"].cancel()
        r["task"] = asyncio.create_task(reminder_scheduler(uid, r, context))
        return await menu(update, context)
    except:
        await update.message.reply_text(TEXTS[lang]["error_fmt"])
        return TAHRIR_KIRITISH

async def reminder_scheduler(uid, reminder, context):
    while True:
        try:
            tz = users[uid]["tz"]
            now = datetime.now(tz)
            wait_sec = (reminder["time"] - now).total_seconds()
            
            if wait_sec > 0:
                await asyncio.sleep(wait_sec)
            
            if reminder.get("is_active", True):
                chat_id = uid if reminder["type"] == "private" else reminder["target_id"]
                try:
                    await context.bot.send_message(
                        chat_id=chat_id, 
                        text=f"⏰ **Eslatma**:\n\n{reminder['text']}", 
                        parse_mode="Markdown"
                    )
                except: pass

            if reminder["repeat"]:
                reminder["time"] += reminder["repeat"]
                while reminder["time"] < datetime.now(tz):
                    reminder["time"] += reminder["repeat"]
            else:
                if reminder in users[uid].get("reminders", []):
                    users[uid]["reminders"].remove(reminder)
                break
        except asyncio.CancelledError:
            break
        except:
            await asyncio.sleep(10)

def main():
    app = Application.builder().token(TOKEN).build()
    conv = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            CommandHandler("change_lang", change_lang)
        ],
        states={
            TIL: [CommandHandler("change_lang", change_lang), MessageHandler(filters.TEXT & ~filters.COMMAND, til)],
            MINTQA: [CommandHandler("change_lang", change_lang), MessageHandler(filters.TEXT & ~filters.COMMAND, mintqa)],
            MENU: [CommandHandler("change_lang", change_lang), MessageHandler(filters.TEXT & ~filters.COMMAND, menu_handler)],
            TUR: [CommandHandler("change_lang", change_lang), MessageHandler(filters.TEXT & ~filters.COMMAND, tur)],
            TARGET_ID: [CommandHandler("change_lang", change_lang), MessageHandler(filters.TEXT & ~filters.COMMAND, target_id)],
            MATN: [CommandHandler("change_lang", change_lang), MessageHandler(filters.TEXT & ~filters.COMMAND, matn)],
            VAQT: [CommandHandler("change_lang", change_lang), MessageHandler(filters.TEXT & ~filters.COMMAND, vaqt)],
            QAYTA: [CommandHandler("change_lang", change_lang), MessageHandler(filters.TEXT & ~filters.COMMAND, qayta)],
            LIST_TYPE: [CommandHandler("change_lang", change_lang), MessageHandler(filters.TEXT & ~filters.COMMAND, list_type)],
            TAHRIR_ID: [CommandHandler("change_lang", change_lang), MessageHandler(filters.TEXT & ~filters.COMMAND, tahrir_id)],
            TAHRIR_TURI: [CommandHandler("change_lang", change_lang), MessageHandler(filters.TEXT & ~filters.COMMAND, tahrir_turi)],
            TAHRIR_KIRITISH: [CommandHandler("change_lang", change_lang), MessageHandler(filters.TEXT & ~filters.COMMAND, tahrir_kirit)],
        },
        fallbacks=[CommandHandler("start", start), CommandHandler("change_lang", change_lang)],
        allow_reentry=True
    )
    app.add_handler(conv)
    app.run_polling()

if __name__ == "__main__":
    main()