import os
import re
import json
import logging
from paymentTest import settlepayment
from datetime import datetime
from telegram import *
from telegram.ext import *
import mysql.connector
from splitwise import *
from openai_connector import query_openai

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

    cur.execute("SELECT * FROM state_manager WHERE user_id=%s AND chat_id=%s", (user_id, chat_id))
    x = cur.fetchone()
    if x:
        db1, db2, state = x
    else:
        db1 = db2 = None
        state = -1

    if db1 == db2 and db1 and state == 10:
        # update email address
        cur.execute("UPDATE users SET email=%s WHERE user_id=%s", (message, user_id, ))
        context.bot.send_message(chat_id, "Email Address added. Account successfully linked.")
        cur.execute("DELETE FROM state_manager WHERE user_id=%s AND state=5", (user_id,))

    elif message == "AI (Beta)" and state == 0:
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
        if message.lower() == "yes":

            context.bot.send_message(chat_id, text="Great that it is working!")
            cur.execute("DELETE FROM state_manager WHERE user_id=%s AND chat_id=%s", (user_id, chat_id))
        elif message.lower() == "no":
            # break and remove last record in DB
            context.bot.send_message(chat_id, text="Please be more specific or list out any mistakes...")
            cur.execute("SELECT date_updated FROM transactions WHERE chat_id=%s ORDER BY date_updated DESC LIMIT 1",
                        (chat_id, ))

            x = cur.fetchone()[0]
            cur.execute("DELETE FROM transactions WHERE chat_id=%s AND date_updated=%s", (chat_id, x))
        else:
            # process chatgpt
            reply = query_openai(message)

            context.bot.send_message(chat_id, text=reply)

            try:
                reply_dict = json.loads(re.search('({.+})', reply).group(0).replace("'", '"'))

                if "Me" in reply_dict:
                    i = reply_dict["Me"]
                    del reply_dict["Me"]
                    cur.execute("SELECT username FROM users WHERE user_id=%s", (user_id,))
                    username = cur.fetchone()[0]

                    cur.execute("SELECT name FROM friends WHERE username=%s", (username,))
                    name = cur.fetchone()[0]
                    reply_dict[name] = i

                tmpList = []
                for name, value in reply_dict.items():
                    cur.execute("SELECT username FROM friends WHERE name=%s AND chat_id=%s", (name.lower(), chat_id))
                    x = cur.fetchone()
                    if x:
                        ppl_username = x[0]
                        # send msg to user to pay
                        cur.execute("SELECT user_id FROM users WHERE username=%s", (ppl_username,))
                        x = cur.fetchone()
                        if x:
                            ppl_id = x[0]
                            tmpList.append([ppl_id, value])
                        else:
                            context.bot.send_message(chat_id,
                                                     text=f"It seems like @{ppl_username} has not registered for an "
                                                          f"account. Ask @{ppl_username} to @garupay_bot to register.")

                    else:
                        context.bot.send_message(chat_id, text=f"It seems like {name} has not been mapped yet. Please "
                                                               f"map it at /set_names first.")
                print(tmpList, "-==============================")
                splitW = settleUp(tmpList)
                print(splitW, "********************************")
                for fromUser, toUser, amount in splitW:
                    cur.execute("INSERT INTO transactions VALUES (%s, %s, %s, %s, %s, %s)", (fromUser, toUser, chat_id, amount, str(datetime.utcnow()).split(".")[0], 0))

                reply_markup = ReplyKeyboardMarkup([
                    [KeyboardButton("Yes", callback_data=f"confirm_ai:yes"),
                     KeyboardButton("No", callback_data=f"confirm_ai:no")],
                ], one_time_keyboard=True, resize_keyboard=True)
                output = "Current Status. Is this accurate?\n\n"
                for name, value in reply_dict.items():
                    output += f"{name}: {value}\n"
                context.bot.send_message(chat_id, text=output, reply_markup=reply_markup, parse_mode=ParseMode.HTML)

            except AttributeError:
                update.message.reply_text("I can't seem to understand what you are saying. Please be more concise. "
                                          "If you do not wish to split your payment now, type /remove.")
    elif state == 5:
        # mapping name to tele
        cur.execute("DELETE FROM friends WHERE chat_id=%s", (chat_id,))
        for row in message.split("\n"):
            try:
                name, tele_handle = row.split(": @")
                cur.execute("INSERT IGNORE INTO friends VALUES (%s, %s, %s)",
                            (name.replace(" ", ""), tele_handle.replace(" ", ""), chat_id))
            except:
                context.bot.send_message(chat_id, "Wrong format! Please try again")
                return

        context.bot.send_message(chat_id, text="Mapping successfully completed!")
        cur.execute("DELETE FROM state_manager WHERE user_id=%s AND chat_id=%s", (user_id, chat_id))


