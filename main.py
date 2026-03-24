import os
import json
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import UserNotParticipant

# --- إعدادات الاتصال ---
API_ID = 21226626 
API_HASH = "ea1a0c2fa9587a9df2a3325056efe110" 
BOT_TOKEN = "8628506847:AAHXZ5rbQvA4BA2CZuf-R-_tt17dqQ3aRRk" 
OWNER_ID = 2011675494  
CHANNEL_USER = "ybpi1" # معرف قناتك بدون @

app = Client("saqr_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ملف حفظ حالات القفل
LOCKS_FILE = "locks.json"

def get_locks():
    if not os.path.exists(LOCKS_FILE):
        initial_locks = {
            "الروابط": False, "المعرف": False, "التاك": False, "الشارحه": False,
            "التعديل": False, "المتحركه": False, "الملفات": False, "الصور": False,
            "الفيديو": False, "البوتات": False, "التكرار": False, "الملصقات": False,
            "التوجيه": False, "الاغاني": False, "الصوت": False, "التثبيت": False,
            "الدردشه": False, "الفشار": False, "الكفر": False, "الاباحي": False
        }
        with open(LOCKS_FILE, "w", encoding="utf-8") as f:
            json.dump(initial_locks, f)
    with open(LOCKS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# --- فحص الاشتراك الإجباري ---
async def check_subscribe(client, message):
    try:
        await client.get_chat_member(CHANNEL_USER, message.from_user.id)
        return True
    except UserNotParticipant:
        await message.reply_text(
            f"⚠️ عذراً عزيزي، يجب عليك الاشتراك في قناة البوت أولاً لاستخدام الميزات!\n\nقناتنا: @{CHANNEL_USER}",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("اضغط هنا للاشتراك 📢", url=f"https://t.me/{CHANNEL_USER}")
            ]])
        )
        return False
    except Exception:
        return True # في حال وجود خطأ تقني لا نعطل البوت

# --- معالج أوامر القفل والفتح (للمطور/المشرف) ---
@app.on_message(filters.group & filters.regex(r"^(قفل|فتح) (.*)"))
async def lock_unlock_handler(client, message):
    if not await check_subscribe(client, message): return
    
    # التحقق من أن المرسل هو المطور أو مشرف
    member = await client.get_chat_member(message.chat.id, message.from_user.id)
    if message.from_user.id != OWNER_ID and member.status not in ["administrator", "creator"]:
        return

    action = message.matches[0].group(1)
    item = message.matches[0].group(2).strip()
    
    locks = get_locks()
    if item in locks:
        status = True if action == "قفل" else False
        locks[item] = status
        with open(LOCKS_FILE, "w", encoding="utf-8") as f:
            json.dump(locks, f, ensure_ascii=False, indent=4)
        
        status_text = "مقفول 🔒" if status else "مفتوح 🔓"
        await message.reply_text(f"★ ¦ تم {action} {item} بنجاح\n★ ¦ الحالة الآن: {status_text}")

# --- نظام الحماية التلقائي ---
@app.on_message(filters.group & ~filters.service, group=2)
async def auto_protection(client, message):
    if message.from_user and message.from_user.id == OWNER_ID: return
    
    locks = get_locks()
    # (هنا نضع نفس شروط الحذف التي شرحناها سابقاً للصور والروابط...)
    if message.text or message.caption:
        text = message.text or message.caption
        if locks.get("الروابط") and ("http" in text or "t.me" in text): await message.delete()
    if locks.get("الصور") and message.photo: await message.delete()

# --- قائمة الأوامر بحقوقك ---
@app.on_message(filters.command("الاوامر"))
async def show_all_locks(client, message):
    if not await check_subscribe(client, message): return
    
    locks = get_locks()
    text = "★ ¦ اوامر الحمايه الخاصة ببوت الصقر ...\n"
    text += "—————————————\n"
    for key, val in locks.items():
        status = "قفل 🔒" if val else "فتح 🔓"
        text += f"★ ¦ {status} ← {key}\n"
    text += "—————————————"
    
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("{ 2 }", callback_data="p2"), InlineKeyboardButton("{ 1 }", callback_data="p1")],
        [InlineKeyboardButton("{ 4 }", callback_data="p4"), InlineKeyboardButton("{ 3 }", callback_data="p3")],
        [InlineKeyboardButton("┇ 𝖢𝖧𝖠𝖭𝖭𝖤𝖫 𝖲𝖠𝖰𝖱", url=f"https://t.me/{CHANNEL_USER}")]
    ])
    
    await message.reply_text(text, reply_markup=markup)

print("✅ بوت الصقر يعمل الآن مع نظام الاشتراك الإجباري وحقوق قناتك!")
app.run()
