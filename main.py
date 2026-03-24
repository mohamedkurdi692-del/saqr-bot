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
CHANNEL_USER = "ybpi1" # معرف قناتك للاشتراك الإجباري

app = Client("saqr_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ملفات البيانات
GROUPS_FILE = "ReplyGroups.json"
USERS_FILE = "usefebot.json"
LOCKS_FILE = "locks.json"

# دالة لجلب الأقفال
def get_locks():
    if not os.path.exists(LOCKS_FILE):
        initial = {
            "الروابط": False, "المعرف": False, "التاك": False, "الصور": False,
            "الفيديو": False, "الملصقات": False, "المتحركه": False, "التوجيه": False,
            "الاغاني": False, "الصوت": False, "الفشار": False, "الكفر": False
        }
        with open(LOCKS_FILE, "w", encoding="utf-8") as f: json.dump(initial, f)
    return json.load(open(LOCKS_FILE, "r", encoding="utf-8"))

# دالة حفظ المشتركين والمجموعات
def save_data(file_path, data_id):
    if not os.path.exists(file_path):
        with open(file_path, "w") as f: json.dump([], f)
    with open(file_path, "r") as f: data = json.load(f)
    if data_id not in data:
        data.append(data_id)
        with open(file_path, "w") as f: json.dump(data, f)

# فحص الاشتراك الإجباري
async def check_sub(client, message):
    try:
        await client.get_chat_member(CHANNEL_USER, message.from_user.id)
        return True
    except UserNotParticipant:
        await message.reply_text(
            f"⚠️ عذراً عزيزي، يجب عليك الاشتراك في قناة البوت أولاً!\n📢 القناة: @{CHANNEL_USER}",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("اضغط هنا للاشتراك", url=f"https://t.me/{CHANNEL_USER}")]])
        )
        return False
    except: return True

# --- لوحة التحكم الرئيسية ---
main_markup = InlineKeyboardMarkup([
    [InlineKeyboardButton("{ الاوامر }", callback_data="show_locks")],
    [InlineKeyboardButton("{ جلب النسخة }", callback_data="backup"), InlineKeyboardButton("{ المطور }", url="tg://user?id=2011675494")],
    [InlineKeyboardButton("┇ 𝖢𝖧𝖠𝖭𝖭𝖤𝖫 𝖲𝖠𝖰𝖱", url=f"https://t.me/{CHANNEL_USER}")]
])

@app.on_message(filters.command("start"))
async def start(client, message):
    if not await check_sub(client, message): return
    save_data(USERS_FILE, message.from_user.id)
    await message.reply_text(f"أهلاً بك يا سيدي الصقر 🦅\nأنا بوت حماية متكامل لتأمين مجموعتك.", reply_markup=main_markup)

# --- معالج أوامر قفل و فتح ---
@app.on_message(filters.group & filters.regex(r"^(قفل|فتح) (.*)"))
async def lock_unlock(client, message):
    if not await check_sub(client, message): return
    # التحقق من الرتبة (مطور أو أدمن)
    user = await client.get_chat_member(message.chat.id, message.from_user.id)
    if message.from_user.id != OWNER_ID and user.status not in ["administrator", "creator"]: return

    action, item = message.matches[0].group(1), message.matches[0].group(2).strip()
    locks = get_locks()
    if item in locks:
        locks[item] = True if action == "قفل" else False
        json.dump(locks, open(LOCKS_FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=4)
        await message.reply_text(f"★ ¦ تم {action} {item} بنجاح ✅")

# --- نظام الحماية ---
@app.on_message(filters.group & ~filters.service, group=2)
async def protector(client, message):
    if message.from_user and message.from_user.id == OWNER_ID: return
    locks = get_locks()
    if message.text or message.caption:
        text = message.text or message.caption
        if locks["الروابط"] and ("http" in text or "t.me" in text): await message.delete()
        if locks["المعرف"] and "@" in text: await message.delete()
    if locks["الصور"] and message.photo: await message.delete()
    if locks["الفيديو"] and message.video: await message.delete()
    if locks["الملصقات"] and message.sticker: await message.delete()
    if locks["التوجيه"] and message.forward_from_chat: await message.delete()

# --- معالج الأزرار ---
@app.on_callback_query()
async def callback_handler(client, query: CallbackQuery):
    if query.data == "show_locks":
        locks = get_locks()
        text = "★ ¦ اوامر الحمايه كالاتي ...\n—————————————\n"
        for k, v in locks.items(): text += f"★ ¦ {'قفل 🔒' if v else 'فتح 🔓'} ← {k}\n"
        text += "—————————————"
        await query.message.edit_text(text, reply_markup=main_markup)
    
    elif query.data == "backup":
        if query.from_user.id != OWNER_ID: return await query.answer("للمطور فقط!")
        g_count = len(json.load(open(GROUPS_FILE))) if os.path.exists(GROUPS_FILE) else 0
        u_count = len(json.load(open(USERS_FILE))) if os.path.exists(USERS_FILE) else 0
        caption = f"★ ¦ تم جلب النسخه الاحتياطيه\n★ ¦ مجموعات: {{{g_count}}}\n★ ¦ مشتركين: {{{u_count}}}"
        for f in [GROUPS_FILE, USERS_FILE]:
            if os.path.exists(f): await client.send_document(OWNER_ID, f, caption=caption if "usefe" in f else "")
        await query.answer("تم الإرسال للخاص ✅")

print("✅ بوت الصقر الشامل جاهز للعمل!")
app.run()
