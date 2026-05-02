import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters
)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
PRIVATE_CHANNEL_LINK = "https://t.me/+iqzHV_L7QYIzYjk1"
UPI_ID = "aditiaditi3323@okicici"
PRICE = "199"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.first_name or "Friend"
    keyboard = [[InlineKeyboardButton("💳 Payment Karo & Access Lo", callback_data="show_payment")]]
    await update.message.reply_text(
        f"👋 Hello {name}!\n\n🔥 *Aditi Pandey – Private Group*\n\n✅ 200+ Exclusive Photos & Videos\n✅ Daily Updates\n✅ Private Community Access\n\n💰 Sirf *₹{PRICE}* mein lifetime access!\n\nNiche button dabao 👇",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def show_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [[InlineKeyboardButton("✅ Maine Pay Kar Diya – Screenshot Bhejo", callback_data="paid")]]
    await query.edit_message_text(
        f"💳 *Payment Details*\n\n📱 UPI ID: `{UPI_ID}`\n💰 Amount: *₹{PRICE}*\n\n*Steps:*\n1️⃣ GPay/PhonePe/Paytm kholo\n2️⃣ UPI ID pe ₹{PRICE} bhejo\n3️⃣ Screenshot lo\n4️⃣ Niche button dabao",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def paid_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["waiting_for_screenshot"] = True
    await query.edit_message_text(
        "📸 *Ab screenshot bhejo!*\n\nPayment success ka screenshot is chat mein bhejo.\n\n✅ Screenshot milte hi private group link milega!",
        parse_mode="Markdown"
    )

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("waiting_for_screenshot"):
        context.user_data["waiting_for_screenshot"] = False
        keyboard = [[InlineKeyboardButton("🔓 Private Group Join Karo →", url=PRIVATE_CHANNEL_LINK)]]
        await update.message.reply_text(
            "✅ *Payment Verified! Welcome!*\n\n🎉 Niche button dabao aur join karo!\n\n⚠️ _Yeh link sirf tumhare liye hai_",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        keyboard = [[InlineKeyboardButton("💳 Pehle Payment Karo", callback_data="show_payment")]]
        await update.message.reply_text("⚠️ Pehle payment karo!", reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("waiting_for_screenshot"):
        await update.message.reply_text("📸 Text nahi, payment ka *screenshot* bhejo!", parse_mode="Markdown")
    else:
        keyboard = [[InlineKeyboardButton("🔥 Access Lo – ₹199", callback_data="show_payment")]]
        await update.message.reply_text("👋 Private group access ke liye tap karo!", reply_markup=InlineKeyboardMarkup(keyboard))

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(show_payment, pattern="^show_payment$"))
    app.add_handler(CallbackQueryHandler(paid_button, pattern="^paid$"))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
