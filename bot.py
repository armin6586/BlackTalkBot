from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters

TOKEN = "8652798240:AAGCxVDwuUKGxNKgT98zQgILdAFI6KZ6IUc"

waiting = []
chats = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [
        [InlineKeyboardButton("🔥 Start Chat", callback_data="find")],
        [InlineKeyboardButton("⚡ Next", callback_data="next")],
        [InlineKeyboardButton("❌ Leave", callback_data="leave")],
        [InlineKeyboardButton("👑 VIP", callback_data="vip")]
    ]

    await update.message.reply_text(
        "🖤 BLACKTALK VIP 🖤\nLuxury Anonymous Chat",
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

        if waiting:
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
