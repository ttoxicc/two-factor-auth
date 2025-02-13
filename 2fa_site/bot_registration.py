import sqlite3
import nest_asyncio
nest_asyncio.apply()

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from database import save_user
import asyncio

BOT_TOKEN = ''

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("👋 Добро пожаловать! Введите логин для регистрации:")
    context.user_data['state'] = 'WAIT_LOGIN'

async def handle_message(update: Update, context: CallbackContext):
    state = context.user_data.get('state')
    
    if state == 'WAIT_LOGIN':
        context.user_data['login'] = update.message.text
        await update.message.reply_text("🔑 Теперь введите пароль:")
        context.user_data['state'] = 'WAIT_PASSWORD'
    
    elif state == 'WAIT_PASSWORD':
        try:
            save_user(
                context.user_data['login'],
                update.message.text,
                update.message.chat_id
            )
            await update.message.reply_text("✅ Регистрация успешна! Теперь вы можете войти на сайт.")
        except sqlite3.IntegrityError:
            await update.message.reply_text("❌ Пользователь с таким логином уже существует")
        finally:
            context.user_data.clear()

async def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    await application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
