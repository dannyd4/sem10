from telegram import  Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, ConversationHandler, CallbackQueryHandler
import logging


ACTION, SURNAME, NUMBERFON, SEARCH, INPUTNAME = range(5)

def start(update, context):
    '''
    Функция приветствует пользователя, создаёт клавиши в телеграмме и предлагает выбрать действие.
    '''
    user = update.message.from_user
    context.bot.send_message(update.effective_chat.id, 'Приветствую вас в телефонном справочнике.\n' 
    '1 Поиск контакта.\n' 
    '2 Добавление контакта.\n'
    '3 Выход.')
    board = [[InlineKeyboardButton('1. Поиск контакта.', callback_data = '0')], [InlineKeyboardButton('2. Добавить контакт.', callback_data = '1'),],
    [InlineKeyboardButton('3. Выход.', callback_data = '2')]]
    update.message.reply_text('Выбери пункт меню:', reply_markup=InlineKeyboardMarkup(board))
    logging.info(f'Бот запущен {user.username} id {user.id}')
    return ACTION

def action(update, context):
    '''
    Функция отслеживает какую клавишу нажал пользователь и направляет выполнение программы.
    '''
    act = update.callback_query.data
    if act == '0':
        context.bot.send_message(update.effective_chat.id, "Введите поисковый запрос: ")
        logging.info('Пользователь выбрал поиск')
        return SEARCH
    elif act == '1':
            context.bot.send_message(update.effective_chat.id, "Введите Имя: ")
            logging.info('Пользователь выбрал: Добавить контакт.')
            return INPUTNAME
    elif act == '2':
            context.bot.send_message(update.effective_chat.id, "Пока!")
            logging.info('Пользователь выбрал: Выход.')
            logging.info('Завершение работы.')
            return ConversationHandler.END 

def search(update, context):
    data = update.message.text         
    with open('phone.txt', 'r', encoding='utf-8') as file:
        count = 0
        for line in file:            
            if data in line:
                context.bot.send_message(update.effective_chat.id, f'База данных содержит запись. \n{line}')
                logging.info('База данных содержит запись.')
                count += 1                               
    if count == 0:            
        context.bot.send_message(update.effective_chat.id,'База данных не содержит такой записи!')
        logging.info('База данных не содержит такой записи!')
    context.bot.send_message(update.effective_chat.id, "Для возврата в основное меню, нажми: /start")     
    logging.info('Завершение работы.')   
    return ConversationHandler.END 

def input_name(update, context):
    '''
    Функция принимает от пользователя число конфет в игре и проверяет корректность ввода.
    '''
    global name
    name = update.message.text
    context.bot.send_message(update.effective_chat.id, "Введите фамилию: ")
    logging.info(f'Пользователь ввел имя: {name}')
    return SURNAME
    
def sur_name(update, context):
    '''
    Функция принимает от пользователя число конфет в игре и проверяет корректность ввода.
    '''
    global surname
    surname = update.message.text
    context.bot.send_message(update.effective_chat.id, "Введите номер: ")
    logging.info(f'Пользователь ввел фамилию: {surname}')
    return NUMBERFON      

def number_fon(update, context):
    '''
    Функция принимает от пользователя максимальное число конфет которые можно взять и проверяет корректность ввода.
    '''
    
    try:
        num = int(update.message.text)
        logging.info(f'Пользователь ввел номер: {num}')
        write_number(surname, name, num) 
        logging.info(f'Запись успешно добавлена.')
        context.bot.send_message(update.effective_chat.id, "Запись успешно добавлена!")
        context.bot.send_message(update.effective_chat.id, "Для возврата в основное меню, нажми: /start") 
        logging.info('Завершение работы.')       
        return ConversationHandler.END
    except: 
        context.bot.send_message(update.effective_chat.id, "Ты ввел не число! Попробуй еще раз!")
        logging.error("Пользователь ввел не корректное значение")
        return NUMBERFON

def get_id():
    '''
    Функция получает последний ID номер из файла. Если файл пустой возвращает 0. 
    '''    
    try:
        with open('phone.txt', 'r', encoding='utf-8') as file:
            id = int(file.readlines()[-1].split(' ')[0])
        return id
    except:
        return 0
    
def write_number(surname, name, num):
    '''
    Функция записи данных в файл. Принимает в качестве аргументов фамилию, имя и номер телефона, присваивает
    ID, формирует строку и записывает в файл.
    '''
    id = get_id() + 1
    entry = f'{id} {surname} {name} {num}'    
    with open('phone.txt', 'a', encoding='utf-8') as file:
        file.write(entry + '\n')

def cancel(update, context):
    '''
    Функция принимает от пользователя команду закончить работу и останавливает выполнение программы.
    '''
    context.bot.send_message(update.effective_chat.id, "Пока!")
    logging.info('Завершение работы.')
    return ConversationHandler.END