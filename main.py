from telegram import Update
from telegram.error import TelegramError
from telegram.ext import CommandHandler, MessageHandler, filters, CallbackContext, Application
from functions import get_birthday, add_birthday
from datetime import datetime
import logging
from keys import tele_token, vivek_chat_id

async def send_message_to_user(context, message):
    try:
        await context.bot.send_message(chat_id=vivek_chat_id, text=message) #chat_id=update.effective_chat.id
        print("Message sent successfully.")
    except TelegramError as e:
        logging.error(f"Failed to send message: {e}")

async def send_birthdays(context: CallbackContext):
    birthdays = get_birthday()
    print(birthdays)
    for birthday in birthdays:
        greeting = f"{birthday[0]}'s birthday is {birthday[1]}"
        await send_message_to_user(context, message=greeting)

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Welcome to the Birthday Reminder bot! Use /add_bdae to add a new birthday.")

async def add_bdae(update: Update, context: CallbackContext):
    context.user_data['adding_bdae'] = 1
    await update.message.reply_text("Please enter the name of the person whose birthday you want to add.")

async def confirm_birthday(update: Update, context: CallbackContext):
    if 'adding_bdae' in context.user_data and context.user_data['adding_bdae'] == 1:
        name = update.message.text.strip()
        context.user_data['name_tb_added'] = name
        await update.message.reply_text(f"Got it! Now, please enter the birth date of {name} (DD/MM).")
        context.user_data['adding_bdae'] =2
        print("Name is" + name)

        
async def save_birthday(update: Update, context: CallbackContext):
    if 'adding_bdae' in context.user_data and context.user_data['adding_bdae'] == 2:
        birthday_strip = update.message.text.strip()
        try:
            birth_date = datetime.strptime(birthday_strip, '%d/%m')
        except ValueError:
            await update.message.reply_text("Invalid date format. Please use DD/MM format.")
            return

        add_birthday(name=context.user_data['name_tb_added'], birthday=birth_date)
        await update.message.reply_text(f"Added {context.user_data['name_tb_added']}'s birthday ({birth_date}) to the database.")
        context.user_data.clear()


if __name__ == "__main__":
    #Create Dispatcher
    application = Application.builder().token(tele_token).build()

    #Add /start handler
    application.add_handler(CommandHandler("start", start))

    #Add /add_bdae handler
    application.add_handler((CommandHandler("add_bdae", add_bdae)))
    
    application.add_handler(MessageHandler(filters.Regex(r"^\d{2}/\d{2}$"), save_birthday))
    application.add_handler(MessageHandler(filters.TEXT & (~ filters.COMMAND), confirm_birthday))

    application.job_queue.run_daily(send_birthdays, time=datetime.strptime('7:10', '%H:%M').time())

    #Start Bot
    application.run_polling(5)
    

