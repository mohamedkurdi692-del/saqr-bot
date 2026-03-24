import os
import json
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

# --- إعدادات الاتصال ---
API_ID = 21226626 
API_HASH = "ea1a0c2fa9587a9df2a3325056efe110" 
BOT_TOKEN = "8628506847:AAHXZ5rbQvA4BA2CZuf-R-_tt17dqQ3aRRk" 
OWNER_ID = 2011675494  

app = Client("saqr_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ملفات البيانات
GROUPS_FILE = "ReplyGroups.json"
USERS_FILE = "usefebot.json"

# دالة لحفظ البيانات وتحديث الإحصائيات
def save_data(file_path, data_id):
    if not os.path.exists(file_path):
        with open(file_path, "w") as f: json.dump([], f)
    
    with open(file_path, "r") as f:
        data = json.load(f)
    
    if data_id not in data:
        data.append(data_id)
        with open(file_path, "w") as f:
            json.dump(data, f)
    return len(data)

# --- لوحة التحكم الأساسية ---
settings_markup = InlineKeyboardMarkup([
    [InlineKeyboardButton("القوانين 📜", callback_data="rules"), 
     InlineKeyboardButton("الترحيب 💬", callback_data="welcome")],
    [InlineKeyboardButton("حذف الرسائل 🗑️", callback_data="del_msgs"),
     InlineKeyboardButton("القيود 🚫", callback_data="limits")],
    [InlineKeyboardButton("رابط المجموعة 🔗", callback_data="link")],
    [InlineKeyboardButton("جلب النسخة الاحتياطية 📥", callback_data="backup")]
])

back_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data="main_menu")]])

# --- تسجيل المجموعات والمشتركين تلقائياً ---
@app.on_message(group=1)
async def auto_save(client, message):
    if message.chat.type in ["group", "supergroup"]:
        save_data(GROUPS_FILE, message.chat.id)
    if message.from_user:
        save_data(USERS_FILE, message.from_user.id)

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

# --- معالج الأزرار ---
@app.on_callback_query()
async def on_button_click(client, callback_query: CallbackQuery):
    data = callback_query.data
    user_id = callback_query.from_user.id

    if data == "rules":
        await callback_query.message.edit_text("📜 **قوانين المجموعة:**\n1️⃣ لا سب\n2️⃣ لا روابط\n3️⃣ احترم الجميع.", reply_markup=back_markup)
    
    elif data == "welcome":
        await callback_query.answer("💬 الترحيب مفعل تلقائياً!", show_alert=True)

    elif data == "backup":
        if user_id != OWNER_ID:
            return await callback_query.answer("عذراً، هذا الأمر للمطور فقط.", show_alert=True)
        
        # قراءة الإحصائيات الحقيقية من الملفات
        g_count = len(json.load(open(GROUPS_FILE))) if os.path.exists(GROUPS_FILE) else 0
        u_count = len(json.load(open(USERS_FILE))) if os.path.exists(USERS_FILE) else 0
        
        caption = (
            "★ ¦ تم جلب النسخه الاحتياطيه\n"
            f"★ ¦ تحتوي على {{{g_count}}} مجموعه\n"
            f"★ ¦ وتحتوي على {{{u_count}}} مشترك"
        )
        
        # إرسال الملفات (تأكد من وجودها)
        for f_name in [GROUPS_FILE, USERS_FILE]:
            if os.path.exists(f_name):
                await client.send_document(chat_id=user_id, document=f_name, caption=caption if "usefe" in f_name else "")
        await callback_query.answer("تم إرسال النسخة الاحتياطية إلى الخاص.")

    elif data == "main_menu":
        await callback_query.message.edit_text(f"أهلاً بك يا سيدي الصقر 🦅\nماذا تأمر؟", reply_markup=settings_markup)

    await callback_query.answer()

print("✅ البوت المطور يعمل الآن!")
app.run()
