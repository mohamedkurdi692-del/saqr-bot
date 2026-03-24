import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# بياناتك
API_ID = 21226626
API_HASH = "ea1a0c2fa9587a9df2a3325056efe110"
BOT_TOKEN = "8628506847:AAHXZ5rbQvA4BA2CZuf-R-_tt17dqQ3aRRk"
MY_ACCOUNT = "ShexSaqar"

app = Client("saqr_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- أمر المساعدة بتصميم الصورة ---
@app.on_message(filters.command("help"))
async def help_menu(client, message):
    text = "مرحبا بك في قائمة المساعدة!"
    markup = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("الأوامر الأساسية 🙋‍♂️", callback_data="basic"),
            InlineKeyboardButton("المُتقدّم 🙋‍♂️", callback_data="advanced")
        ],
        [
            InlineKeyboardButton("الخَبِير 🕵️", callback_data="expert"),
            InlineKeyboardButton("دليل المُطوّر 👳‍♂️", callback_data="dev")
        ],
        [InlineKeyboardButton("الرجوع ⬅️ BACK", callback_data="main_menu")]
    ])
    await message.reply_text(text, reply_markup=markup)

# --- معالجة ضغطات الأزرار ---
@app.on_callback_query()
async def on_click(client, query):
    if query.data == "basic":
        await query.message.edit_text("📌 **الأوامر الأساسية:**\nتستخدم لإدارة الأعضاء الجدد والترحيب.")
    elif query.data == "advanced":
        await query.message.edit_text("🚀 **الأوامر المتقدمة:**\nتستخدم لقفل الروابط والتحكم الكامل.")
    elif query.data == "main_menu":
        await help_menu(client, query.message)

app.run()