def add_bills(update: Update, context: CallbackContext):
    user_id = str(update.message.from_user.id)
    chat_id = update.message.chat_id

    cur.execute("SELECT * FROM state_manager WHERE user_id=%s AND chat_id=%s", (user_id, chat_id))
    x = cur.fetchone()
    if x:
        context.bot.send_message(chat_id, text="You have an existing payment that is incomplete. Please "
                                               "continue it or type /remove to remove it.")
    else:
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


def existing_payment(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    tmp = {}
    cur.execute("SELECT to_user_id, SUM(amount) as totalAmt FROM transactions WHERE chat_id=%s AND "
                "has_paid=0 GROUP BY to_user_id", (chat_id, ))
    x = cur.fetchall()
    for ppl, amt in x:
        tmp[ppl] = tmp.get(ppl, 0) + amt

    cur.execute("SELECT from_user_id, -SUM(amount) as totalAmt FROM transactions WHERE chat_id=%s AND "
                "has_paid=0 GROUP BY from_user_id", (chat_id,))
    x = cur.fetchall()
    for ppl, amt in x:
        tmp[ppl] = tmp.get(ppl, 0) + amt

    if tmp:
        output = "Existing transactions not settled: \n\n"
        for user_id, amt in tmp.items():
            cur.execute("SELECT username FROM users WHERE user_id=%s", (user_id,))
            username = cur.fetchone()[0]
            output += f"@{username}: {amt}$\n"
        context.bot.send_message(chat_id, text=output)
    else:
        context.bot.send_message(chat_id, text="No pending payments at the moment.")


def settle_bills(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    cur.execute("SELECT from_user_id, to_user_id, amount FROM transactions WHERE chat_id=%s AND has_paid=0", (chat_id,))
    x = cur.fetchall()
    print(x)
    for from_user_id, to_user_id, amount in x:
        cur.execute("SELECT email FROM users WHERE user_id=%s", (to_user_id,))
        email = cur.fetchone()[0]

        settlepayment(amount, email)

        cur.execute("UPDATE transactions SET has_paid=1 WHERE chat_id=%s AND has_paid=0", (chat_id,))

    context.bot.send_message(chat_id, "Payment settled!")


def register(update: Update, context: CallbackContext):
    user_id = str(update.message.from_user.id)
    username = update.message.from_user.username
    context.bot.send_message(user_id, "Please enter your Paypal email address to register for GaruPay.")
    cur.execute("INSERT IGNORE INTO state_manager VALUES (%s, %s, %s)", (user_id, user_id, 10))
    cur.execute("INSERT IGNORE INTO users (username, user_id) VALUES (%s, %s)", (username, user_id, ))


def view_names(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    cur.execute("SELECT * FROM friends WHERE chat_id=%s", (chat_id,))
    x = cur.fetchall()
    if x:
        output = "This group current mapping is:\n\n"
        for name, username, _ in x:
            output += f"{name}: @{username}\n"
        context.bot.send_message(chat_id, output, parse_mode=ParseMode.HTML)
    else:
        context.bot.send_message(chat_id, "This group has no mapping currently.")


def set_names(update: Update, context: CallbackContext):
    user_id = str(update.message.from_user.id)
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id, "Map your name/initials to your telegram username. \n\n"
                                      "For example, if your name is Ming Ming and your telegram handle is @mingmingg,"
                                      "and your friend name is Wen Wen and his telegram handle is @wenwenn, "
                                      "you should format your input like this: \n\n"
                                      "<pre><code>"
                                      "Ming Ming: @mingmingg\n"
                                      "Wen Wen: @wenwenn"
                                      "</code></pre>", parse_mode=ParseMode.HTML)

    cur.execute("SELECT * FROM friends WHERE chat_id=%s", (chat_id,))
    x = cur.fetchall()
    if x:
        output = "This group current mapping is:\n\n"
        for name, username, _ in x:
            output += f"{name}: @{username}\n"
        context.bot.send_message(chat_id, output, parse_mode=ParseMode.HTML)
    else:
        context.bot.send_message(chat_id, "This group has no mapping currently.")

    cur.execute("SELECT * FROM state_manager WHERE user_id=%s AND chat_id=%s", (user_id, chat_id))
    x = cur.fetchone()
    if x:
        cur.execute("UPDATE state_manager SET state=%s WHERE user_id=%s AND chat_id=%s", (5, user_id, chat_id))
    else:
        cur.execute("INSERT INTO state_manager VALUES (%s, %s, %s)", (user_id, chat_id, 5))


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
    dispatcher.add_handler(CommandHandler("existing_payment", existing_payment))
    dispatcher.add_handler(CommandHandler("settle", settle_bills))
    dispatcher.add_handler(CommandHandler("register", register))
    dispatcher.add_handler(CommandHandler("set_names", set_names))
    dispatcher.add_handler(MessageHandler(Filters.text, user_input))
    # dispatcher.add_error_handler(prevent_error)
    updater.start_polling()


if __name__ == "__main__":
    main()
