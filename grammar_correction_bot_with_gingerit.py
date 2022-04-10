import logging
from gingerit.gingerit import GingerIt

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent, Update
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, CallbackContext
from telegram.utils.helpers import escape_markdown
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
parser = GingerIt()


api_key = "1977947414:AAGwtoKBw9txvw-53dnPMgZ3v6Y8rtJ-knw"


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    text = update.message.text
    json_result = parser.parse(text)
    entered_text = f'''{json_result['text']}'''
    result = f'''{json_result['result']}'''

    all_mistakes = "";
    corrections = json_result['corrections']
    for i in range(1,len(json_result['corrections'])+1):
        error_text = f'''{json_result['corrections'][i-1]['text']}'''
        corrected_text = f'''{json_result['corrections'][i-1]['correct']}'''
        all_mistakes = all_mistakes + f"{i}) <s>{error_text}</s> >> {corrected_text} \n"

    if text != result:
        update.message.reply_text(f"<b>[CORRECTED SENTENCE]</b> 👇 \n{result} \n\n <b>There were {len(json_result['corrections'])} mistakes  ❌</b> \n <i>{all_mistakes}</i>",parse_mode= ParseMode.HTML)
    else:
        update.message.reply_text(f"<b>You have no mistakes  ✅ </b>",parse_mode= ParseMode.HTML)



def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(api_key)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()