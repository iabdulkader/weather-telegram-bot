import logging
import requests, json, time
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv
from dotenv import dotenv_values

config = dotenv_values(".env")

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


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


def farhad_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Bokachoda to?')


def weather(update: Update, context: CallbackContext) -> None:
    api_key = "b78ac697e648cb55b8f9ceb396f62e48"
    base_url = "https://api.openweathermap.org/data/2.5/weather?q="
    city = update.message.text.split(" ")[1].lower()


    def weather_data(url, key, city):
        complete_url = url + city + "&appid=" + key
        response = requests.get(complete_url)
        x = response.json()
        print(x)

        if (x["cod"] == '404'):
            string = f'''Invalid City'''
            return string
        else:
            string = f'''temperture of  {city} is  {"%.2f" % ((x['main']['temp']) - 273)} Degree Celsius
But it feels like : {"%.2f" % ((x['main']["feels_like"]) - 273)} Celcius
Humidity of {city} is : {(x['main']['humidity'])} %
In {city} weather condition is: {(x['weather'][0]['description'])} today
The wind speed in {city} is : {(x['main']['temp'])} m/s today
'''
            return string

    update.message.reply_text(weather_data(base_url, api_key, city))


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(config['bot_token'])

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("farhad", farhad_command))
    dispatcher.add_handler(CommandHandler("weather", weather))

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
