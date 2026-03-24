import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- إعداداتك ---
API_ID = 21226626
API_HASH = "ea1a0c2fa9587a9df2a3325056efe110"
BOT_TOKEN = "8628506847:AAHXZ5rbQvA4BA2CZuf-R-_tt17dqQ3aRRk"
OWNER_ID = 2011675494
MY_ACCOUNT = "ShexSaqar"

# أضف آيدي مجموعتك هنا لكي يعمل فيها البوت
ALLOWED_GROUPS = [-100123456789] 

app = Client("saqr_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- 1. قائمة الأوامر (تظهر عند الضغط على الزر) ---
orders_text = (
    "📜 **قائمة أوامر الحماية:**\n\n"
    "🔹 `قفل الروابط` - لمنع نشر الروابط.\n"
    "🔹 `فتح الروابط` - للسماح بنشر الروابط.\n"
    "🔹 `قفل التوجيه` - لمنع توجيه الرسائل.\n"
    "🔹 `طرد` - (بالرد) لطرد عضو.\n"
    "🔹 `كتم` - (بالرد) لكتم عضو.\n\n"
    "⚠️ **ملاحظة:** يجب رفع البوت مشرفاً لتفعيل الأوامر."
)

@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    text = (
        "★ ¦ أهلاً بك يا سيدي الصقر 🦅\n"
        "★ ¦ أنا بوت حماية متكامل لتأمين مجموعتك.\n"
        "★ ¦ البوت يعمل الآن بنظام الموافقة المسبقة."
    )
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("┇ مطور البوت 👨‍💻", url=f"https://t.me/{MY_ACCOUNT}")],
        [InlineKeyboardButton("{ الاوامر }", callback_data="show_orders")]
    ])
    await message.reply_text(text, reply_markup=markup)

# --- 2. معالجة الأزرار ---
@app.on_callback_query()
async def callback(client, query):
    if query.data == "show_orders":
        await query.message.edit_text(orders_text, reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("رجوع للخلف ↩️", callback_data="back_home")]
        ]))
    elif query.data == "back_home":
        # تعود لنفس رسالة البداية
        await start(client, query.message)

# --- 3. نظام الحماية (مثال: منع الروابط) ---
@app.on_message(filters.group & filters.regex(r"t.me|http"))
async def link_filter(client, message):
    # إذا لم يكن المرسل هو المطور أو مشرف
    if message.from_user.id != OWNER_ID:
        await message.delete()
        await message.reply_text(f"⚠️ ممنوع إرسال الروابط هنا يا {message.from_user.mention}!")

# --- 4. الترحيب بالأعضاء الجدد ---
@app.on_message(filters.new_chat_members)
async def welcome(client, message):
    for member in message.new_chat_members:
        await message.reply_text(f"🦅 أهلاً بك يا {member.mention} في مجموعتنا!")

print("🚀 البوت الشامل انطلق الآن!")
app.run()
