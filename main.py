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

# --- واجهة المساعدة الرئيسية ---
@app.on_message(filters.command("help"))
async def help_menu(client, message):
    text = "مرحبا بك في قائمة المساعدة!"
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("الأوامر الأساسية 🙋‍♂️", callback_data="basic_cmds"), 
         InlineKeyboardButton("المُتقدّم 🙋‍♂️", callback_data="adv_menu")],
        [InlineKeyboardButton("الخَبِير 🕵️", callback_data="expert_cmds"), 
         InlineKeyboardButton("دليل المُطوّر 👳‍♂️", callback_data="dev_guide")],
        [InlineKeyboardButton("الرجوع ⬅️ BACK", callback_data="back_to_start")]
    ])
    if message.from_user:
        await message.reply_text(text, reply_markup=markup)
    else:
        await message.edit_text(text, reply_markup=markup)

# --- معالجة الضغطات ---
@app.on_callback_query()
async def callback_handler(client, query):
    data = query.data

    # 🕵️ قسم الخبير (الأوامر التي أرسلتها كتابةً)
    if data == "expert_cmds":
        text = (
            "🕵️ **قسم الخبير**\n\n"
            "📌 **أوامر للجميع:**\n"
            "👥 `/geturl` - جلب رابط الرسالة (بالرد)\n"
            "👮‍♂️ `/inactives` - قائمة الأعضاء غير المتفاعلين\n\n"
            "📌 **الرسائل المثبتة:**\n"
            "👮‍♂️ `/pin` - تثبيت رسالة | `/delpin` - حذف التثبيت\n"
            "👮‍♂️ `/editpin` - تعديل المثبتة | `/repin` - إعادة تثبيت بإشعار\n"
            "👮‍♂️ `/pinned` - عرض الرسائل المثبتة\n\n"
            "📌 **إحصائيات وقوائم:**\n"
            "👮‍♂️ `/list` - قائمة الأعضاء مع عدد رسائلهم\n"
            "👮‍♂️ `/list roles` - عرض الأدوار المخصصة\n"
            "👮‍♂️ `/graphic` - رسم بياني للاتجاهات\n"
            "👮‍♂️ `/trend` - إحصائيات تطور المجموعة\n\n"
            "📌 **الوضع الصامت للمجموعة:**\n"
            "👮‍♂️ `/silence` - تفعيل الوضع الصامت بالكامل\n"
            "👮‍♂️ `/unsilence` - إلغاء الوضع الصامت"
        )
        markup = InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ الرجوع إلى التعليمات", callback_data="back_to_help")]])
        await query.message.edit_text(text, reply_markup=markup)

    # ⬅️ معالجة أزرار الرجوع
    elif data == "back_to_help":
        await help_menu(client, query.message)
    
    elif data == "back_to_start":
        await query.message.edit_text("★ ¦ أهلاً بك يا سيدي الصقر 🦅\n★ ¦ استخدم /help للتحكم بالبوت.")

app.run()
