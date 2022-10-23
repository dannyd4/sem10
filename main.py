from telegram import  Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, ConversationHandler, CallbackQueryHandler
from config import TOKEN
import logging
from func import*

bot = Bot(token=TOKEN)
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher



logging.basicConfig(level=logging.INFO, filename="py_log_book.log", filemode="a",
                    format="%(asctime)s %(levelname)s %(message)s", datefmt="%Y/%m/%d, %H:%M:%S", encoding='UTF-8')

logger = logging.getLogger(__name__)



conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={ACTION: [CallbackQueryHandler(action)],            
            INPUTNAME: [MessageHandler(Filters.text & ~Filters.command, input_name)],
            SURNAME: [MessageHandler(Filters.text & ~Filters.command, sur_name)],
            NUMBERFON: [MessageHandler(Filters.text & ~Filters.command, number_fon)],
            SEARCH: [MessageHandler(Filters.text & ~Filters.command, search)],                       
            },
    fallbacks=[CommandHandler('cancel', cancel)])

dispatcher.add_handler(conv_handler)
updater.start_polling()
updater.idle()