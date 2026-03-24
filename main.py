import os
import json
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import UserNotParticipant

# --- بياناتك الخاصة ---
API_ID = 21226626 
API_HASH = "ea1a0c2fa9587a9df2a3325056efe110" 
BOT_TOKEN = "8628506847:AAHXZ5rbQvA4BA2CZuf-R-_tt17dqQ3aRRk" 
OWNER_ID = 2011675494  
CHANNEL_USER = "ybpi1" 
MY_ACCOUNT = "@ShexSaqar" # معرف حسابك الشخصي

app = Client("saqr_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- لوحة التحكم المعدلة برابط مباشر ---
main_markup = InlineKeyboardMarkup([
    [InlineKeyboardButton("{ الاوامر }", callback_data="show_locks")],
    [InlineKeyboardButton("{ جلب النسخة }", callback_data="backup")],
    [InlineKeyboardButton("┇ مطور البوت 👨‍💻", url=f"https://t.me/{MY_ACCOUNT}")] # الرابط المباشر
])

@app.on_message(filters.command("start"))
async def start(client, message):
    # فحص الاشتراك الإجباري أولاً
    try:
        await client.get_chat_member(CHANNEL_USER, message.from_user.id)
    except UserNotParticipant:
        return await message.reply_text(
            f"⚠️ عذراً عزيزي، يجب عليك الاشتراك في قناة البوت أولاً!\n📢 القناة: @{CHANNEL_USER}",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("اضغط هنا للاشتراك", url=f"https://t.me/{CHANNEL_USER}")]])
        )
    except: pass

    text = (
        "★ ¦ أهلاً بك يا سيدي الصقر 🦅\n"
        "★ ¦ أنا بوت حماية متكامل، يمكنك التحكم بالأقفال من هنا.\n"
        "★ ¦ للتواصل مع المطور اضغط على الزر أدناه."
    )
    await message.reply_text(text, reply_markup=main_markup)

# باقي الكود (معالجة الأزرار والأوامر...)
@app.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    if query.data == "show_locks":
        await query.answer("قريباً سيتم عرض قائمة الأقفال..", show_alert=True)
    elif query.data == "backup":
        if query.from_user.id != OWNER_ID:
            return await query.answer("هذا الأمر للمطور فقط!", show_alert=True)
        await query.answer("يتم تجهيز النسخة..")

app.run()
