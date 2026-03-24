import os
‏import json
‏from pyrogram import Client, filters
‏from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
‏from pyrogram.errors import UserNotParticipant
‏
‏# --- بياناتك الخاصة (تأكد من صحتها) ---
‏API_ID = 21226626 
‏API_HASH = "ea1a0c2fa9587a9df2a3325056efe110" 
‏BOT_TOKEN = "8628506847:AAHXZ5rbQvA4BA2CZuf-R-_tt17dqQ3aRRk" 
‏OWNER_ID = 2011675494  
‏CHANNEL_USER = "ybpi1" # قناة الاشتراك الإجباري
‏MY_USERNAME = "ShexSaqar" # حسابك الخاص للتواصل
‏
‏app = Client("saqr_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
‏
‏# ملفات البيانات
‏LOCKS_FILE = "locks.json"
‏GROUPS_FILE = "ReplyGroups.json"
‏USERS_FILE = "usefebot.json"
‏
‏def get_locks():
‏    if not os.path.exists(LOCKS_FILE):
‏        initial = {"الروابط": False, "الصور": False, "المعرف": False, "التوجيه": False}
‏        with open(LOCKS_FILE, "w", encoding="utf-8") as f: json.dump(initial, f)
‏    return json.load(open(LOCKS_FILE, "r", encoding="utf-8"))
‏
‏# --- فحص الاشتراك الإجباري ---
‏async def check_subscribe(client, message):
‏    try:
‏        await client.get_chat_member(CHANNEL_USER, message.from_user.id)
‏        return True
‏    except UserNotParticipant:
‏        await message.reply_text(
‏            f"⚠️ عذراً عزيزي، يجب عليك الاشتراك في قناة البوت أولاً لاستخدام الميزات!\n\nقناتنا: @{CHANNEL_USER}",
‏            reply_markup=InlineKeyboardMarkup([[
‏                InlineKeyboardButton("اضغط هنا للاشترك في القناة 📢", url=f"https://t.me/{CHANNEL_USER}")
‏            ]])
‏        )
‏        return False
‏    except: return True
‏
‏# --- لوحة التحكم (حقوق المطور) ---
‏main_markup = InlineKeyboardMarkup([
‏    [InlineKeyboardButton("{ الاوامر }", callback_data="show_locks")],
‏    [InlineKeyboardButton("{ جلب النسخة }", callback_data="backup")],
‏    [InlineKeyboardButton("┇ مطور البوت 👨‍💻", url=f"https://t.me/{MY_USERNAME}")]
‏])
‏
‏@app.on_message(filters.command("start"))
‏async def start(client, message):
‏    if not await check_subscribe(client, message): return
‏    
‏    text = (
‏        "★ ¦ أهلاً بك يا سيدي الصقر 🦅\n"
‏        "★ ¦ أنا بوت حماية متكامل، يمكنك التحكم بالأقفال من هنا.\n"
‏        "★ ¦ للتواصل مع المطور اضغط على الزر أدناه."
‏    )
‏    await message.reply_text(text, reply_markup=main_markup)
‏
‏# --- معالجة الأزرار ---
‏@app.on_callback_query()
‏async def callback_handler(client, query: CallbackQuery):
‏    if query.data == "show_locks":
‏        locks = get_locks()
‏        text = "★ ¦ قائمة أوامر الحماية الخاصة بك:\n—————————————\n"
‏        for k, v in locks.items():
‏            text += f"★ ¦ {'قفل 🔒' if v else 'فتح 🔓'} ← {k}\n"
‏        text += "—————————————"
‏        await query.message.edit_text(text, reply_markup=main_markup)
‏    
‏    elif query.data == "backup":
‏        if query.from_user.id != OWNER_ID:
‏            return await query.answer("عذراً، هذا الأمر للمطور فقط. تواصل مع @{}.".format(MY_USERNAME), show_alert=True)
‏        
‏        for f in [GROUPS_FILE, USERS_FILE]:
‏            if os.path.exists(f):
‏                await client.send_document(OWNER_ID, f, caption="✅ نسخة احتياطية لبيانات البوت")
‏        await query.answer("تم إرسال الملفات إلى الخاص بنجاح ✅")
‏
‏print("🚀 تم التحديث: الاشتراك الإجباري مفعل + حقوق المطور @{}!".format(MY_USERNAME))
‏app.run()
‏
‏
‏
