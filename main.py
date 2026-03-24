import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- بياناتك الخاصة ---
API_ID = 21226626
API_HASH = "ea1a0c2fa9587a9df2a3325056efe110"
BOT_TOKEN = "8628506847:AAHXZ5rbQvA4BA2CZuf-R-_tt17dqQ3aRRk"
OWNER_ID = 2011675494
MY_ACCOUNT = "ShexSaqar"

# --- قائمة المجموعات المسموح لها (ضع آيدي مجموعتك هنا) ---
# يمكنك إضافة أكثر من آيدي بين الفواصل
ALLOWED_GROUPS = [-100123456789] 

app = Client("saqr_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# فحص إذا كانت المجموعة مسموحة
def is_allowed(_, __, message):
    if message.chat.type == "private": return True # السماح بالخاص دائماً لك
    return message.chat.id in ALLOWED_GROUPS

@app.on_message(filters.group & ~filters.create(is_allowed))
async def bot_leave(client, message):
    await message.reply_text("⚠️ عذراً، هذا البوت خاص ولا يعمل في هذه المجموعة دون موافقة المطور.")
    await client.leave_chat(message.chat.id) # البوت يغادر المجموعة تلقائياً

@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    text = "★ ¦ أهلاً بك يا سيدي الصقر 🦅\n★ ¦ البوت محمي بنظام 'الموافقة المسبقة' ولا يعمل إلا في مجموعاتك المعتمدة."
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("┇ مطور البوت 👨‍💻", url=f"https://t.me/{MY_ACCOUNT}")],
        [InlineKeyboardButton("{ الاوامر }", callback_data="orders")]
    ])
    await message.reply_text(text, reply_markup=markup)

app.run()
