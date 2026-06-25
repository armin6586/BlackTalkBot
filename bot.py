from database import db, cursor
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters

TOKEN = "8652798240:AAGCxVDwuUKGxNKgT98zQgILdAFI6KZ6IUc"

waiting = []
chats = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [
        [InlineKeyboardButton("🔥 Start Chat | شروع چت", callback_data="find")],
        [InlineKeyboardButton("⚡ Next | چت بعدی", callback_data="next")],
        [InlineKeyboardButton("❌ Leave | خروج", callback_data="leave")],
        [InlineKeyboardButton("👤 Profile | پروفایل", callback_data="profile")],
        [InlineKeyboardButton("👑 VIP Lounge", callback_data="vip")]
    ]
cursor.execute(
    "INSERT OR IGNORE INTO users(user_id) VALUES(?)",
    (update.effective_user.id,)
)
db.commit()
    text = (
        "🖤✨ BLACKTALK VIP ✨🖤\n\n"
        "🎭 Luxury Anonymous Chat\n"
        "چت ناشناس خاص و متفاوت\n\n"
        "🔥 Meet strangers\n"
        "⚡ Safe & Fast\n"
        "👑 VIP Experience"
    )

    await update.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(kb)
    )
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    try:
        await q.answer()
    except:
        pass

    uid = q.from_user.id
    data = q.data

    if data == "find":
        if uid in chats:
            await q.message.reply_text("Already chatting")
            return

        if waiting and waiting[0] != uid:
            p = waiting.pop(0)
            chats[uid] = p
            chats[p] = uid
            await context.bot.send_message(uid, "✅ Connected")
            await context.bot.send_message(p, "✅ Connected")
        else:
            waiting.append(uid)
            await q.message.reply_text("⏳ Waiting...")

    elif data == "next":
        if uid in chats:
            p = chats[uid]
            del chats[uid]
            del chats[p]
            await context.bot.send_message(p, "Partner left")

        if waiting:
            p = waiting.pop(0)
            chats[uid] = p
            chats[p] = uid
            await context.bot.send_message(uid, "✅ Connected")
            await context.bot.send_message(p, "✅ Connected")
        else:
            waiting.append(uid)
            await q.message.reply_text("Searching...")

    elif data == "leave":
        if uid in chats:
            p = chats[uid]
            del chats[uid]
            del chats[p]
            await context.bot.send_message(p, "Disconnected")
            await q.message.reply_text("You left chat")
        else:
            await q.message.reply_text("No active chat")
elif data == "profile":
    await q.message.reply_text(
        f"👤 Profile\n🆔 ID: {uid}\n👑 Rank: Member"
    
    elif data == "vip":
        await q.message.reply_text("👑 VIP Coming Soon")

async def relay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid in chats:
        p = chats[uid]
        await context.bot.send_message(p, update.message.text)
    else:
        await update.message.reply_text("Press Start Chat")

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, relay))

print("BlackTalk Cloud Running")
app.run_polling()
