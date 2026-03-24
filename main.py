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

# --- 1. واجهة البداية /start ---
@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    text = (
        "السلام عليكم ورحمة الله وبركاته!\n"
        f"@{client.me.username} هو البوت الأكثر تميزاً لمساعدتك في إدارة مجموعتك بكل سهولة و أمان!\n\n"
        "👈 أضفني في مجموعتك ثم قم بمنحي الصلاحيات الكاملة لكي أعمل بشكل صحيح.\n\n"
        "📌 ماهي أوامر البوت؟\nاضغط /help لأعرض لك جميع الأوامر."
    )
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ أضفني إلى مجموعة ➕", url=f"https://t.me/{client.me.username}?startgroup=true")],
        [InlineKeyboardButton("📝 إعدادات المجموعة ⚙️", callback_data="settings_main")],
        [InlineKeyboardButton("📢 القناة", url="https://t.me/ybpi1"), InlineKeyboardButton("👥 المجموعة", url=f"https://t.me/{MY_ACCOUNT}")],
        [InlineKeyboardButton("💬 معلومات", callback_data="info_bot"), InlineKeyboardButton("⛑️ الدعم", url=f"https://t.me/{MY_ACCOUNT}")],
        [InlineKeyboardButton("🇸🇦 Languages 🌍", callback_data="lang_select")]
    ])
    await message.reply_text(text, reply_markup=markup)

# --- 2. واجهة المساعدة الرئيسية /help ---
@app.on_message(filters.command("help"))
async def help_menu(client, message):
    text = "مرحبا بك في قائمة المساعدة!"
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("الأوامر الأساسية 🙋‍♂️", callback_data="basic_cmds"), InlineKeyboardButton("المُتقدّم 🙋‍♂️", callback_data="adv_menu")],
        [InlineKeyboardButton("الخَبِير 🕵️", callback_data="expert_cmds"), InlineKeyboardButton("دليل المُطوّر 👳‍♂️", callback_data="dev_guide")],
        [InlineKeyboardButton("الرجوع ⬅️ BACK", callback_data="back_to_start")]
    ])
    if message.from_user: await message.reply_text(text, reply_markup=markup)
    else: await message.edit_text(text, reply_markup=markup)

# --- 3. معالجة جميع الأزرار (التنقل) ---
@app.on_callback_query()
async def callback_handler(client, query):
    data = query.data

    # أ- الأوامر الأساسية (صورة 24904)
    if data == "basic_cmds":
        text = (
            "🔸 **أوامر أساسية** 🔸\n\n"
            "👮‍♂️ [متاحة لـ المشرفين و المساعدين بالبوت]\n\n"
            "👮‍♂️ /reload - إعادة تشغيل البوت وتحديث المشرفين\n"
            "👮‍♂️ /settings - لعرض إعدادات وأوامر البوت\n"
            "👮‍♂️ /ban - حظر العضو نهائياً\n"
            "👮‍♂️ /mute - كتم العضو عن الكلام\n"
            "👮‍♂️ /kick - طرد العضو من المجموعة\n"
            "👮‍♂️ /unban - إلغاء الحظر عن العضو\n"
            "👮‍♂️ /info - عرض معلومات العضو (بالرد)\n"
            "👮‍♂️ /infopvt - ارسال معلومات العضو بالخاص\n"
            "👮‍♂️ /staff - عرض قائمة الإداريين"
        )
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ الرجوع إلى التعليمات", callback_data="back_to_help")]]))

    # ب- قائمة المتقدم (صورة 24919)
    elif data == "adv_menu":
        text = "إرشادات متقدمة\nفي هذه القائمة ستجد بعض الإرشادات لوظائف مساعدة المجموعة المتقدمة جداً."
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("🏗️ إنشاء فريق الإدارة", callback_data="adv_cmds_list")],
            [InlineKeyboardButton("👾 طريقة صناعة بوت", callback_data="make_bot")],
            [InlineKeyboardButton("🎩 أدوار المستخدمين", callback_data="user_roles")],
            [InlineKeyboardButton("⬅️ الرجوع إلى التعليمات", callback_data="back_to_help")]
        ])
        await query.message.edit_text(text, reply_markup=markup)

    # ج- تفاصيل الأوامر المتقدمة (صورة 24917)
    elif data == "adv_cmds_list":
        text = (
            "📌 **الأوامر المتقدمة**\n\n"
            "📍 **إدارة الإنذارات:**\n"
            "👮‍♂️ /warn - إضافة إنذار للعضو\n"
            "👮‍♂️ /unwarn - إزالة الإنذار\n"
            "👮‍♂️ /warns - رؤية عدد الإنذارات\n\n"
            "📍 **إدارة الحذف:**\n"
            "🛡️ /del - حذف الرسالة المحددة\n"
            "🛡️ /logdel - حذف الرسالة وإرسال إشعار لسجل المجموعة\n\n"
            "📍 **إدارة الإرسال:**\n"
            "👮‍♂️ /send - إرسال رسالة عبر البوت للمجموعة"
        )
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ الرجوع إلى التعليمات", callback_data="adv_menu")]]))

    # د- الخبير (النص الذي أرسلته كتابة)
    elif data == "expert_cmds":
        text = (
            "🕵️ **قسم الخبير**\n\n"
            "📌 **أوامر للجميع:**\n"
            "👥 /geturl - جلب رابط الرسالة (بالرد)\n"
            "👮‍♂️ /inactives - قائمة الأعضاء غير المتفاعلين\n\n"
            "📌 **الرسائل المثبتة:**\n"
            "👮‍♂️ /pin - تثبيت رسالة | /delpin - حذف التثبيت\n"
            "👮‍♂️ /repin - إعادة التثبيت بإشعار\n\n"
            "📌 **الوضع الصامت:**\n"
            "👮‍♂️ /silence - تفعيل الوضع الصامت بالكامل\n"
            "👮‍♂️ /unsilence - إلغاء الوضع الصامت"
        )
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ الرجوع إلى التعليمات", callback_data="back_to_help")]]))

    # هـ- الرجوع واللغات
    elif data == "back_to_help":
        await help_menu(client, query.message)
    elif data == "back_to_start":
        await start(client, query.message)
    elif data == "lang_select":
        await query.message.edit_text("اختر لغتك / Choose Language:", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("العربية 🇸🇦", callback_data="set_ar"), InlineKeyboardButton("English 🇺🇸", callback_data="set_en")]
        ]))

app.run()
