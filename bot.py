import os
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ChatJoinRequestHandler,
    ContextTypes,
)

TOKEN = os.getenv("BOT_TOKEN")

WELCOME_MSG = """Hey!  Welcome ❤️🫶🏼
Aapki join request approve ho jyegi soon ✅

Main channel join kar lo yaha:
https://t.me/+Pi6GvsfYlFUzZTg1

Updates miss mat karna! 🔥
"""

logging.basicConfig(level=logging.INFO)

# /start — show all commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
🤖 Bot Commands

/start — Show commands
/approve — Accept all pending requests
/broadcast — Reply to a message with this to broadcast

Owner: @Savan_jod
"""
    await update.message.reply_text(text)


# Join request aate hi user ko DM
async def join_req(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.chat_join_request.from_user
    try:
        await context.bot.send_message(user.id, WELCOME_MSG)
    except:
        pass


# /approve — sab pending accept
async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    approved = 0
    rejected = 0

    try:
        reqs = await context.bot.get_chat_join_requests(chat_id)
        for r in reqs:
            try:
                await context.bot.approve_chat_join_request(chat_id, r.user_chat_id)
                approved += 1
            except:
                rejected += 1
    except:
        pass

    report = f"""✅ ALL REQUEST APPROVED DONE ✓

✔ Approved: {approved}
❌ Rejected: {rejected}

RG - @Savan_jod / @UR_SAVAN

Feedback zaroor dena 💬"""
    await context.bot.send_message(chat_id, report)


# /broadcast — reply karke send
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("Reply to a message to broadcast.")
        return

    msg = update.message.reply_to_message.text
    chat_id = update.effective_chat.id

    try:
        admins = await context.bot.get_chat_administrators(chat_id)
        for a in admins:
            try:
                await context.bot.send_message(a.user.id, msg)
            except:
                pass
        await update.message.reply_text("✅ Broadcast sent")
    except:
        await update.message.reply_text("❌ Broadcast failed")


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("approve", approve))
app.add_handler(CommandHandler("broadcast", broadcast))
app.add_handler(ChatJoinRequestHandler(join_req))

app.run_polling()
