from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

# --- إعدادات الاتصال (بياناتك الصحيحة) ---
API_ID = 21226626 
API_HASH = "ea1a0c2fa9587a9df2a3325056efe110" 
BOT_TOKEN = "8628506847:AAHXZ5rbQvA4BA2CZuf-R-_tt17dqQ3aRRk" 
OWNER_ID = 2011675494  

app = Client("saqr_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- لوحة التحكم الأساسية ---
settings_markup = InlineKeyboardMarkup([
    [InlineKeyboardButton("القوانين 📜", callback_data="rules"), 
     InlineKeyboardButton("الترحيب 💬", callback_data="welcome")],
    [InlineKeyboardButton("حذف الرسائل 🗑️", callback_data="del_msgs"),
     InlineKeyboardButton("القيود 🚫", callback_data="limits")],
    [InlineKeyboardButton("رابط المجموعة 🔗", callback_data="link")]
])

# زر الرجوع للقائمة الرئيسية
back_markup = InlineKeyboardMarkup([
    [InlineKeyboardButton("🔙 رجوع", callback_data="main_menu")]
])

# --- الأوامر ---

@app.on_message(filters.command("start"))
async def start(client, message):
    if message.from_user.id == OWNER_ID:
        await message.reply_text(
            f"أهلاً بك يا سيدي الصقر 🦅\nأنا تحت سيطرتك الآن، ماذا تأمر؟",
            reply_markup=settings_markup
        )
    else:
        await message.reply_text("🛡️ أهلاً بك في بوت الحماية. أنا أعمل الآن لتأمين المجموعة.")

# --- معالج الأزرار (هذا الجزء هو الذي يحل مشكلة التعليق) ---

@app.on_callback_query()
async def on_button_click(client, callback_query: CallbackQuery):
    data = callback_query.data
    
    # 1. زر القوانين
    if data == "rules":
        await callback_query.message.edit_text(
            "📜 **قوانين المجموعة:**\n\n1️⃣ ممنوع السب والقذف.\n2️⃣ ممنوع إرسال روابط إعلانية.\n3️⃣ احترم الأعضاء والمشرفين.",
            reply_markup=back_markup
        )
    
    # 2. زر الترحيب
    elif data == "welcome":
        await callback_query.answer("💬 ميزة الترحيب تعمل تلقائياً عند دخول أعضاء جدد!", show_alert=True)
    
    # 3. زر حذف الرسائل
    elif data == "del_msgs":
        await callback_query.answer("🗑️ سيتم تفعيل التنظيف التلقائي للرسائل المزعجة.", show_alert=True)

    # 4. زر رابط المجموعة
    elif data == "link":
        chat = callback_query.message.chat
        await callback_query.message.edit_text(
            f"🔗 **رابط المجموعة:**\nيمكنك الحصول على الرابط من إعدادات المجموعة مباشرة.",
            reply_markup=back_markup
        )

    # 5. زر الرجوع للقائمة الرئيسية
    elif data == "main_menu":
        await callback_query.message.edit_text(
            "أهلاً بك يا سيدي الصقر 🦅\nأنا تحت سيطرتك الآن، ماذا تأمر؟",
            reply_markup=settings_markup
        )

    # لإنهاء حالة "التحميل" (الساعة الرملية) على الزر فوراً
    await callback_query.answer()

print("✅ البوت يعمل الآن بكامل طاقته وأزراره!")
app.run()
