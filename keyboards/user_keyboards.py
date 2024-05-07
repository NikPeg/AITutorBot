from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup,ReplyKeyboardMarkup,KeyboardButton


def take_markup(numb):
    markup = InlineKeyboardMarkup(row_width=True)
    markup.add(InlineKeyboardButton(text='👩‍🎓Кто сдал?',callback_data=f'take_{numb}'))
    return markup
def user_markup():
    markup = InlineKeyboardMarkup(resize_keyboard=True,row_width=True)
    markup.add(InlineKeyboardButton(text='📚Список заданий',callback_data=f'userworks'))
    return markup
def user_t_markup(numb):
    markup = InlineKeyboardMarkup(resize_keyboard=True, row_width=True)
    markup.add(InlineKeyboardButton(text='✈️Отправить решение', callback_data=f'send_{numb}'),
               InlineKeyboardButton(text='🤔Задать вопрос', callback_data=f'ask_{numb}'),
               )
    return markup


def t_check_markup(user_id,numb):
    markup = InlineKeyboardMarkup(resize_keyboard=True, row_width=True)
    markup.add(InlineKeyboardButton(text='👍Отправить проверку студенту', callback_data=f'allow_{user_id}_{numb}'),
               InlineKeyboardButton(text='👎Ввести свой вариант проверки', callback_data=f'no_{user_id}_{numb}'),
               )
    return markup

def user_return_markup():
    markup = InlineKeyboardMarkup(resize_keyboard=True,row_width=True)
    markup.add(InlineKeyboardButton(text='Назад',callback_data=f'return'))
    return markup


def t_menu():
    markup = InlineKeyboardMarkup(resize_keyboard=True,row_width=True)
    markup.add(InlineKeyboardButton(text='👨‍🎓Список студентов',callback_data='all'),
               InlineKeyboardButton(text='📚Список заданий',callback_data='works'),
               InlineKeyboardButton(text='🔗Ссылка для студентов',callback_data='link'),
               )
    return markup

def user_info(user_id):
    markup = InlineKeyboardMarkup(resize_keyboard=True,row_width=True)
    markup.add(InlineKeyboardButton(text='📚Список сданных работ',callback_data=f'info_{user_id}'))
    return markup


