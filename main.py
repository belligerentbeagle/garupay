import os
import logging
from telegram import *
from telegram.ext import *
import mysql.connector

cnx = mysql.connector.connect(user="root",
                              password="admin",
                              host="localhost",
                              database="garupay")
cur = cnx.cursor()
cnx.autocommit = True

TOKEN = os.environ.get("TELEGRAM_TOKEN_KEY", "6399385307:AAGRq0zwoqVWO7GRSPAm8VeOKJ1aeu9UvJU")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    """
    When user starts the bot, show location keyboard and add user id into database to keep record of who uses the bot
    """
    bot_typing(context.bot, update.message.chat_id)
    update.message.reply_text("hi")


def user_input(update: Update, context: CallbackContext):
    message = update.message.text
    user_id = str(update.message.from_user.id)
    chat_id = update.message.chat_id

    cur.execute("SELECT state FROM state_manager WHERE user_id=%s AND chat_id=%s", (user_id, chat_id))
    x = cur.fetchone()
    if x:
        state = x[0]
    else:
        state = -1

    if message == "AI (Beta)" and state == 0:
        context.bot.send_message(chat_id, "AI (Beta) was clicked. Please enter your details...")
        cur.execute("UPDATE state_manager SET state=%s WHERE user_id=%s AND chat_id=%s", (2, user_id, chat_id))
    elif message == "Manual" and state == 0:
        context.bot.send_message(chat_id, "Manual was clicked. Please enter your details...")
        cur.execute("UPDATE state_manager SET state=%s WHERE user_id=%s AND chat_id=%s", (1, user_id, chat_id))

    elif state == 1:
        # getting manual messages:
        print("MANUAL MSG...", message)
        pass
    elif state == 2:
        # process chatgpt
        print("CHATGPT MSG...", message)

        reply_markup = ReplyKeyboardMarkup([
            [KeyboardButton("Yes", callback_data=f"confirm_ai:yes"),
             KeyboardButton("No", callback_data=f"confirm_ai:no")],
        ], one_time_keyboard=True, resize_keyboard=True)
        context.bot.send_message(chat_id, text="Is the payment accurate?", reply_markup=reply_markup)


def add_bills(update: Update, context: CallbackContext):
    user_id = str(update.message.from_user.id)
    chat_id = update.message.chat_id

    cur.execute("INSERT IGNORE INTO state_manager VALUES (%s, %s, %s)", (user_id, chat_id, 0))

    reply_markup = ReplyKeyboardMarkup([
        [KeyboardButton("AI (Beta)", callback_data=f"add_method:ai"),
         KeyboardButton("Manual", callback_data=f"add_method:manual")],
    ], one_time_keyboard=True, resize_keyboard=True)
    context.bot.send_message(chat_id, text="How do you wish to split your bills?", reply_markup=reply_markup)


def remove_bills(update: Update, context: CallbackContext):
    user_id = str(update.message.from_user.id)
    chat_id = update.message.chat_id
    cur.execute("DELETE FROM state_manager WHERE user_id=%s AND chat_id=%s", (user_id, chat_id))
    context.bot.send_message(chat_id, "State have been removed.")


def prevent_error(update: Update, context: CallbackContext):
    logger.info(context.error)


def help_command(update: Update, context: CallbackContext):
    bot_typing(context.bot, update.message.chat_id)
    context.bot.send_message(update.message.chat_id, "Help!")


def bot_typing(bot, chat_id):
    """
    To stimulate human typing action
    """
    bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

# def stop(update: Update, context: CallbackContext):
#     """
#     When user stops the bot
#     """
#     bot_typing(context.bot, update.message.chat_id)
#     user = update.message.from_user
#     logger.info("User %s canceled the conversation.", user.first_name)
#     update.message.reply_text("stop", reply_markup=ReplyKeyboardRemove())
#     return ConversationHandler.END


def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("add", add_bills))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("remove", remove_bills))
    dispatcher.add_handler(MessageHandler(Filters.text, user_input))
    # dispatcher.add_error_handler(prevent_error)
    updater.start_polling()


if __name__ == "__main__":
    main()
