from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- إعدادات الاتصال ---
API_ID =  21226626 # ضع رقمك هنا
API_HASH = "ea1a0c2fa9587a9df2a3325056efe110" # ضع الهاش هنا
BOT_TOKEN = "8628506847:AAHXZ5rbQvA4BA2CZuf-R-_tt17dqQ3aRRk" # ضع توكن البوت هنا
OWNER_ID = 2011675494  # !!! ضع الأيدي (ID) الخاص بحسابك أنت هنا لكي يعرفك البوت

app = Client("saqr_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- لوحة التحكم (الأزرار) ---
settings_markup = InlineKeyboardMarkup([
    [InlineKeyboardButton("القوانين 📜", callback_data="rules"), 
     InlineKeyboardButton("الترحيب 💬", callback_data="welcome")],
    [InlineKeyboardButton("حذف الرسائل 🗑️", callback_data="del_msgs"),
     InlineKeyboardButton("القيود 🚫", callback_data="limits")],
    [InlineKeyboardButton("رابط المجموعة 🔗", callback_data="link")]
])

# أمر البداية - يعمل في الخاص والمجموعة ولا يتجاهلك
@app.on_message(filters.command("start"))
async def start(client, message):
    if message.from_user.id == OWNER_ID:
        await message.reply_text(
            f"أهلاً بك يا سيدي الصقر 🦅\nأنا تحت سيطرتك الآن، ماذا تأمر؟",
            reply_markup=settings_markup
        )
    else:
        await message.reply_text("أهلاً بك في بوت الحماية. أنا أعمل الآن لتأمين المجموعة.")

# أمر الإعدادات - يفتح فقط للمشرفين أو لك أنت
@app.on_message(filters.command("settings") & (filters.me | filters.create(lambda _, __, m: m.from_user.id == OWNER_ID)))
async def show_settings(client, message):
    await message.reply_text(
        "⚙️ لوحة تحكم المشرفين:\nاختر القسم الذي تريد تعديله:",
        reply_markup=settings_markup
    )

print("البوت يعمل بنجاح وتحت سيطرة الصقر!")
app.run()
