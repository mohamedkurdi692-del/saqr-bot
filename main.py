from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant

# --- بيانات البوت (املأها بنفسك) ---
API_ID = 21226626
API_HASH = "ea1a0c2fa9587a9df2a3325056efe110"
BOT_TOKEN = "8628506847:AAHXZ5rbQvA4BA2CZuf-R-_tt17dqQ3aRRk" 
CHANNEL_USERNAME = "ybpi1" 
# --------------------------------

app = Client("saqr_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.group & ~filters.service)
async def check_subscription(client, message: Message):
    try:
        # التحقق هل العضو مشترك في القناة أم لا
        user = await client.get_chat_member(CHANNEL_USERNAME, message.from_user.id)
    except UserNotParticipant:
        # إذا لم يكن مشتركاً: احذف رسالته وأرسل له تنبيه
        await message.delete()
        await message.reply_text(
            f"يا {message.from_user.mention}، عذراً لا يمكنك الكتابة في المجموعة!\n\n"
            f"يجب عليك الاشتراك في قناة المجموعة أولاً لتتمكن من التفاعل.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("إضغط هنا للاشتراك", url=f"https://t.me/{CHANNEL_USERNAME}")],
                [InlineKeyboardButton("تحقق من الاشتراك ✅", callback_data="check_sub")]
            ])
        )
    except Exception as e:
        print(f"Error: {e}")

@app.on_callback_query(filters.regex("check_sub"))
async def check_button(client, callback_query):
    try:
        await client.get_chat_member(CHANNEL_USERNAME, callback_query.from_user.id)
        await callback_query.answer("أحسنت! أنت الآن مشترك، يمكنك الكتابة.", show_alert=True)
        await callback_query.message.delete()
    except UserNotParticipant:
        await callback_query.answer("ما زلت غير مشترك! اشترك أولاً.", show_alert=True)

print("البوت يعمل بنجاح...")
app.run()
