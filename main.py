import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- بياناتك الأساسية ---
API_ID = 21226626
API_HASH = "ea1a0c2fa9587a9df2a3325056efe110"
BOT_TOKEN = "8628506847:AAHXZ5rbQvA4BA2CZuf-R-_tt17dqQ3aRRk"
OWNER_ID = 2011675494
MY_ACCOUNT = "ShexSaqar"

app = Client("saqr_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- واجهة البداية (مثل الصورة المطلوبة) ---
@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    text = (
        "السلام عليكم ورحمة الله وبركاته!\n"
        f"@{client.me.username} هو البوت الأكثر تميزاً لمساعدتك في إدارة مجموعتك بكل سهولة و أمان!\n\n"
        "👈 أضفني في مجموعتك ثم قم بمنحي الصلاحيات الكاملة كمشرف لكي أعمل بشكل صحيح.\n\n"
        "📌 ماهي أوامر البوت؟\n"
        "اضغط /help لأعرض لك جميع الأوامر وطريقة عملها."
    )
    
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ أضفني إلى مجموعة ➕", url=f"https://t.me/{client.me.username}?startgroup=true")],
        [InlineKeyboardButton("📝 إعدادات المجموعة ⚙️", callback_data="settings")],
        [InlineKeyboardButton("📢 القناة", url="https://t.me/ybpi1"), 
         InlineKeyboardButton("👥 المجموعة", url="https://t.me/ShexSaqar")], # عدل الروابط كما تحب
        [InlineKeyboardButton("💬 معلومات", callback_data="info"), 
         InlineKeyboardButton("⛑️ الدعم", url=f"https://t.me/{MY_ACCOUNT}")],
        [InlineKeyboardButton("🇸🇦 Languages 🌍", callback_data="lang")]
    ])
    
    await message.reply_text(text, reply_markup=markup)

# --- معالجة الضغط على الأزرار ---
@app.on_callback_query()
async def callback_handler(client, query):
    if query.data == "lang":
        # واجهة اختيار اللغات
        lang_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("العربية 🇸🇦", callback_data="set_ar"),
             InlineKeyboardButton("English 🇺🇸", callback_data="set_en")],
            [InlineKeyboardButton("Kurdî ☀️", callback_data="set_ku"),
             InlineKeyboardButton("Türkçe 🇹🇷", callback_data="set_tr")],
            [InlineKeyboardButton("رجوع للخلف ↩️", callback_data="back_home")]
        ])
        await query.message.edit_text("الرجاء اختيار اللغة المناسبة لك:\nPlease choose your language:", reply_markup=lang_markup)
    
    elif query.data == "back_home":
        # العودة للواجهة الرئيسية
        await start(client, query.message)
    
    # يمكنك إضافة استجابة لكل لغة هنا
    elif query.data.startswith("set_"):
        await query.answer("تم حفظ إعدادات اللغة بنجاح!", show_alert=True)

app.run()
