import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# بياناتك الخاصة 
API_ID = 21226626
API_HASH = "ea1a0c2fa9587a9df2a3325056efe110"
BOT_TOKEN = "8628506847:AAHXZ5rbQvA4BA2CZuf-R-_tt17dqQ3aRRk"
MY_ACCOUNT = "ShexSaqar" # حسابك الشخصي

app = Client("saqr_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    # الرسالة الترحيبية الجديدة (بدون ذكر ترمكس)
    text = "★ ¦ أهلاً بك يا سيدي الصقر 🦅\n★ ¦ بوت الحماية الخاص بك يعمل الآن بنجاح على السيرفر السحابي ✅"
    
    # الأزرار التي تظهر حسابك فقط وتحذف القناة
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("┇ مطور البوت 👨‍💻", url=f"https://t.me/{MY_ACCOUNT}")],
        [InlineKeyboardButton("{ الاوامر }", callback_data="orders"), 
         InlineKeyboardButton("{ جلب النسخة }", callback_data="backup")]
    ])
    await message.reply_text(text, reply_markup=markup)

# هذه الجملة ستظهر في سجلات Koyeb فقط لتؤكد لك مكان التشغيل
print("🚀 تم تشغيل البوت بنجاح على سيرفر Koyeb!")
app.run()
